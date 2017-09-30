from drf_signed_auth.authentication import SignedURLAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MeView(APIView):
    """
    Returns currently logged in user.

    This view
    """
    authentication_classes = [SignedURLAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'full_name': request.user.get_full_name()
        })
