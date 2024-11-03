from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated', null=True, blank=True)

    class Meta:
        abstract = True

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    max_sessions = models.PositiveIntegerField()
    max_voters_per_session = models.PositiveIntegerField()
    max_candidates_per_position = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organization")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default=None)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    domain = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='organization_logo/', blank=True, null=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def can_create_session(self):
        """Check if the organization can create another session."""
        return self.sessions.count() < self.subscription_plan.max_sessions

class VotingSession(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="sessions")
    session_title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unique_id = models.CharField(max_length=12, unique=True, editable=False, default=get_random_string)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    allow_anonymous_voting = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = get_random_string(length=12)
        if not self.slug:
            self.slug = slugify(self.session_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.session_title} - {self.unique_id}"

class Position(BaseModel):
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name="positions")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Candidate(BaseModel):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="candidates")
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)

    def __str__(self):
        return self.name

class Voter(models.Model):
    voting_session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name="voters")
    email = models.EmailField(unique=True)
    voter_id = models.CharField(max_length=250)
    passcode = models.CharField(max_length=10, unique=True)
    has_voted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.voting_session.session_title} {self.voter_id} - {self.has_voted}"

class Ballot(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name="ballots")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="ballots")
    vote_casted_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.voter}: {self.message[:20]}..."

class Feedback(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='feedbacks')
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'session')

    def __str__(self):
        return f"Feedback from {self.voter} for {self.session}"

class Report(models.Model):
    voting_session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name='reports')
    total_voters = models.IntegerField()
    total_votes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.voting_session} - {self.total_voters} voters"

class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey(VotingSession, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    object_id = models.IntegerField()
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} - {self.timestamp}"
