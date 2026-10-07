from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactSubmitView(APIView):
    """
    POST /api/contact/
    Submit a message / inquiry from the customer contact page.
    """
    def post(self, request, *args, **kwargs):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Inquiry received successfully. Our team will contact you soon."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
