from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/', include('clients.urls')),
    path('api/v1/', include('machines.urls')),
    path('api/v1/', include('service_records.urls')),
    path('api/v1/', include('inventory.urls')),
    path('api/v1/', include('activity_logs.urls')),
    path('api/v1/', include('dashboard.urls')),
]
