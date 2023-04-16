from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from posts_collections.models import Collection
 # For now only view permission by default for all, others include add, delete, change

class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        self.writer()
        self.manager()
        self.curator()
        self.stdout.write(self.style.SUCCESS('Successfully create groups!'))

    def writer(self, *args, **optons):
        new_group, created = Group.objects.get_or_create(name='writer')

        ids = [
            'view_writers',
            'view_post'
        ]
        for i in ids:
            for obj in Permission.objects.filter(codename=i):
                new_group.permissions.add(obj)
        print("Created writer group and permissions.")
    
    def manager(self):
        new_group, created = Group.objects.get_or_create(name='manager')
        ids = [
            'add_non_approved',
            'change_non_approved',
            'delete_non_approved',
            'view_non_approved',
            'add_post',
            'can_search',
            'change_post',
            'delete_post',
            'view_post',
            'add_tag',
            'change_tag',
            'delete_tag',
            'view_tag',
            'add_collection',
            'change_collection',
            'delete_collection',
            'send_collection',
            'view_collection',
            'view_writers',
            'view_writers_admin_queue',
            'add_tag',
            'change_tag',
            'delete_tag',
            'view_tag',
            ]
        for i in ids:
            for obj in Permission.objects.filter(codename=i):
                new_group.permissions.add(obj)

        print("Created manager group and permissions.")

    def curator(self):
        new_group, created = Group.objects.get_or_create(name='curator')
        ids = [
            'can_search',
            'view_post',
            'add_tag',
            'delete_tag',
            'view_tag',
            'change_collection',
            'view_collection',
            'add_tag',
            'change_tag',
            'delete_tag',
            'view_tag',
            ]
        for i in ids:
            
            for obj in Permission.objects.filter(codename=i):
                new_group.permissions.add(obj)
        new_group, created = Group.objects.get_or_create(name='curator')
        print("Created curator group and permissions.")
