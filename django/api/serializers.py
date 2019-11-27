""" /api/serializers.py
    serializers for consistent and validated API data handling

"""
from rest_framework import serializers
from core.models import History


class PredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'img', 'label', 'model', 'prediction']
        read_only_fields = ('prediction', )


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = History
        fields = ['url', 'id', 'img', 'label', 'model', 'prediction']
