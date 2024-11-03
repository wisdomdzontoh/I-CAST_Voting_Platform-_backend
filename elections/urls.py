from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'subscription-plans', views.SubscriptionPlanViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'voting-sessions', views.VotingSessionViewSet)
router.register(r'positions', views.PositionViewSet)
router.register(r'candidates', views.CandidateViewSet)
router.register(r'voters', views.VoterViewSet)
router.register(r'ballots', views.BallotViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'feedbacks', views.FeedbackViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'audit-logs', views.AuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Registration
    path('register/', views.RegisterView.as_view(), name='register'),

    # JWT Login
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),

    # Refresh Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Logout
    path('logout/', views.LogoutView.as_view(), name='logout'),
]


