from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from portfolio.models import Portfolio
from portfolio.serializers import PortfolioSerializer
from portfolio.models import Image
from portfolio.serializers import ImageSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def PortfolioViewSet(request):
    if request.method == 'GET':
        portfolio = Portfolio.objects.all()
        
        user = request.query_params.get('user', None)
        if user is not None:
            users = portfolio.filter(user=user)
        
            Portfolio_serializer = PortfolioSerializer(users, many=True)
        return JsonResponse(Portfolio_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        portfolio_data = JSONParser().parse(request)
        portfolio_serializer = PortfolioSerializer(data=portfolio_data)
        if portfolio_serializer.is_valid():
            portfolio_serializer.save()
            return JsonResponse(portfolio_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(portfolio_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        portfolio = Portfolio.objects.all()
        
        user = request.query_params.get('user', None)
        image_id = request.query_params.get('photo', None)
        
        if user is not None and image_id is not None:
            entry = portfolio.filter(user=user, photo=image_id)
            count = entry.delete()
            return JsonResponse({'message': '{} Portfolio entries were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Invalid portfolio entry!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def ImageAddViewSet(request):
    if request.method == 'POST':
        image_data = JSONParser().parse(request)
        image_serializer = ImageSerializer(data=image_data)
        if image_serializer.is_valid():
            image_serializer.save()
            return JsonResponse(image_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        images = Image.objects.all()
        
        image_id = request.query_params.get('id', None)
        if image_id is not None:
            images_f = images.filter(id=image_id)
            image_serializer = ImageSerializer(images_f, many=True)
        else:
            image_serializer = ImageSerializer(images, many=True)

        return JsonResponse(image_serializer.data, safe=False)
    elif request.method == 'DELETE':
        image = Image.objects.all()
        image_id = request.query_params.get('id', None)
        
        if image_id is not None:
            entry = portfolio.filter(id=image_id)
            count = entry.delete()
            return JsonResponse({'message': '{} Images were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Invalid Image ID!'}, status=status.HTTP_400_BAD_REQUEST)