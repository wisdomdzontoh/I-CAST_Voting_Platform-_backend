from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Register API
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API (JWT)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

# Logout API
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Custom Permissions
class IsCreatorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow creators to modify or delete objects."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow safe methods for everyone
        return obj.user == request.user  # Only allow creator to modify/delete

# Base ViewSet for common functionality
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCreatorOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)  # Filter by logged-in user

# Organization Views
class OrganizationViewSet(BaseViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user to the logged-in user before saving
        serializer.save(user=self.request.user)

# Subscription Plan Views
class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):  # Use ReadOnlyModelViewSet if only read operations are needed
    queryset = SubscriptionPlan.objects.all()  # Keep the queryset accessible for all
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return all subscription plans without filtering by user
        return self.queryset.all()

# Voting Session Views
class VotingSessionViewSet(BaseViewSet):
    queryset = VotingSession.objects.all()
    serializer_class = VotingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

# Position Views
class PositionViewSet(BaseViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]

# Candidate Views
class CandidateViewSet(BaseViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

# Voter Views
class VoterViewSet(BaseViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    permission_classes = [permissions.IsAuthenticated]

# Ballot Views
class BallotViewSet(BaseViewSet):
    queryset = Ballot.objects.all()
    serializer_class = BallotSerializer
    permission_classes = [permissions.IsAuthenticated]

# Notification Views
class NotificationViewSet(BaseViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Feedback Views
class FeedbackViewSet(BaseViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

# Report Views
class ReportViewSet(BaseViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

# Audit Log Views
class AuditLogViewSet(BaseViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
