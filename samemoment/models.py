from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

# Data model for a post on our social website.
class Post(models.Model):
    text = models.CharField(max_length=160)
    user = models.ForeignKey(User, default=None)
    create_time =models.DateTimeField(auto_now=False, auto_now_add=True)
    ip_addr = models.GenericIPAddressField()

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '", create time="' + self.create_time + '"'
