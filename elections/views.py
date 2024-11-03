from rest_framework import viewsets, status, permissions, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import (
    Organization, SubscriptionPlan, VotingSession, Position,
    Candidate, Voter, Ballot, Notification, Feedback, Report, AuditLog
)
from .serializers import (
    OrganizationSerializer, SubscriptionPlanSerializer, VotingSessionSerializer,
    PositionSerializer, CandidateSerializer, VoterSerializer, BallotSerializer,
    NotificationSerializer, FeedbackSerializer, ReportSerializer, AuditLogSerializer
)

# Serializer for User Registration
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Register API
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API (JWT)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

# Logout API
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class IsCreatorOrReadOnly(permissions.BasePermission):
    """Custom permission class to allow only the creator to modify or delete an object."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow safe methods for everyone
        return obj.created_by == request.user  # Only allow creator to modify/delete

class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset with common permissions and query filtering."""
    
    permission_classes = [IsCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SubscriptionPlanViewSet(BaseViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(organizations__created_by=self.request.user)

class OrganizationViewSet(BaseViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        if self.queryset.filter(created_by=self.request.user).exists():
            raise ValidationError("You can only create one organization.")
        super().perform_create(serializer)

class VotingSessionViewSet(BaseViewSet):
    queryset = VotingSession.objects.all()
    serializer_class = VotingSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(organization__created_by=self.request.user)

class PositionViewSet(BaseViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)

class CandidateViewSet(BaseViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)

class VoterViewSet(BaseViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)

class BallotViewSet(BaseViewSet):
    queryset = Ballot.objects.all()
    serializer_class = BallotSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)

class NotificationViewSet(BaseViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)

class FeedbackViewSet(BaseViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)

class ReportViewSet(BaseViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)

class AuditLogViewSet(BaseViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(voting_session__organization__created_by=self.request.user)
