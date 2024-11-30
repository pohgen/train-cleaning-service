from django.db import models


class Train(models.Model):
    class Status(models.TextChoices):
        AWAITS = "awaits cleaning", "Awaits cleaning"
        IN_PROGRESS = "in progress", "Cleaning in progress"
        COMPLETED = "completed", "Cleaning is completed"
        APPROVED = "approved", "Cleaning is approved"
        CANCELED = "canceled", "Cleaning is canceled"

    cleaning_type = models.ForeignKey("CleaningType", on_delete=models.CASCADE)
    status = models.CharField(max_length=31, choices=Status.choices, default=Status.AWAITS)
    workers = models.ManyToManyField("Worker", related_name="trains")
    approval = models.ForeignKey("Approval", on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class CleaningType(models.Model):
    class Title(models.TextChoices):
        SP0 = "SP0", "SP0"
        SP1 = "SP1", "SP1"
        SP2 = "SP2", "SP2"

    title = models.CharField(max_length=3, choices=Title.choices, default="Null")
    description = models.TextField(null=True, blank=True)


class Approval(models.Model):
    worker = models.ForeignKey("Worker", on_delete=models.CASCADE, related_name="approvals")
    status = models.BooleanField()
    comments = models.TextField(null=True, blank=True)
