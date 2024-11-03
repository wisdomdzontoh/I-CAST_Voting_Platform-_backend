from django.contrib import admin
from .models import (
    SubscriptionPlan,
    Organization,
    VotingSession,
    Position,
    Candidate,
    Voter,
    Ballot,
    Notification,
    Feedback,
    Report,
    AuditLog,
)

# Registering SubscriptionPlan model
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_sessions', 'max_voters_per_session', 'max_candidates_per_position')
    search_fields = ('name',)

# Registering Organization model
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'type')
    search_fields = ('name', 'email', 'phone_number')

# Registering VotingSession model
@admin.register(VotingSession)
class VotingSessionAdmin(admin.ModelAdmin):
    list_display = ('session_title', 'organization', 'start_date', 'end_date', 'is_active')
    search_fields = ('session_title',)
    list_filter = ('organization', 'is_active')

# Registering Position model
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session')
    search_fields = ('title',)

# Registering Candidate model
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name',)

# Registering Voter model
@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'email', 'has_voted', 'is_active')
    search_fields = ('voter_id', 'email')
    list_filter = ('has_voted', 'is_active')

# Registering Ballot model
@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'vote_casted_at')
    search_fields = ('voter__voter_id', 'candidate__name')

# Registering Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('voter', 'message', 'is_read', 'timestamp')
    search_fields = ('voter__voter_id', 'message')

# Registering Feedback model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('voter', 'session', 'rating', 'timestamp')
    search_fields = ('voter__voter_id', 'session__session_title')
    list_filter = ('rating',)

# Registering Report model
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('voting_session', 'total_voters', 'total_votes', 'created_at')
    search_fields = ('voting_session__session_title',)

# Registering AuditLog model
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'session', 'timestamp')
    search_fields = ('action', 'details')
