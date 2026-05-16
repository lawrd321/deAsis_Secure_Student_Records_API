from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from records.views import StudentRecordViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

# This creates all the standard web routes automatically
router = DefaultRouter()
router.register(r'student-records', StudentRecordViewSet, basename='studentrecord')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This URL is where users go to get their JWT Token (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # This URL is where the student records live
    path('api/', include(router.urls)),
]