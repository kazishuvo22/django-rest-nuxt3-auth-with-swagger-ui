from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status
from authapp import permissions as authapp_permissions
from .models import Category, SubCategory, Brand, Item, ItemVariant, ProductImage
from .serializers import (
    CategorySerializer, SubCategorySerializer, BrandSerializer,
    ItemSerializer, ItemVariantSerializer, ProductImageSerializer
)
from utils.viewsets import DynamicFieldsModelViewSet


class CategoryViewSet(DynamicFieldsModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]  # Or AllowAny if public
        elif self.action == 'deactivate':
            permission_classes = [authapp_permissions.IsStaffUser]
        else:
            permission_classes = [authapp_permissions.IsStaffUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def deactivate(self, request, slug=None):
        category = self.get_object()
        category.is_active = False
        category.save()
        return Response(
            {"message": f"Category '{category.name}' deactivated."},
            status=status.HTTP_200_OK
        )


class SubCategoryViewSet(DynamicFieldsModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'list_with_categories']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [authapp_permissions.IsStaffUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='list-with-categories')
    def list_with_categories(self, request):
        subcategories = SubCategory.objects.select_related('category')
        data = [
            {
                "id": sub.id,
                "name": sub.name,
                "category": {"id": sub.category.id, "name": sub.category.name}
            }
            for sub in subcategories
        ]
        return Response(data, status=status.HTTP_200_OK)


class BrandViewSet(DynamicFieldsModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [authapp_permissions.IsStaffUser]
        return [permission() for permission in permission_classes]


class ItemViewSet(DynamicFieldsModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [authapp_permissions.IsStaffUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], url_path='full-details')
    def get_item_full_details_by_slug(self, request, slug=None):
        try:
            item = self.get_object()  # Fetch the item based on the slug
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        # Build the response data manually
        response_data = {
            "id": item.id,
            "name": item.name,
            "slug": item.slug,
            "description": item.description,
            "category": item.category.id if item.category else None,
            "subcategory": item.subcategory.id if item.subcategory else None,
            "brand": item.brand.id if item.brand else None,
            "price": str(item.price),
            "created_at": item.created_at.isoformat(),
            "images": [
                {
                    "id": img.id,
                    "image": request.build_absolute_uri(img.image.url),
                    "created_at": img.created_at.isoformat(),
                }
                for img in item.images.all()
            ],
            "variants": [
                {
                    "id": variant.id,
                    "size": variant.size,
                    "color": variant.color,
                    "availability": variant.availability,
                    "stock_quantity": variant.stock_quantity,
                    "is_available": variant.is_available,
                    "created_at": variant.created_at.isoformat(),
                }
                for variant in item.variants.all()
            ],
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ItemVariantViewSet(DynamicFieldsModelViewSet):
    queryset = ItemVariant.objects.all()
    serializer_class = ItemVariantSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [authapp_permissions.IsStaffUser]
        return [permission() for permission in permission_classes]


class ProductImageViewSet(DynamicFieldsModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [authapp_permissions.IsStaffUser]
        return [permission() for permission in permission_classes]
