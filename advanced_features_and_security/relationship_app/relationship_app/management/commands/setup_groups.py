from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions'

    def handle(self, *args, **options):
        # Get permissions
        content_type = ContentType.objects.get_for_model(Book)
        
        can_view = Permission.objects.get(codename='can_view_book', content_type=content_type)
        can_create = Permission.objects.get(codename='can_create_book', content_type=content_type)
        can_edit = Permission.objects.get(codename='can_edit_book', content_type=content_type)
        can_delete = Permission.objects.get(codename='can_delete_book', content_type=content_type)

        # Create Viewers group
        viewers, created = Group.objects.get_or_create(name='Viewers')
        viewers.permissions.add(can_view)
        self.stdout.write(self.style.SUCCESS('Viewers group created/updated'))

        # Create Editors group
        editors, created = Group.objects.get_or_create(name='Editors')
        editors.permissions.add(can_view, can_create, can_edit)
        self.stdout.write(self.style.SUCCESS('Editors group created/updated'))

        # Create Admins group
        admins, created = Group.objects.get_or_create(name='Admins')
        admins.permissions.add(can_view, can_create, can_edit, can_delete)
        self.stdout.write(self.style.SUCCESS('Admins group created/updated'))
