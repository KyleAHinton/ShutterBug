#########################################################################################################################
# Author: Paul Wells
# Purpose: Retrieve image url's from websites based on search params
# Valid Params: 
#   aspect_ratio: must be width divided by height, example 16:9 is 1.7778
#   aspect_ratio_min: boolean, if true then it will search for anything greater than or equal to passed in aspect ratio,
#      false means it will return less than or equal to the passed in ratio, no value passed in means only equal.
#   color: string hex value for dominant color search
#   height: pixel height
#   height_from: boolean, if true then height value greater than or equal, false lessthan or equal, none exact
#   orientation: string, either "vertical", "horizontal"
#   page: page number
#   per_page: num of results per page
#   query: string search term
#   width: pixel width
#   width_from: boolean, if true then width value greater than or equal, false lessthan or equal, none exact
#########################################################################################################################  
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import urllib

@api_view(['GET'])
def ImageViewSet(request):
    in_params = request.query_params
    shutter_key = "v2/Uktud084elNpdnJuNVlyV0dkOEY0ekVHZjdESDl4akcvMjg1MjkyMzE3L2N1c3RvbWVyLzMvQkcwYV9ORkdDYnFtVHBIX19HR3JwMThFLWxvSDBwT1puWEdmQVVUYVlNSGxPejVtSm9aYndXRk9JeVJxUm9TTUV5TnhNRGVieldSUWNpRzV6VV92SDdwZEQyRnNQM1J3Sm55bldsNExIeUh4dkpDYU9tWlJaOVFOS2lDbkY2V2ZOa2NrT2F3b3dXYUtBUTctWDNCRkJ2VWVhUUZxQlQ4d0REVjVBSVJ0UWY0bnR3QVg1Zm5QY0dybnY2NEtLam5UakRKazJvbGxnWk5yQ3BrN3BhVXpxQQ"

    header = {'Authorization' : ('bearer ' + shutter_key)}
    
    # validate query
    options = {}
    for key, value in in_params.items():
        if key == "aspect_ratio":
            if not "aspect_ratio_min" in in_params.keys():
                options['aspect_ratio'] = value
            elif in_params['aspect_ratio']:
                options['aspect_ratio_min'] = value
            else:
                options['aspect_ratio_max'] = value
        elif key == "color":
            options['color'] = value
        elif key == "height":
            if not "height_from" in in_params.keys():
                options['height'] = value
            elif in_params['height_from']:
                options['height_from'] = value
            else:
                options['height_to'] = value
        elif key == "orientation":
            if value == "vertical" or value == "horizontal":
                options['orientation'] = value
        elif key == "page":
            if isInstance(value, int):
                options['page'] = value
        elif key == "per_page":
            if isInstance(value, int):
                options['per_page'] = value
        elif key == "query":
            options['query'] = str(value)
        elif key == "width":
            if not "width_from" in in_params.keys():
                options['width'] = value
            elif in_params['width_from']:
                options['width_from'] = value
            else:
                options['width_to'] = value
    # pass valid query
    url = urllib.parse.urlencode(options)
    resp = requests.get(('https://api.shutterstock.com/v2/images/search?' + url), headers=header)
    url1 = resp.json()['data'][0]['assets']['preview']['url']
    return Response(url1)