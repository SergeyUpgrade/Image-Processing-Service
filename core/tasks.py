import time
import random
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from .models import ImageProcessingResult

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3)
def process_image_task(self, result_id):
    try:
        logger.info(f"Starting processing for result_id: {result_id}")

        # Get the result object with select_for_update to lock the row
        result = ImageProcessingResult.objects.select_for_update().get(id=result_id)

        if result.status == 'completed':
            logger.warning(f"Result {result_id} already completed")
            return {'status': 'already_completed'}

        result.status = 'processing'
        result.save(update_fields=['status'])
        logger.info(f"Set status to processing for {result_id}")

        # Simulate processing (20 seconds)
        for i in range(20):
            time.sleep(1)
            logger.debug(f"Processing {result_id} - {i + 1}/20 seconds")

        # Generate and save result
        result.result = random.randint(1, 1000)
        result.processing_time = 20.0
        result.status = 'completed'
        result.save()

        logger.info(f"Completed processing for {result_id}. Result: {result.result}")
        return {'status': 'success', 'result': result.result}

    except ImageProcessingResult.DoesNotExist:
        logger.error(f"Result {result_id} not found")
        raise self.retry(exc=Exception(f"Result {result_id} not found"), countdown=60)
    except Exception as e:
        logger.error(f"Error processing {result_id}: {str(e)}")
        if 'result' in locals():
            result.status = 'failed'
            result.save(update_fields=['status'])
        raise self.retry(exc=e, countdown=60)