"""
Contains app-settings imported from Django with default values
"""
from django.conf import settings

# Time (in seconds) URL is valid
# Default: 30
SIGNED_URL_TTL = getattr(settings, 'SIGNED_URL_TTL', 30)

# Query parameter variable name
# Default: 'sig'  =>  /fizz?sig=<signature>
SIGNED_URL_QUERY_PARAM = getattr(settings, 'SIGNED_URL_QUERY_PARAM', 'sig')
