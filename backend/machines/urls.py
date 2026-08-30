from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, AssignmentViewSet
router = DefaultRouter(); router.register('machines', MachineViewSet); router.register('assignments', AssignmentViewSet, basename='assignments')
urlpatterns = [path('', include(router.urls))]
