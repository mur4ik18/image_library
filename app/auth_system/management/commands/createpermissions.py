from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from posts_collections.models import Collection


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def create_search_permission(self):
        content_type = ContentType.objects.get_for_model(Post)
        permission = Permission.objects.get_or_create(
            codename='can_search',
            name='Can use search',
            content_type=content_type,
        )
        return permission

    def create_can_send_writer(self):
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get_or_create(
            codename='send_collection',
            name='Can send collection for writer',
            content_type=content_type,
        )
        return permission
    
    def create_view_writers(self):
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get_or_create(
            codename='view_writers',
            name='Can view writers',
            content_type=content_type,
        )
        return permission

    def create_view_writers_queue(self):
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get_or_create(
            codename='view_writers_queue',
            name='Can view writers_queue',
            content_type=content_type,
        )
        return permission

    def create_view_writers_admin_queue(self):
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get_or_create(
            codename='view_writers_admin_queue',
            name='Can view writers_admin_queue',
            content_type=content_type,
        )
        return permission

    def handle(self, *args, **options):
        self.can_search = self.create_search_permission()[0]
        self.send_collection = self.create_can_send_writer()[0]
        self.view_writers = self.create_view_writers()[0]
        self.view_writers_admin_queue = self.create_view_writers_admin_queue()[0]
        self.create_view_writers = self.create_view_writers()[0]
        self.stdout.write(self.style.SUCCESS('Successfully create new permissions!'))