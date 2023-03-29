from .models import LandingPage
from .serializers import LandingPageSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from trainings.models import Trainings


class LandingPageViewSet(viewsets.ModelViewSet):
    serializer_class = LandingPageSerializer
    queryset = LandingPage.objects.all()


class LandingPageStatisticView(APIView):
    def get(self, request, *args, **kwargs):

        region_count = 0
        for i in range(7):
            region_count += (User.objects.filter(region=(i+1)).count() != 0)

        data = {
            'user_count': User.objects.filter(is_staff=False, is_mentor=False).count(),
            'region_count': region_count,
            'trainings_count': Trainings.objects.all().count()
        }

        return Response(data)
