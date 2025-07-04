from django.urls import get_resolver, URLPattern, URLResolver
from rest_framework.response import Response
from rest_framework.views import APIView

class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        resolver = get_resolver()
        api_endpoints = []

        def extract_patterns(patterns, prefix=''):
            for pattern in patterns:
                if isinstance(pattern, URLPattern):  # Regular URL pattern
                    api_endpoints.append({
                        "pattern": prefix + convert_regex_to_path_converter(str(pattern.pattern)),
                        "name": pattern.name,
                        "callback": f"{pattern.callback.__module__}.{pattern.callback.__qualname__}",
                    })
                elif isinstance(pattern, URLResolver):  # Nested resolver
                    extract_patterns(pattern.url_patterns, prefix + str(pattern.pattern))

        extract_patterns(resolver.url_patterns)
        return Response(api_endpoints)

def convert_regex_to_path_converter(regex):
    """
    Converts Django regex patterns into readable Django path converters.
    Example:
    - Converts (?P<slug>[^/.]+) to <slug:slug>
    """
    import re

    # Replace regex groups with Django path converters
    regex = re.sub(r'\(\?P<(\w+)>[^)]+\)', r'<slug:\1>', regex)
    # Remove start (^) and end ($) markers
    regex = regex.replace('^', '').replace('$', '')
    return regex