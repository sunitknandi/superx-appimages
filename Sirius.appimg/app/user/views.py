from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserSerializerWithToken, ProfileSerializer
from .permissions import IsNotAuthenticated, ProfileExists
from .models import Profile


class UserCurrentView(APIView):

    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserCreateView(APIView):

    permission_classes = (IsNotAuthenticated, AllowAny)
    throttle_clasees = (AnonRateThrottle, ScopedRateThrottle,)
    throttle_scope = "register"

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileCreateView(generics.CreateAPIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated, ProfileExists)

    serializer_class = ProfileSerializer

    def post(self, request):
        try:
            profile = Profile.objects.create(
                user=request.user,
                picture=request.FILES["picture"],
                username=request.data["username"]
            )
            profile.favourite_genres.set(request.data["favourite_genres"])
            return Response(
                data=ProfileSerializer(profile).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({
                "message": str(e)
            })


class UserProfileView(generics.RetrieveUpdateAPIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    query_set = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request):
        try:
            profile = self.query_set.get(user=request.user)
            return Response(ProfileSerializer(profile).data)
        except Profile.DoesNotExist:
            return Response(
                data={
                    "message": "Profile for user {} does not exist".format(request.user)
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            profile = self.query_set.get(user=request.user)
            serializer = ProfileSerializer()
            updated_profile = serializer.update(profile, request.data)
            return Response(ProfileSerializer(updated_profile).data)
        except Profile.DoesNotExist:
            return Response(
                data={
                    "message": "Profile for user {} does not exist".format(request.user)
                },
                status=status.HTTP_404_NOT_FOUND
            )
