import time
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from django.urls import reverse
from django_tables2 import SingleTableView
from .models import ImageProcessingResult
from .tasks import process_image_task
from .tables import ResultTable


class HomeView(SingleTableView):
    model = ImageProcessingResult
    table_class = ResultTable
    template_name = 'core/home.html'
    ordering = ['-created_at']


class UploadImageView(View):
    def post(self, request):
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)

        image = request.FILES['image']
        result = ImageProcessingResult.objects.create(image=image)

        # Start async processing
        process_image_task.delay(result.id)

        return JsonResponse({
            'id': result.id,
            'status_url': reverse('status', kwargs={'result_id': result.id})
        })


class ProcessStatusView(View):
    def get(self, request, result_id):
        try:
            result = ImageProcessingResult.objects.get(id=result_id)
            return JsonResponse({
                'status': result.status,
                'result': result.result,
                'created_at': result.created_at.isoformat(),
                'filename': result.image.name.split('/')[-1],
            })
        except ImageProcessingResult.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)


class BulkUploadTestView(View):
    def get(self, request):
        return render(request, 'core/bulk_upload.html')

    def post(self, request):
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)

        image = request.FILES['image']
        results = []

        for i in range(100):
            result = ImageProcessingResult.objects.create(image=image)
            process_image_task.delay(result.id)
            results.append({
                'id': result.id,
                'status_url': reverse('status', kwargs={'result_id': result.id})
            })

        return JsonResponse({'results': results})
