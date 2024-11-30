from django.db import models
from django.db.models import ForeignKey, CASCADE, CharField, ManyToManyField, SET_NULL, DateTimeField, TextField, \
    BooleanField


class Train(models.Model):
    class Status(models.TextChoices):
        AWAITS = "awaits cleaning", "Awaits cleaning"
        IN_PROGRESS = "in progress", "Cleaning in progress"
        COMPLETED = "completed", "Cleaning is completed"
        APPROVED = "approved", "Cleaning is approved"
        CANCELED = "canceled", "Cleaning is canceled"

    cleaning_type = ForeignKey("CleaningType", on_delete=CASCADE)
    status = CharField(max_length=31, choices=Status.choices, default=Status.AWAITS)
    workers = ManyToManyField("Worker", related_name="trains")
    approval = ForeignKey("Approval", on_delete=SET_NULL, null=True)
    start_time = DateTimeField()
    end_time = DateTimeField()


class CleaningType(models.Model):
    class Title(models.TextChoices):
        SP0 = "SP0", "SP0"
        SP1 = "SP1", "SP1"
        SP2 = "SP2", "SP2"

    title = CharField(max_length=3, choices=Title.choices, default="Null")
    description = TextField(null=True, blank=True)


class Approval(models.Model):
    worker = ForeignKey("Worker", on_delete=CASCADE, related_name="approvals")
    status = BooleanField()
    comments = TextField(null=True, blank=True)
