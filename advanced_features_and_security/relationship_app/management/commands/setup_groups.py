from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from LibraryProject.bookshelf.models import Book  # Updated import

class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions for book management'

    def handle(self, *args, **options):
        # Get the content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get all the custom permissions we defined
        try:
            can_view = Permission.objects.get(codename='can_view', content_type=content_type)
            can_create = Permission.objects.get(codename='can_create', content_type=content_type)
            can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
            can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permissions not found. Please run migrations first.'))
            return

        # Create Viewers group - can only view books
        viewers, created = Group.objects.get_or_create(name='Viewers')
        viewers.permissions.set([can_view])
        if created:
            self.stdout.write(self.style.SUCCESS('Viewers group created'))
        else:
            self.stdout.write(self.style.SUCCESS('Viewers group updated'))

        # Create Editors group - can view, create, and edit books
        editors, created = Group.objects.get_or_create(name='Editors')
        editors.permissions.set([can_view, can_create, can_edit])
        if created:
            self.stdout.write(self.style.SUCCESS('Editors group created'))
        else:
            self.stdout.write(self.style.SUCCESS('Editors group updated'))

        # Create Admins group - can do everything
        admins, created = Group.objects.get_or_create(name='Admins')
        admins.permissions.set([can_view, can_create, can_edit, can_delete])
        if created:
            self.stdout.write(self.style.SUCCESS('Admins group created'))
        else:
            self.stdout.write(self.style.SUCCESS('Admins group updated'))

        self.stdout.write(self.style.SUCCESS('\nGroups created successfully!'))
