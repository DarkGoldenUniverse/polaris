from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from account.v2.serializers import UserSerializer


class UserDetailApiView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
