from django.db import models


class ActiveMixIn(models.Model):
    """
    A mixin that allows you to automatically add the user that has created, delete or updated a particular model.
    We use "arrow" to convert models
    """
    class Meta:
        abstract = True

    active = models.BooleanField(default=True, help_text="If set, the row should be included in whatever queryset generated")