from actstream import action
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Task(models.Model):
    subject = models.CharField(max_length=100)

    content = models.TextField(null=False)

    created_by = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.RESTRICT,
        related_name="tasks_created_by",
    )
    created_on = models.DateTimeField(null=False, blank=True)

    modified_by = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.RESTRICT,
        related_name="tasks_modified_by",
    )
    modified_on = models.DateTimeField(null=False, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50)  # UUID as well as INTs
    content_object = GenericForeignKey("content_type", "object_id")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.created_on:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.subject


@receiver(post_save, sender=Task, dispatch_uid="task_save")
def update_stock(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.created_by,
            verb="created",
            action_object=instance,
            target=instance.content_object,
        )
    else:
        action.send(
            instance.modified_by,
            verb="changed",
            action_object=instance,
            target=instance.content_object,
        )
