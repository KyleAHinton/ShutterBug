from rest_framework import serializers 
from portfolio.models import Image
from portfolio.models import Portfolio
 
 
class ImageSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Image
        fields = ('id', 'url', 'mods')
        
class PortfolioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Portfolio
        fields = ('id', 'photo', 'user', 'tags')
