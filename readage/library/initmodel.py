from django.contrib.contenttypes.models import ContentType
from library.models import *

dummy_type = ContentType.objects.get(model='myuser')
NormalUser = Group.objects.create(name='NormalUser')
AdvancedUser = Group.objects.create(name='AdvancedUser')
Blacklist = Group.objects.create(name='Blacklist')
Admin = Group.objects.create(name='Admin')
comment = Permission.objects.create(
    codename='can_comment', name='can comment', content_type=dummy_type
    )
manage = Permission.objects.create(
    codename='can_manage', name='can manage', content_type=dummy_type
    )
search = Permission.objects.create(
    codename='can_search', name='can search', content_type=dummy_type
    )
NormalUser.permissions = [comment, search]
AdvancedUser.permissions = [comment, search]
Blacklist.permissions = [comment, search]
Admin.permissions = [comment, search, manage]
root = User.objects.create_superuser(
    username='root', password='root', email='root@root.com'
    )
