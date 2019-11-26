""" /api/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'model', views.ModelView, basename='model')
router.register(r'history', views.HistoryView, basename='history')

urlpatterns = [
    path('ping/', views.ping_pong),
    path('predict/', views.predict),
    path('', include(router.urls))
]
