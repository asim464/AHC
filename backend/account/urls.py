from django.urls import path
from account import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register('users', views.GHQUserViewSet, basename='user')
routers.register('organizations', views.GHQOrganizationViewSet, basename='organization')
routers.register('hierarchies', views.HierarchyViewSet, basename='hierarchy')

urlpatterns = []

urlpatterns += routers.urls
