from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import filters


class DynamicFieldsModelViewSet(ModelViewSet):
    # Enable ordering filter globally for this viewset; if postive like id ascending, if -id then descending
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'  # Allow ordering by all model fields (or specify a list of fields)
    ordering = ['id']  # Default ordering

    def get_parser_classes(self):
        """
        Return parsers based on whether the request contains file uploads.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH'] and self.request.FILES:
            return [MultiPartParser, FormParser]
        return [JSONParser]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()

        # Handle dynamic `fields` inclusion
        fields = self.request.query_params.get('fields')
        if fields:
            fields = [f.strip() for f in fields.split(',')]
            kwargs['fields'] = fields

        # Handle dynamic `exclude_fields` for specific methods like POST
        exclude_fields = []
        if self.request.method == 'POST':
            exclude_fields.append('slug')  # Example: Exclude `slug` for POST requests
        kwargs['context'] = {'exclude_fields': exclude_fields}

        return serializer_class(*args, **kwargs)
