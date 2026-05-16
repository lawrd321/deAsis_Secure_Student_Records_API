from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from .models import StudentRecord
from .serializers import StudentRecordSerializer

# CUSTOM RULE: Checks if the user is in the Admin or Faculty group
class IsAdminOrFaculty(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Admin', 'Faculty']).exists()

class StudentRecordViewSet(ModelViewSet):
    serializer_class = StudentRecordSerializer

    # RULE: Students view only their own record. Admins/Faculty view all.
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists() or user.is_superuser:
            return StudentRecord.objects.all()
        return StudentRecord.objects.filter(owner=user)

    # RULE: Admins can create/delete. Faculty can update. Everyone else must be logged in.
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser] # Only Admins
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrFaculty] # Admins or Faculty
        else:
            permission_classes = [IsAuthenticated] # Students (just viewing)
        
        return [permission() for permission in permission_classes]