from .models import Category, SubCategory, Brand, Item, ItemVariant, ProductImage
from utils.serializers import DynamicFieldsModelSerializer, FileUploadField, ExcludeFieldsMixin


class CategorySerializer(ExcludeFieldsMixin, DynamicFieldsModelSerializer):
    image = FileUploadField()

    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(ExcludeFieldsMixin, DynamicFieldsModelSerializer):
    image = FileUploadField()

    class Meta:
        model = SubCategory
        fields = '__all__'


class BrandSerializer(ExcludeFieldsMixin, DynamicFieldsModelSerializer):
    image = FileUploadField()

    class Meta:
        model = Brand
        fields = '__all__'


class ItemSerializer(ExcludeFieldsMixin, DynamicFieldsModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemVariantSerializer(ExcludeFieldsMixin, DynamicFieldsModelSerializer):
    class Meta:
        model = ItemVariant
        fields = '__all__'


class ProductImageSerializer(ExcludeFieldsMixin, DynamicFieldsModelSerializer):
    image = FileUploadField()

    class Meta:
        model = ProductImage
        fields = '__all__'
