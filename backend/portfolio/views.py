import errno
import string
import random
from io import BytesIO

from django.http.response import JsonResponse, Http404, HttpResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import portfolio
 
from portfolio.models import Portfolio
from portfolio.serializers import PortfolioSerializer
from portfolio.models import Image
from portfolio.serializers import ImageSerializer
from rest_framework.decorators import api_view
import requests
from django.conf import settings
import os
from PIL import Image as PImage
import json
from datetime import datetime

@api_view(['GET', 'POST', 'DELETE'])
def PortfolioViewSet(request):
    # GET request handler
    if request.method == 'GET':
        portfolio = Portfolio.objects.all()
        
        user = request.query_params.get('user', None)
        if user is not None:
            users = portfolio.filter(user=user)
        
            portfolio_serializer = PortfolioSerializer(users, many=True)
        return JsonResponse(portfolio_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    # POST request handler
    elif request.method == 'POST':
        portfolio_data = JSONParser().parse(request)
        if 'id' in portfolio_data.keys():
            port_id = portfolio_data['id']
        else:
            port_id = None
        # check if id is provided, then run update
        if port_id is not None:
            portfolio_f = Portfolio.objects.all().filter(id=port_id)[0]
            portfolio_serializer = PortfolioSerializer(portfolio_f, data=portfolio_data)
        else:
            portfolio_serializer = PortfolioSerializer(data=portfolio_data)
        if portfolio_serializer.is_valid():
            portfolio_serializer.save()
            return JsonResponse(portfolio_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(portfolio_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete request handler
    elif request.method == 'DELETE':
        portfolio = Portfolio.objects.all()
        
        user = request.query_params.get('user', None)
        image_id = request.query_params.get('photo', None)
        
        if user is not None and image_id is not None:
            entry = portfolio.filter(user=user, photo=image_id)
            count = entry.delete()
            return JsonResponse({'message': '{} Portfolio entries were deleted successfully!'.format(count[0])},
                                status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Invalid portfolio entry!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ImageAddViewSet(request):
    # POST request handler, for creation and updating
    if request.method == 'POST':
        image_data = JSONParser().parse(request)
        if 'id' in image_data.keys():
            image_id = image_data['id']
        else:
            image_id = None
        # check if id is provided, then run update
        if image_id is not None:
            images_f = Image.objects.all().filter(id=image_id)[0]
            image_serializer = ImageSerializer(images_f, data=image_data)
        else:
            image_serializer = ImageSerializer(data=image_data)

        if image_serializer.is_valid():
            image_serializer.save()
            return JsonResponse(image_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET request handler
    elif request.method == 'GET':
        images = Image.objects.all()
        
        image_id = request.query_params.get('id', None)
        if image_id is not None:
            images_f = images.filter(id=image_id)
            image_serializer = ImageSerializer(images_f, many=True)
        else:
            image_serializer = ImageSerializer(images, many=True)

        return JsonResponse(image_serializer.data, safe=False)

    # DELETE request handler
    elif request.method == 'DELETE':
        image = Image.objects.all()
        image_id = request.query_params.get('id', None)
        
        if image_id is not None:
            entry = image.filter(id=image_id)
            count = entry.delete()
            return JsonResponse({'message': '{} Images were deleted successfully!'.format(count[0])},
                                status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Invalid Image ID!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def EditView(request):
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    # make directory if it doesnt exist
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    if request.method == "POST":
        image_data = JSONParser().parse(request)
        url = image_data['url']
        extension = url.split(".")[-1]
        user_id = image_data['user_id']
        edits = image_data['edits']
        pth = os.path.dirname(settings.MEDIA_ROOT)
        image = requests.get(url, allow_redirects=True)

        while True:
            local_url = get_random_string(20)
            new_file = (local_url + "." + extension)
            pth = os.path.join(pth, (local_url + "." + extension))
            if not os.path.exists(pth):
                break
        new_url = request.build_absolute_uri(settings.MEDIA_URL + new_file)
        im = PImage.open(BytesIO(image.content))
        if 'crop' in edits.keys():
            crop = edits['crop']
            box = (crop[0], crop[1], crop[2], crop[3])
            mod_image = im.crop(box)
        if 'resize' in edits.keys():
            resize = (edits['resize'][0], edits['resize'][1])
            mod_image = im.resize(resize)

        mod_image.save(pth)
        # save modified image to database
        payload = {"url": new_url, "mods": edits}
        image_r = requests.post("http://127.0.0.1:8000/image/", json=payload)
        image_id = json.loads(image_r.content)['id']
        payload = {"user": user_id, "photo": image_id}
        port_r = requests.post("http://127.0.0.1:8000/portfolio/", json=payload)

        # log edit
        log_path = os.path.join(os.path.dirname(__file__), "logs")
        # make path if it doesnt exist
        mkdir_p(log_path)
        log_file = open(os.path.join(log_path, "edit_log.log"), "a")
        time = datetime.now()
        entry = str(time) + ";user_id=" + str(user_id) + ";url=" + url + ";edits=" + str(edits) + "\n"
        entry = entry.replace("'", '"')
        log_file.write(entry)

        return JsonResponse({"message": "Created"}, status=status.HTTP_201_CREATED)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@api_view(["GET"])
def LogView(request):
    if request.method == "GET":
        passed_user_id = request.query_params.get('user_id', None)
        if passed_user_id is None:
            return JsonResponse({'message': 'Invalid User ID!'}, status=status.HTTP_400_BAD_REQUEST)
        log_path = os.path.join(os.path.dirname(__file__), "logs")
        log_file = open(os.path.join(log_path, "edit_log.log"), "r")
        logs = dict()
        for line in log_file:
            print(str(line.split(",")) + "\n---\n")
            if ';' not in line:
                break
            data = line.split(";")
            time = data[0]
            user_id = data[1].split("=")[1]
            url = data[2].split("=")[1]
            edits = json.loads(data[3].split("=")[1])
            if int(user_id) == int(passed_user_id):
                logs[time] = {"user_id": user_id, "url": url, "edits": edits}
        return JsonResponse(logs, status=status.HTTP_200_OK)
