from celery import shared_task
from .models import ImageProcessingResult

@shared_task(bind=True)
def process_image_task(self, result_id):
    try:
        result = ImageProcessingResult.objects.get(id=result_id)
        result.status = 'processing'
        result.save()
        result.process_image()
        return {'status': 'success', 'result_id': result_id}
    except ImageProcessingResult.DoesNotExist:
        return {'status': 'error', 'message': 'Result not found'}