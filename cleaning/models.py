from django.db import models


class Train(models.Model):
    class Status(models.TextChoices):
        AWAITS = "awaits cleaning", "Awaits cleaning"
        IN_PROGRESS = "in progress", "Cleaning in progress"
        COMPLETED = "completed", "Cleaning is completed"
        APPROVED = "approved", "Cleaning is approved"
        CANCELED = "canceled", "Cleaning is canceled"

    name = models.CharField(max_length=6)
    cleaning_type = models.ForeignKey("CleaningType", on_delete=models.CASCADE)
    status = models.CharField(max_length=31, choices=Status.choices, default=Status.AWAITS)
    workers = models.ManyToManyField("accounts.Worker", related_name="trains")
    approval = models.ForeignKey("Approval", on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class CleaningType(models.Model):
    class Title(models.TextChoices):
        SP0 = "SP0", "SP0"
        SP1 = "SP1", "SP1"
        SP2 = "SP2", "SP2"

    title = models.CharField(max_length=3, choices=Title.choices, default="Null")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Approval(models.Model):
    worker = models.ForeignKey("accounts.Worker", on_delete=models.CASCADE, related_name="approvals")
    status = models.BooleanField(null=True)
    comments = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status