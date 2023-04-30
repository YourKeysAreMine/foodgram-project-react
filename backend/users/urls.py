from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet,
                    SubscriptionViewSet,
                    ShowSubscriptionsViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    'users',
    CustomUserViewSet,
    basename='users'
)
router_v1.register(
    r'users/(?P<user_id>\d+)/subscribe', SubscriptionViewSet,
    basename='subscribe')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
            'users/subscriptions/', ShowSubscriptionsViewSet.as_view(),
            name='subscriptions'
        ),
]
