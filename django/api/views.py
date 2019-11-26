""" /api/views.py
    simple function-based views and class-based viewsets for various APIs

"""
import json
import random
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import History
from .serializers import HistorySerializer


@api_view(['GET'])
def ping_pong(request):
    """
    This view always returns string 'pong!' with status code 200, That's all what it does.

    this view, 'ping' is made for purpose of health-check of backend API server.
    """
    return Response({'ping': 'pong!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def predict(request):
    """
    Process machine-learning processing for request
    """
    data = request.data
    image = data['image']
    model = data['model']

    # run prediction with machine learning
    if model == 'svm':
        prediction = 0
    elif model == 'cnn':
        prediction = 1
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    history = History.objects.create(
        img=image,
        label=data['label'],
        model=model,
        prediction=prediction
    )
    return Response(HistorySerializer(history, context={'request': request}).data,
                    status=status.HTTP_201_CREATED)


class ModelView(ViewSet):
    """
    API for providing information of models provided by service

    available query options:
    - none: none
    """
    data = json.load(open('ml-models.json'))

    def retrieve(self, request, pk):
        for item in self.data:
            if item.get('kind') == pk:
                return Response(item['instance'], status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        items = [item.get('instance') for item in self.data]
        return Response({'results': items}, status=status.HTTP_200_OK)


class HistoryView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    """
    API for history listing purpose, no additional routes for it

    available query options:
    - model: string, filter histories with prediction model used
    """
    serializer_class = HistorySerializer

    def get_queryset(self):
        queryset = History.objects.all()

        # queries are applied only for list action
        if self.action != 'list':
            return queryset

        # filter with model it uses
        query = self.request.query_params
        model = query.get('model')
        if model and isinstance(model, str):
            queryset.filter(model=model)

        return queryset
