# Generated by Django 5.1.2 on 2024-11-02 17:04

import django.core.validators
import django.db.models.deletion
import django.utils.crypto
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('max_sessions', models.PositiveIntegerField()),
                ('max_voters_per_session', models.PositiveIntegerField()),
                ('max_candidates_per_position', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('voter_id', models.CharField(max_length=250)),
                ('passcode', models.CharField(max_length=10, unique=True)),
                ('has_voted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='candidates/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='elections.position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('domain', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='organization_logo/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to=settings.AUTH_USER_MODEL)),
                ('subscription_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.subscriptionplan')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='elections.voter')),
            ],
        ),
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_casted_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballots', to='elections.candidate')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballots', to='elections.voter')),
            ],
        ),
        migrations.CreateModel(
            name='VotingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('unique_id', models.CharField(default=django.utils.crypto.get_random_string, editable=False, max_length=12, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, unique=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('allow_anonymous_voting', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='elections.organization')),
            ],
        ),
        migrations.AddField(
            model_name='voter',
            name='voting_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='elections.votingsession'),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_voters', models.IntegerField()),
                ('total_votes', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('voting_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='elections.votingsession')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='elections.votingsession'),
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.IntegerField()),
                ('details', models.TextField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.votingsession')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='elections.voter')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='elections.votingsession')),
            ],
            options={
                'unique_together': {('voter', 'session')},
            },
        ),
    ]
