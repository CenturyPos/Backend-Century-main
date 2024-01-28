from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.newsletter.models import Newsletter
from apps.newsletter.utils import EmailNewsletter
from .serializer import NewsletterSerializer


class NewsletterViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Endpoint to handle requests to send newsletters."""

    queryset = Newsletter.objects.all()

    def get_serializer_class(self):
        if self.action == "newsletter":
            return NewsletterSerializer
        return NewsletterSerializer

    @extend_schema(
        description="Send newsletter",
        tags=["newsletter"],
        responses={status.HTTP_201_CREATED: NewsletterSerializer},
    )
    @action(methods=["post"], detail=False)
    def newsletter(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get("message")
            newsletter = Newsletter(
                message=message,
            )
            newsletter.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["delete"], detail=True)
    def delete_newsletter(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
        except Newsletter.DoesNotExist:
            return Response(
                {"message": "Newsletter not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        newsletter.delete()
        return Response(
            {"message": "Newsletter deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(methods=["post"], detail=True)
    def resend_newsletter(self, request, *args, **kwargs):
        newsletter = self.get_object()
        serializer = NewsletterSerializer(
            newsletter, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            # Send email
            email_dist = EmailNewsletter(newsletter=newsletter)
            email_dist.send_email_newsletter()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
