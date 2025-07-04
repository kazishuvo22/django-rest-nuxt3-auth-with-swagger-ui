from django.core.exceptions import ValidationError
from PIL import Image
import os


def validate_image_format(value):
    """Validate the image format to allow only PNG, JPEG, and JPG."""
    valid_mime_types = ['image/png', 'image/jpeg']
    file_mime_type = value.file.content_type
    if file_mime_type not in valid_mime_types:
        raise ValidationError("Invalid file format. Only PNG, JPEG, and JPG are allowed.")


def compress_image(image_path):
    """Compress the image to 50% quality."""
    try:
        with Image.open(image_path) as img:
            img_format = img.format
            # Ensure the format is valid
            if img_format not in ["PNG", "JPEG"]:
                raise ValidationError("Invalid image format.")
            # Compress and save the image
            img.save(image_path, format=img_format, quality=50, optimize=True)
    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)  # Remove the invalid file
        raise ValidationError(f"Error compressing image: {e}")
