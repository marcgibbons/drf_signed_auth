# DRF Signed Auth
A stateless authentication backend intended to temporarily expose protected
resources.

[![Build Status](https://travis-ci.org/marcgibbons/drf_signed_auth.png?branch=master)](https://travis-ci.org/marcgibbons/drf_signed_auth)
[![Code Coverage](https://codecov.io/gh/marcgibbons/drf_signed_auth/branch/master/graph/badge.svg)](https://codecov.io/gh/marcgibbons/drf_signed_auth)


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


## Is this secure?
Use this backend with caution and sparingly. Anyone with a copy of the signed
URL will be able to access a protected resource, so keep the expiry time
short (see settings), and ensure that the Django `SECRET_KEY` setting is kept
private.


## Requirements
- Python 2.7 / 3.6
- Django 1.8, 1.9, 1.10, 1.11
- Django REST Framework 3.6, 3.7


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
    url(r'^sign-url/$', SignUrlView.as_view(), name='sign-url'),
    ...
]
```

Use the authentication backend on the view you wish to expose.

```python
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

### Example

```
# Request
POST /sign-url  HTTP/1.1
HOST your.api.host
Content-Type: application/json

{"url": "/path"}


# Response
http://your.api.host/path?sig=xxxxxxxxxxxxxxx
```

The returned URL will be valid for the time specified by the `SIGNED_URL_TTL`.


## Settings

The following settings may be configured in your project's `settings.py`

| Setting                   | Description                                           | Default |
| --- | --- | --- |
| `SIGNED_URL_TTL`          | The time in seconds for which the signature is valid  | `30` (seconds) |
| `SIGNED_URL_QUERY_PARAM`  | The querystring variable name                         | `sig` |
| `SIGNED_URL_PERMISSION_CLASSES`  | Permission classes on the signed URL view | `[rest_framework.permissions.IsAuthenticated]` |
