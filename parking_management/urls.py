from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientRegistrationView, ClientLoginView, ClientLogoutView, ParkingUserViewSet

router = DefaultRouter()
router.register(r'parking-users', ParkingUserViewSet, basename='parking-users')

urlpatterns = [
    path('register/', ClientRegistrationView.as_view(), name='register'),
    path('login/', ClientLoginView.as_view(), name='login'),
    path('logout/', ClientLogoutView.as_view(), name='logout'),
    # Include CRUD functionality for parking users.
    path('', include(router.urls)),
    # Include DRF browsable API login/logout views.
    path('api-auth/', include('rest_framework.urls')),
]