""" /api/views.py
    simple function-based views and class-based viewsets for various APIs

"""
import json
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import History
from core import util
from .serializers import PredictSerializer, HistorySerializer


@api_view(['GET'])
def ping_pong(request):
    """
    This view always returns string 'pong!' with status code 200, That's all what it does.

    this view, 'ping' is made for purpose of health-check of backend API server.
    """
    return Response({'ping': 'pong!'}, status=status.HTTP_200_OK)


class ModelView(ViewSet):
    """
    API for providing information of models provided by service

    available query options:
    - none: none
    """

    def retrieve(self, request, pk):
        for item in util.model_meta:
            if item.get('kind') == pk:
                return Response(item['instance'], status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        items = [item.get('instance') for item in util.model_meta]
        return Response({'results': items}, status=status.HTTP_200_OK)


class HistoryView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    """
    API for history listing purpose, no additional routes for it

    available query options:
    - model: string, filter histories with prediction model used
    """

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return HistorySerializer

        return PredictSerializer

    def get_queryset(self):
        queryset = History.objects.order_by('-id')

        # queries are applied only for list action
        if self.action != 'list':
            return queryset

        # filter with model it uses
        query = self.request.query_params
        model = query.get('model')
        if model and isinstance(model, str):
            queryset = queryset.filter(model=model)

        return queryset

    def perform_create(self, serializer):
        arg = self.request.data
        prediction = util.predict(arg['img'], model=arg['model'])
        serializer.save(prediction=prediction)
