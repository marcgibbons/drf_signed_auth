# DRF Signed Auth
A stateless authentication backend intended to temporarily expose protected
resources.


## Why?

The motivation for this package comes from a frequent project requirement to
directly download served by the API in formats like CSV or Excel within the
context of a single-page-application.

Within this context, authentication cannot be achieved using HTTP Headers, as
the resource is accessed directly through a URL via an `<a>` tag. Therefore, a
temporary signature passed in the query string must be used to authenticate the
request.


This package uses Django's cryptographic signing to produce a short-lived
signature. It provides a view used to produce the signature and a DRF
authentication backend.


## Requirements
- Python 2.7 / 3.6
- Django 1.8, 1.9, 1.10, 1.11
- Django REST Framework 3.6


## Installation
`pip install drf-signed-auth`


## Quick start
Register the SignUrlView in `urls.py`

```python
# urls.py

from django.conf.urls import url
from drf_signed_auth.views import SignUrlView


urlpatterns = [
    ...
    url(r'sign-url/$', SignUrlView.as_view(), name='sign-url'),
    ...
]
```

Use the authentication backend on the view you wish to expose.

```
# views.py
from drf_signed_auth.authentication import SignedURLAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class MyCSVView(APIView):
    ...
    authentication_classes = [SignedURLAuthentication]
    permission_classes = [IsAuthenticated]
    ...
```

## Usage

Obtain the signature by making a POST request to the Sign URL endpoint, and
provide the `url` of the endpoint you wish to access. This can be a relative
or absolute path.

    ```
    # Request
    POST /sign-url  HTTP/1.1
    HOST your.api.host
    Content-Type: application/json

    {"url": "/path"}


    # Response
    http://your.api.host/path?sig=<the signature>
    ```

The returned URL will be valid for the time specified by the `SIGNED_URL_TTL`.


## Settings

SIGNED_URL_TTL   # The time in seconds for which the signature is valid (Default: 30)
SIGNED_URL_QUERY_PARAM  # The querystring variable name  (Default: `sig`)
SIGNED_URL_PERMISSION_CLASSES  # Default : (`[IsAuthenticated]`)
