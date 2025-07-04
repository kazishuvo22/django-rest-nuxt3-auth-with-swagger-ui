from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, SubCategoryViewSet, BrandViewSet,
    ItemViewSet, ItemVariantViewSet, ProductImageViewSet
)

router = DefaultRouter()

# Register all ViewSets
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'item-variants', ItemVariantViewSet, basename='itemvariant')
router.register(r'product-images', ProductImageViewSet, basename='productimage')

urlpatterns = router.urls