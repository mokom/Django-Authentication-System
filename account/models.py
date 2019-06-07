from uuid import uuid4

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def profile_photo_directory_with_uuid(instance, filename):
    return '{}/{}'.format(instance.id, uuid4())

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null='True')
    photo = models.ImageField(upload_to=profile_photo_directory_with_uuid, blank=True)
    following = models.ManyToManyField('self', through='Contact', related_name='followers', symmetrical=False)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class Contact(models.Model):
    user_from = models.ForeignKey(Profile, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(Profile, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)
