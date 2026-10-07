from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Order
from .serializers import OrderCreateSerializer, OrderDetailSerializer


class OrderCreateView(APIView):
    """
    POST /api/orders/
    Place a new order with delivery info, items, and payment details.
    """
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Handle direct file upload if passed as form field 'receipt_file'
            if 'receipt_file' in request.FILES:
                uploaded = request.FILES['receipt_file']
                order.receipt_image = uploaded
                order.receipt_file_name = uploaded.name
                order.receipt_file_size = uploaded.size
                order.receipt_file_type = uploaded.content_type
                order.receipt_uploaded_at = timezone.now()
                order.save()

            output_serializer = OrderDetailSerializer(order, context={'request': request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """
    GET /api/orders/<id>/
    Fetch an order by ID (e.g. DB-482913), case-insensitive.
    """
    def get(self, request, pk, *args, **kwargs):
        # Case insensitive lookup
        order = Order.objects.filter(id__iexact=pk.strip()).first()
        if not order:
            return Response(
                {"detail": f"Order {pk} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(serializer.data)


class OrderTrackView(APIView):
    """
    GET /api/orders/track/?order=DB-XXXXXX
    Track an order by its tracking / order number query parameter.
    """
    def get(self, request, *args, **kwargs):
        order_number = request.query_params.get('order', '').strip()
        if not order_number:
            return Response(
                {"detail": "Please provide an order number (?order=DB-XXXXXX)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.filter(id__iexact=order_number).first()
        if not order:
            return Response(
                {"detail": f"No order found with number '{order_number}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(serializer.data)


class OrderUploadReceiptView(APIView):
    """
    POST /api/orders/<id>/receipt/
    Upload or replace receipt screenshot for an existing order.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(id__iexact=pk.strip()).first()
        if not order:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if 'receipt' not in request.FILES:
            return Response({"detail": "No file uploaded under 'receipt' key."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['receipt']
        # Validate format
        if not file.content_type in ['image/jpeg', 'image/png', 'image/webp']:
            return Response(
                {"detail": "Invalid file format. Only JPG, PNG, or WebP allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate size (5MB)
        if file.size > 5 * 1024 * 1024:
            return Response(
                {"detail": "File size exceeds 5MB limit."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.receipt_image = file
        order.receipt_file_name = file.name
        order.receipt_file_size = file.size
        order.receipt_file_type = file.content_type
        order.receipt_uploaded_at = timezone.now()
        order.save()

        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(serializer.data)
