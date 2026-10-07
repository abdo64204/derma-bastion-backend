from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for browsing and searching products.
    Matches frontend catalog filtering, search, sorting, and best sellers.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        sort = self.request.query_params.get('sort')

        # Filter by category
        if category and category.lower() != 'all':
            category_normalized = category.lower().strip()
            if category_normalized in ['skin', 'skin care']:
                qs = qs.filter(Q(category__icontains='Skin') | Q(category_ar__icontains='بشرة'))
            elif category_normalized in ['hair', 'hair care']:
                qs = qs.filter(Q(category__icontains='Hair') | Q(category_ar__icontains='شعر'))
            elif category_normalized in ['eye', 'eye care']:
                qs = qs.filter(Q(category__icontains='Eye') | Q(category_ar__icontains='عيون') | Q(category_ar__icontains='عين'))
            else:
                qs = qs.filter(Q(category__icontains=category) | Q(category_ar__icontains=category))

        # Search query
        if search:
            s = search.strip()
            qs = qs.filter(
                Q(name__icontains=s) |
                Q(name_ar__icontains=s) |
                Q(category__icontains=s) |
                Q(category_ar__icontains=s) |
                Q(description__icontains=s) |
                Q(description_ar__icontains=s) |
                Q(ingredients__icontains=s) |
                Q(ingredients_ar__icontains=s)
            )

        # Sorting
        if sort == 'priceAsc':
            qs = qs.order_by('price')
        elif sort == 'priceDesc':
            qs = qs.order_by('-price')
        elif sort == 'featured':
            qs = qs.order_by('-is_best_seller', 'id')
        else:
            qs = qs.order_by('id')

        return qs

    @action(detail=False, methods=['get'], url_path='best-sellers')
    def best_sellers(self, request):
        best_sellers = self.get_queryset().filter(
            Q(is_best_seller=True) | Q(badge__icontains='Best Seller') | Q(badge_ar__icontains='الأكثر مبيعاً')
        )
        if not best_sellers.exists():
            best_sellers = self.get_queryset()[:8]
        serializer = self.get_serializer(best_sellers, many=True)
        return Response(serializer.data)
