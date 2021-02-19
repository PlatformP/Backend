from rest_framework import serializers

from apps.email_signup.models.email import email


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = email
        fields = ['id', 'email']
