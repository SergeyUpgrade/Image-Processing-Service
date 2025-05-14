import django_tables2 as tables
from .models import ImageProcessingResult
from django.utils.html import format_html


class ResultTable(tables.Table):
    image_name = tables.Column(accessor='image.name', verbose_name='File Name')
    created_at = tables.DateTimeColumn(format='Y-m-d H:i:s')

    class Meta:
        model = ImageProcessingResult
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('image_name', 'result', 'created_at', 'processing_time', 'status')
        attrs = {'class': 'table table-striped table-bordered'}

    def render_image_name(self, value):
        return value.split('/')[-1]

    def render_processing_time(self, value):
        if value:
            return f"{value:.2f}s"
        return "-"

    def render_status(self, value):
        badge_class = {
            'pending': 'bg-secondary',
            'processing': 'bg-info',
            'completed': 'bg-success',
            'failed': 'bg-danger',
        }.get(value, 'bg-secondary')
        return format_html(
            '<span class="badge {}">{}</span>',
            badge_class,
            value.capitalize()
        )
