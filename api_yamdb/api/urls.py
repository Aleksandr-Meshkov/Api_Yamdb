from django.urls import include, path

from rest_framework import routers

from .views import (UserViewSet, send_confirmation_code, get_token_for_user
                    CommentViewSet, ReviewViewSet)

router_api_v1 = routers.DefaultRouter()

router_api_v1.register('users', UserViewSet, basename='users')

router_api_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                       ReviewViewSet, basename='reviews')
router_api_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                       r'/comments', CommentViewSet, basename='comments')



urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_token_for_user),
]
