from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Form
from .serializers import (
    FormParlerSerializer,
    FormReadOnlySerializer,
    FormCreateUpdateSerializer,
)


class FormParlerViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ["get", "list", "retrieve"]:
            return FormParlerSerializer
        return FormCreateUpdateSerializer
