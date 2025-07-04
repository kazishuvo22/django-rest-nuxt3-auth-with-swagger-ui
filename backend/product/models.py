from django.db import models
from django.utils.text import slugify
from product.helpers import compress_image, validate_image_format


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(
        upload_to="category_images/",
        null=True,
        blank=True,
        validators=[validate_image_format]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.image:
            compress_image(self.image.path)

    def __str__(self):
        return self.name


# Subcategory Model
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(
        upload_to="subcategory_images/",
        null=True,
        blank=True,
        validators=[validate_image_format]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.image:
            compress_image(self.image.path)

    def __str__(self):
        return self.name


# Brand Model
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(
        upload_to="brand_images/",
        validators=[validate_image_format]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.image:
            compress_image(self.image.path)

    def __str__(self):
        return self.name


# Item Model
class Item(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="items")
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name="items", null=True,
                                    blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, related_name="items", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(
        max_length=10,
        choices=[('percentage', 'Percentage'), ('flat', 'Flat Amount')],
        blank=True,
        null=True,
        help_text="Choose 'Percentage' for a percent discount or 'Flat' for a fixed amount."
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Enter the discount value. For percentage, input a number between 0 and 100."
    )
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Price after applying the discount."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the discounted price before saving
        if self.discount_type == 'percentage' and self.discount_value:
            discount = (self.price * self.discount_value) / 100
            self.discounted_price = self.price - discount
        elif self.discount_type == 'flat' and self.discount_value:
            self.discounted_price = self.price - self.discount_value
        else:
            self.discounted_price = self.price

        # Generate slug if not already present
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Item Variant Model (Size, Color, Stock Management)
class ItemVariant(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="variants")
    size = models.CharField(max_length=50, null=True, blank=True)  # Example: "S", "M", "L", "XL"
    color = models.CharField(max_length=50, null=True, blank=True)  # Example: "Red", "Blue", "Black"
    availability = models.CharField(
        max_length=50,
        choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')],
        default='In Stock'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.color or 'No Color'} - {self.size or 'No Size'}"

    @property
    def stock_quantity(self):
        """Calculate current stock quantity dynamically."""
        from stock.models import Stock
        total_stock = Stock.objects.filter(variant=self).aggregate(total=models.Sum('quantity'))['total']
        return total_stock or 0

    @property
    def is_available(self):
        """Determine availability based on stock quantity and status."""
        return self.stock_quantity > 0 and self.availability == 'In Stock'

    def adjust_stock(self, quantity, reason="Manual Adjustment"):
        """Adjust stock using the Stock model."""
        from stock.models import Stock
        Stock.objects.create(variant=self, quantity=quantity, reason=reason)


# Product Image Model for Multiple Images
class ProductImage(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="product_images/",
        validators=[validate_image_format]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        compress_image(self.image.path)

    def __str__(self):
        return f"Image of {self.item.name}"
