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
    AuditLog
)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_sessions', 'max_voters_per_session', 'max_candidates_per_position')
    search_fields = ('name',)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_type', 'email', 'address', 'phone_number', 'subscription_plan')
    search_fields = ('name', 'email', 'address')
    list_filter = ('organization_type', 'subscription_plan')

class VotingSessionAdmin(admin.ModelAdmin):
    list_display = ('session_title', 'organization', 'start_date', 'end_date', 'is_active')
    search_fields = ('session_title',)
    list_filter = ('is_active', 'organization')

class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session')
    search_fields = ('title',)
    list_filter = ('session',)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name',)
    list_filter = ('position',)

class VoterAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'email', 'voting_session', 'has_voted', 'is_active')
    search_fields = ('voter_id', 'email')
    list_filter = ('voting_session', 'has_voted', 'is_active')

class BallotAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'vote_casted_at')
    search_fields = ('voter__voter_id', 'candidate__name')
    list_filter = ('voter', 'candidate')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('voter', 'message', 'is_read', 'timestamp')
    search_fields = ('message',)
    list_filter = ('is_read', 'voter')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('voter', 'session', 'rating', 'timestamp')
    search_fields = ('voter__voter_id', 'session__session_title')
    list_filter = ('session', 'rating')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('voting_session', 'total_voters', 'total_votes', 'created_at')
    search_fields = ('voting_session__session_title',)
    list_filter = ('voting_session',)

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'session', 'timestamp', 'object_id')
    search_fields = ('action', 'details')
    list_filter = ('user', 'session')

# Registering the models with their respective Admin classes
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(VotingSession, VotingSessionAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Ballot, BallotAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(AuditLog, AuditLogAdmin)
