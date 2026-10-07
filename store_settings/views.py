from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StoreSettings
from .serializers import StoreSettingsSerializer


class StoreConfigView(APIView):
    """
    GET /api/store-config/
    Returns store payment configs (Vodafone Cash, InstaPay), shipping thresholds,
    and official contact information.
    """
    def get(self, request, *args, **kwargs):
        settings = StoreSettings.get_settings()
        serializer = StoreSettingsSerializer(settings)
        return Response(serializer.data)
