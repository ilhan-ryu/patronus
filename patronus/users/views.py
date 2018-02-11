from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers
from patronus.notifications import views as notification_views

class ExplorerUsers(APIView):

    def get(self, request, format=None):

        last_five = models.User.objects.all().order_by('-date_joined')[:5]

        serializer = serializers.ListUserSerializers(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FollowUsers(APIView):

    def post(self, request, user_id, format=None):

        user = request.user
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user.save()

        notification_views.create_notification(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)

class UnFollowUsers(APIView):

    def post(self, request, user_id, format=None):

        user = request.user
        print (user)
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)
        user.save()

        return Response(status=status.HTTP_200_OK)

class UserProfile(APIView):

    def get_user(self, username):
        
        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None

    def get(self, request, username, format=None):

        found_user = self.get_user(username)
        
        if not found_user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):

        user = request.user
        found_user = self.get_user(username)
        
        if not found_user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        elif found_user.username != user.username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            serializer = serializers.UserProfileSerializer(found_user, data=request.data, partial=True)

            if serializer.is_valid():
            
                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserFollowers(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()

        serializer = serializers.ListUserSerializers(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserFollowing(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()

        serializer = serializers.ListUserSerializers(user_following, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Search(APIView):

    def get(self, request, format=None):

        username = request.query_params.get('username', None)

        if username and len(username) >= 2:
            users = models.User.objects.filter(username__icontains=username)

            serializer = serializers.ListUserSerializers(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)