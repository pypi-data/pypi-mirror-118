from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q

from ...models import RssFeed

User = get_user_model()


class Command(BaseCommand):
    help = "Create / delete Podle rss feeds for users belonging to the PODLE_RSS_FEED_GROUP_NAME group"

    def handle(self, *args, **options):
        self.stdout.write("Start command create_or_delete_podle_rss_feeds...")

        # Create rss feeds for users belonging to the PODLE_RSS_FEED_GROUP_NAME group
        users_with_feed_to_create = User.objects.filter(
            groups__name=settings.PODLE_RSS_FEED_GROUP_NAME, rssfeed__isnull=True
        )
        count_users_with_feed_to_create = users_with_feed_to_create.count()
        RssFeed.objects.create_rss_feed(users_with_feed_to_create)

        self.stdout.write(
            f"{count_users_with_feed_to_create} rss feeds have been created"
        )

        # Delete rss feeds for users that do not belong to the PODLE_RSS_FEED_GROUP_NAME group
        users_with_feed_to_delete = User.objects.filter(
            ~Q(groups__name=settings.PODLE_RSS_FEED_GROUP_NAME), rssfeed__isnull=False
        )
        count_users_with_feed_to_delete = users_with_feed_to_delete.count()
        RssFeed.objects.delete_rss_feed(users_with_feed_to_delete)

        self.stdout.write(f"{count_users_with_feed_to_delete} rss feeds been deleted")

        self.stdout.write(
            "create_or_delete_podle_rss_feeds command finished successfully!"
        )
