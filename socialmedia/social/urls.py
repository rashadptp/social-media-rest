from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Post URLs
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # Comment URLs
    path('comments/', CommentListView.as_view(), name='comment-list'),
 
    # Like URLs
    path('likes/', LikeListView.as_view(), name='like-list'),
    
    # Follow URLs
    path('follows/', FollowListView.as_view(), name='follow-list'),
    # FEED 
    path('feed/',FeedView.as_view(),name='feed-list'),
    
    # User profile
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user-profile'),
]
