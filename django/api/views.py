""" /api/views.py
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


@api_view(['GET'])
def ping_pong(request):
    """
    This view always returns string 'pong!' with status code 200, That's all what it does.

    this view, 'ping' is made for purpose of health-check of backend API server.
    """
    return Response({'ping': 'pong!'}, status=HTTP_200_OK)
