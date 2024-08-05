from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Post, Comment, Like, Follow
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from .permissions import IsOwnerOrReadOnly

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'status': "success", 'message': 'User created successfully.', 'response_code': status.HTTP_201_CREATED, 'data': serializer.data})
        else:
            return Response({'status': "failed", 'message': 'User creation failed.', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'status': 'success', 'message': 'Login successful', 'response_code': status.HTTP_200_OK, 'data': {'token': token.key}})
            return Response({'status': 'failed', 'message': 'Invalid credentials', 'response_code': status.HTTP_401_UNAUTHORIZED})
        return Response({'status': 'failed', 'message': 'Validation error', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'status': "success", 'message': 'User retrieved successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'status': "success", 'message': 'User updated successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})
        else:
            return Response({'status': "failed", 'message': 'User update failed.', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': "success", 'message': 'User deleted successfully.', 'response_code': status.HTTP_204_NO_CONTENT, 'data': {}})

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().select_related('user').prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': "success", 'message': 'Posts retrieved successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'status': "success", 'message': 'Post created successfully.', 'response_code': status.HTTP_201_CREATED, 'data': serializer.data})
        else:
            return Response({'status': "failed", 'message': 'Post creation failed.', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().select_related('user').prefetch_related('comments', 'likes')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'status': "success", 'message': 'Post retrieved successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'status': "success", 'message': 'Post updated successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})
        else:
            return Response({'status': "failed", 'message': 'Post update failed.', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': "success", 'message': 'Post deleted successfully.', 'response_code': status.HTTP_204_NO_CONTENT, 'data': {}})

class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().select_related('user', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': "success", 'message': 'Comments retrieved successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'status': "success", 'message': 'Comment created successfully.', 'response_code': status.HTTP_201_CREATED, 'data': serializer.data})
        else:
            return Response({'status': "failed", 'message': 'Comment creation failed.', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})

class LikeListView(generics.ListCreateAPIView):
    queryset = Like.objects.all().select_related('user', 'post')
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': "success", 'message': 'Likes retrieved successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'status': "success", 'message': 'Like created successfully.', 'response_code': status.HTTP_201_CREATED, 'data': serializer.data})
        else:
            return Response({'status': "failed", 'message': 'Like creation failed.', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})

class FollowListView(generics.ListCreateAPIView):
    queryset = Follow.objects.all().select_related('follower', 'following')
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]  # Changed to IsAuthenticated for security

    def create(self, request, *args, **kwargs):
        # Ensure 'follower' and 'following' are included in the request data
        if 'follower' not in request.data or 'following' not in request.data:
            return Response({'status': 'failed', 'message': 'Follower and following IDs are required.', 'response_code': status.HTTP_400_BAD_REQUEST})

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'status': "success", 'message': 'Follow created successfully.', 'response_code': status.HTTP_201_CREATED, 'data': serializer.data})
        else:
            return Response({'status': "failed", 'message': 'Follow creation failed.', 'response_code': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        return Post.objects.filter(user__in=following_users).select_related('user').prefetch_related('comments', 'likes')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': "success", 'message': 'Feed retrieved successfully.', 'response_code': status.HTTP_200_OK, 'data': serializer.data})
