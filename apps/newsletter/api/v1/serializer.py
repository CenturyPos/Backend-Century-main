from rest_framework import serializers
from ...models import Newsletter
from ...utils import EmailNewsletter

class NewsletterSerializer(serializers.ModelSerializer):
    email = serializers.ListField(child=serializers.EmailField())

    class Meta:
        model = Newsletter
        fields = (
            "email",
            "message",
            "title"
        )

    def create(self, validated_data):
        # Extract and remove the 'email' field from the validated_data
        email_list = validated_data.pop('email', [])

        # Create the Newsletter instance
        instance = Newsletter.objects.create(**validated_data)

        # Iterate over the email list and send the email to each recipient
        for email in email_list:
            # Create a new instance for each email address
            instance.email = email
            # Send email
            email_dist = EmailNewsletter(newsletter=instance)
            email_dist.send_email_newsletter()

        return instance
