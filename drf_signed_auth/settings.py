"""
Contains app-settings imported from Django with default values
"""
from django.conf import settings
from rest_framework import permissions

# Time (in seconds) URL is valid
# Default: 30
SIGNED_URL_TTL = getattr(settings, 'SIGNED_URL_TTL', 30)

# Query parameter variable name
# Default: 'sig'  =>  /fizz?sig=<signature>
SIGNED_URL_QUERY_PARAM = getattr(settings, 'SIGNED_URL_QUERY_PARAM', 'sig')

# Permission classes for signing view.
# Default: IsAuthenticated
SIGNED_URL_PERMISSION_CLASSES = getattr(
    settings,
    'SIGNED_URL_PERMISSION_CLASSES',
    [permissions.IsAuthenticated]
)
