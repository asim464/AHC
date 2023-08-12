from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register('roles', views.RoleViewSet, basename='role')
routers.register('complainant-types', views.ComplainantTypeViewSet, basename='complaint')
routers.register('martial-statuses', views.MartialStatusViewSet, basename='martial-status')
routers.register('categories', views.CategoryViewSet, basename='categories')
routers.register('serving-statuses', views.ServingStatusViewSet, basename='serving-status')
routers.register('cities', views.CityViewSet, basename='cities')
routers.register('corps', views.CorpsViewSet, basename='corp')

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('refresh', views.RefreshView.as_view()),
    path('current', views.CurrentUserView.as_view()),
    path('permissions', views.PermissionListView.as_view()),
    path('users-create-update', views.UserCreateUpdateView.as_view()),
]

urlpatterns += routers.urls
