import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .podle import PodleHelper

logger = logging.getLogger(__name__)


class NewsletterManager(models.Manager):
    def create_or_update_newsletter(self, instance, json_content):
        content_type = ContentType.objects.get_for_model(instance._meta.model)
        object_id = instance.id

        try:
            newsletter = self.get(content_type=content_type, object_id=object_id)
        except self.model.DoesNotExist:
            response = PodleHelper().create_newsletter(json_content)
            logger.debug(response)
            newsletter_id = response["id"]
            return self.create(
                content_type=content_type, object_id=object_id, uuid=newsletter_id
            )

        # If we update the newsletter, it is best to reuse the newsletter uuid
        json_content["newsletterId"] = str(newsletter.uuid)
        PodleHelper().create_newsletter(json_content)
        return newsletter


class RssFeedManager(models.Manager):
    def get_rss_feed(self, user):
        try:
            return self.get(user=user).feed
        except self.model.DoesNotExist:
            return None

    def create_rss_feed(self, users):
        for batch_users in self._chunked_queryset(users):
            data = {
                "subscribers": [
                    {
                        "subscriberId": user.pk,
                        "newsletterName": settings.PODLE_NEWSLETTER_NAME,
                    }
                    for user in batch_users
                ]
            }

            response = PodleHelper().create_batch_private_rss(data)

            # Format the response and bulk update or create the Rss feed objects for RssFeed model
            objs = []
            for obj in response:
                rss_feed, _ = self.update_or_create(
                    user_id=list(obj)[0], defaults={"feed": list(obj.values())[0]}
                )
                objs.append(rss_feed)

            self.bulk_update(objs, ["user_id", "feed"])

    def delete_rss_feed(self, users):
        for batch_users in self._chunked_queryset(users):
            data = {
                "subscribers": [
                    {
                        "subscriberId": user.pk,
                        "newsletterName": settings.PODLE_NEWSLETTER_NAME,
                    }
                    for user in batch_users
                ]
            }

            response = PodleHelper().delete_batch_private_rss(data)

            # Delete the Rss feed objects from RssFeed model
            user_ids = []
            for obj in response:
                user_ids.append(list(obj)[0])

            qs = self.filter(user_id__in=user_ids)

            # We use _raw_delete as we don't want to trigger the signals when bulk deleting.
            # We couldn't find a better way to do it as for now.
            qs._raw_delete(qs.db)

    @staticmethod
    def _chunked_queryset(queryset, chunk_size=200):
        """Slice a queryset into chunks."""

        start_pk = 0
        queryset = queryset.order_by("pk")

        while True:
            # No entry left
            if not queryset.filter(pk__gt=start_pk).exists():
                break

            try:
                # Fetch chunk_size entries if possible
                end_pk = queryset.filter(pk__gt=start_pk).values_list("pk", flat=True)[
                    chunk_size - 1
                ]

                # Fetch rest entries if less than chunk_size left
            except IndexError:
                end_pk = queryset.values_list("pk", flat=True).last()

            yield queryset.filter(pk__gt=start_pk).filter(pk__lte=end_pk)

            start_pk = end_pk
