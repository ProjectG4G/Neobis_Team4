from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Form
from .serializers import FormParlerSerializer


class FormParlerViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormParlerSerializer
    permission_classes = (AllowAny,)
