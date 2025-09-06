from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import Subscriber, Campaign
from .serializers import SubscriberSerializer, SubscriberCreateSerializer, CampaignSerializer




class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('-created_at')
    serializer_class = SubscriberSerializer


    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriberCreateSerializer
        return SubscriberSerializer


    @action(detail=False, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request):
    # Accepts {"email": "..."} to unsubscribe
        email = request.data.get('email')
        if not email:
            return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sub = get_object_or_404(Subscriber, email__iexact=email)
            sub.is_active = False
            sub.save()
            return Response({'status': 'unsubscribed', 'email': sub.email})
        except Subscriber.DoesNotExist:
            return Response({'error': 'subscriber not found'}, status=status.HTTP_404_NOT_FOUND)      



class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('-published_date')
    serializer_class = CampaignSerializer


# Simple API endpoint to call unsubscribe via GET if preferred
@api_view(['GET'])
def unsubscribe_get(request):
    email = request.query_params.get('email')
    if not email:
        return Response({'error': 'email required'}, status=status.HTTP_400_BAD_REQUEST)
        sub = get_object_or_404(Subscriber, email__iexact=email)
        sub.is_active = False
        sub.save()
    return Response({'status': 'unsubscribed', 'email': sub.email})