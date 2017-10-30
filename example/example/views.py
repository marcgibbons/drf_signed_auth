from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token


def index(request):
    # Get an access token for George. Depends on fixtures.
    george = get_user_model().objects.get(username='george')
    token = Token.objects.get(user=george)

    # We'll pass the token to the template and set it as a
    # global XHR authorization header.
    return render(request, 'index.html', {'token': token.key})
