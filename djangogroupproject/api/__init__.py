from rest_framework import serializers
from campaigns.models import Campaign
from organizations.models import Organization
from donations.models import Donation
from tags.models import Tag
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class OrganizationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Organization
        fields = ['id', 'name', 'owner']

class CampaignSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Campaign
        fields = ['id', 'title', 'organization', 'goal_amount', 'current_amount', 'status', 'tags']

class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'user', 'campaign', 'amount', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']