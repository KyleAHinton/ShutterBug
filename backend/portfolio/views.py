import errno
import string
import random
from io import BytesIO

from django.http.response import JsonResponse, Http404, HttpResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

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


# Handles functionality behind the endpoint for /portfolio
@api_view(['GET', 'POST', 'DELETE'])
def PortfolioViewSet(request):
    # GET request handler
    if request.method == 'GET':
        # get all portfolios
        portfolio = Portfolio.objects.all()
        # get user id
        user = request.query_params.get('user', None)

        # only return data if a user id has been provided
        if user is not None:
            users = portfolio.filter(user=user)
            portfolio_serializer = PortfolioSerializer(users, many=True)

        return JsonResponse(portfolio_serializer.data, safe=False)

    # POST request handler
    elif request.method == 'POST':
        # get passed in data
        portfolio_data = JSONParser().parse(request)

        # if an id is provided then overwrite existing
        if 'id' in portfolio_data.keys():
            port_id = portfolio_data['id']
        # else create new
        else:
            port_id = None

        # check if id is provided, then run update
        if port_id is not None:
            portfolio_f = Portfolio.objects.all().filter(id=port_id)[0]
            portfolio_serializer = PortfolioSerializer(portfolio_f, data=portfolio_data)
        # else create new
        else:
            portfolio_serializer = PortfolioSerializer(data=portfolio_data)

        # if inputted data is valid save to database
        if portfolio_serializer.is_valid():
            portfolio_serializer.save()
            return JsonResponse(portfolio_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(portfolio_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete request handler
    elif request.method == 'DELETE':
        # get all portfolio objects
        portfolio = Portfolio.objects.all()

        # get passed in params to delete
        user = request.query_params.get('user', None)
        image_id = request.query_params.get('photo', None)

        # make sure both params are present
        if user is not None and image_id is not None:
            # get matching entry and delete
            entry = portfolio.filter(user=user, photo=image_id)
            count = entry.delete()
            return JsonResponse({'message': '{} Portfolio entries were deleted successfully!'.format(count[0])},
                                status=status.HTTP_204_NO_CONTENT)

        # else return bad request
        return JsonResponse({'message': 'Invalid portfolio entry!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ImageAddViewSet(request):
    # POST request handler, for creation and updating
    if request.method == 'POST':
        # get inputted image data
        image_data = JSONParser().parse(request)

        # if id is present then overwrite
        if 'id' in image_data.keys():
            image_id = image_data['id']
        else:
            image_id = None

        # check if id is provided, then run update
        if image_id is not None:
            images_f = Image.objects.all().filter(id=image_id)[0]
            image_serializer = ImageSerializer(images_f, data=image_data)
        # else create new
        else:
            image_serializer = ImageSerializer(data=image_data)

        # insure info is valid then save if it is
        if image_serializer.is_valid():
            image_serializer.save()
            return JsonResponse(image_serializer.data, status=status.HTTP_201_CREATED)

        # else return bad request
        return JsonResponse(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET request handler
    elif request.method == 'GET':
        # get all image objects
        images = Image.objects.all()

        # if image id is provided get specified image
        image_id = request.query_params.get('id', None)
        if image_id is not None:
            images_f = images.filter(id=image_id)
            image_serializer = ImageSerializer(images_f, many=True)
        # else get all images
        else:
            image_serializer = ImageSerializer(images, many=True)

        # returns nothing if bad request
        return JsonResponse(image_serializer.data, safe=False)

    # DELETE request handler
    elif request.method == 'DELETE':
        # get all images
        image = Image.objects.all()
        image_id = request.query_params.get('id', None)

        # ensure image id was provided
        if image_id is not None:
            # delete image
            entry = image.filter(id=image_id)
            count = entry.delete()
            return JsonResponse({'message': '{} Images were deleted successfully!'.format(count[0])},
                                status=status.HTTP_204_NO_CONTENT)\

        # else return bad response
        return JsonResponse({'message': 'Invalid Image ID!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def EditView(request):
    # used to generate random url string for saved modified images
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

    # handle POST request
    if request.method == "POST":
        # get passed in data
        image_data = JSONParser().parse(request)
        url = image_data['url']
        # get image extension
        extension = url.split(".")[-1]
        user_id = image_data['user_id']
        edits = image_data['edits']
        # get path to where image will be saved
        pth = os.path.dirname(settings.MEDIA_ROOT)
        # get image from url
        image = requests.get(url, allow_redirects=True)

        # create local file with random strings
        count = 0
        # keep trying until 500 attempts or unique string is created
        while True:
            local_url = get_random_string(20)
            new_file = (local_url + "." + extension)
            pth = os.path.join(pth, (local_url + "." + extension))
            # break loop if unique string found
            if not os.path.exists(pth):
                break
            # raise internal server error if it cant find a unique sting in 500 attempts
            elif count >= 500:
                return HttpResponse(status=500)
            # increment attempt counter
            count += 1

        # create new url to save to image object
        new_url = request.build_absolute_uri(settings.MEDIA_URL + new_file)
        # create pillow image object for modification
        im = PImage.open(BytesIO(image.content))

        # check which edits have been specified and apply them
        if 'crop' in edits.keys():
            crop = edits['crop']
            box = (crop[0], crop[1], crop[2], crop[3])
            mod_image = im.crop(box)
        if 'resize' in edits.keys():
            resize = (edits['resize'][0], edits['resize'][1])
            mod_image = im.resize(resize)

        # save modified image locally
        mod_image.save(pth)

        # save modified image to database through API calls
        payload = {"url": new_url, "mods": edits}
        image_r = requests.post("http://127.0.0.1:8000/image/", json=payload)
        # get returned image id from API call
        image_id = json.loads(image_r.content)['id']
        payload = {"user": user_id, "photo": image_id}
        port_r = requests.post("http://127.0.0.1:8000/portfolio/", json=payload)

        # create log
        log_path = os.path.join(os.path.dirname(__file__), "logs")
        # make path if it doesnt exist
        mkdir_p(log_path)
        log_file = open(os.path.join(log_path, "edit_log.log"), "a")
        # create log values
        time = datetime.now()
        entry = str(time) + ";user_id=" + str(user_id) + ";url=" + url + ";edits=" + str(edits) + "\n"
        # format for later json.loads()
        entry = entry.replace("'", '"')
        # add new line
        log_file.write(entry)

        return JsonResponse({"message": "Created"}, status=status.HTTP_201_CREATED)


# download image from media folder
def download(request, path):
    # get path from url and find system file path with it
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        # return image if its found
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    # return 404 for bad image name
    raise Http404


# get all edit logs related to a user
@api_view(["GET"])
def LogView(request):
    # handles GET request
    if request.method == "GET":
        # get user id from params
        passed_user_id = request.query_params.get('user_id', None)
        # ensure the id is provided
        if passed_user_id is None:
            return JsonResponse({'message': 'Invalid User ID!'}, status=status.HTTP_400_BAD_REQUEST)
        # get the log path
        log_path = os.path.join(os.path.dirname(__file__), "logs")
        log_file = open(os.path.join(log_path, "edit_log.log"), "r")
        # create emptry dict object for return
        logs = dict()

        # iterate through file
        for line in log_file:
            # check if its the last line, which is a newline, if it is skip it
            if ';' not in line:
                break

            # split log entry by semi-colons
            data = line.split(";")
            # get data from log
            time = data[0]
            user_id = data[1].split("=")[1]
            url = data[2].split("=")[1]
            edits = json.loads(data[3].split("=")[1])

            # check if user in log line is the same as the one being requested
            if int(user_id) == int(passed_user_id):
                # add log entry to return for user with time being the key
                logs[time] = {"user_id": user_id, "url": url, "edits": edits}

        # return JSON with logs, logs will be empty if nothing is found
        return JsonResponse(logs, status=status.HTTP_200_OK)
