from rest_framework import serializers
from .models import Product


class ProductTranslationSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    description = serializers.CharField()
    benefits = serializers.ListField(child=serializers.CharField())
    howToUse = serializers.CharField()
    ingredients = serializers.CharField()
    badge = serializers.CharField(allow_null=True, required=False)


class ProductSerializer(serializers.ModelSerializer):
    howToUse = serializers.CharField(source='how_to_use', read_only=True)
    image = serializers.SerializerMethodField()
    badge = serializers.SerializerMethodField()
    ar = serializers.SerializerMethodField()
    price = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'price',
            'image',
            'badge',
            'description',
            'benefits',
            'howToUse',
            'ingredients',
            'ar',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url or ''

    def get_badge(self, obj):
        return obj.badge if obj.badge else None

    def get_ar(self, obj):
        if not (obj.name_ar or obj.description_ar or obj.category_ar):
            return None
        return {
            'name': obj.name_ar or obj.name,
            'category': obj.category_ar or obj.category,
            'description': obj.description_ar or obj.description,
            'benefits': obj.benefits_ar if obj.benefits_ar else (obj.benefits or []),
            'howToUse': obj.how_to_use_ar or obj.how_to_use,
            'ingredients': obj.ingredients_ar or obj.ingredients,
            'badge': obj.badge_ar if obj.badge_ar else (obj.badge or None),
        }
