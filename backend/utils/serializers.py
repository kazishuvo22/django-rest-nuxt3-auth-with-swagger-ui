from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import ImageField


@extend_schema_field({"type": "string", "format": "binary"})
class FileUploadField(ImageField):
    pass


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Handle `fields` and `exclude` dynamically
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        # Apply `fields` logic
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        # Apply `exclude` logic
        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class ExcludeFieldsMixin:
    def get_fields(self):
        """
        Dynamically exclude fields from the serializer.
        """
        fields = super().get_fields()
        exclude_fields = self.context.get('exclude_fields', [])

        for field_name in exclude_fields:
            fields.pop(field_name, None)

        return fields
