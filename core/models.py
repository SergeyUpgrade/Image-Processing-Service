import os
import random
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import time


def image_upload_path(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    return f'uploads/{timestamp}_{filename}'


class ImageProcessingResult(models.Model):
    image = models.ImageField(
        upload_to=image_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    result = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])

    def __str__(self):
        return f"{self.image.name} - {self.result}"

    def process_image(self):
        start_time = time.time()

        # Simulate processing time
        time.sleep(20)

        # Generate random result
        self.result = random.randint(1, 1000)
        self.processing_time = time.time() - start_time
        self.status = 'completed'
        self.save()
