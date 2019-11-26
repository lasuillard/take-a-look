""" /api/serializers.py
    serializers for consistent and validated API data handling

"""
from rest_framework import serializers
from core.models import History


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = History
        fields = ['url', 'id', 'img', 'label', 'model', 'prediction']
