from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SubscriberViewSet, CampaignViewSet, unsubscribe_get


router = DefaultRouter()
router.register(r'subscribers', SubscriberViewSet, basename='subscriber')
router.register(r'campaigns', CampaignViewSet, basename='campaign')


urlpatterns = [
    path('', include(router.urls)),
    path('unsubscribe/', unsubscribe_get, name='unsubscribe-get'),
]