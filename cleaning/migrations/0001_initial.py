# Generated by Django 5.1.3 on 2024-11-30 16:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CleaningType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[("SP0", "SP0"), ("SP1", "SP1"), ("SP2", "SP2")],
                        default="Null",
                        max_length=3,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Approval",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField()),
                ("comments", models.TextField(blank=True, null=True)),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "worker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approvals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Train",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("awaits cleaning", "Awaits cleaning"),
                            ("in progress", "Cleaning in progress"),
                            ("completed", "Cleaning is completed"),
                            ("approved", "Cleaning is approved"),
                            ("canceled", "Cleaning is canceled"),
                        ],
                        default="awaits cleaning",
                        max_length=31,
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "approval",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cleaning.approval",
                    ),
                ),
                (
                    "cleaning_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cleaning.cleaningtype",
                    ),
                ),
                (
                    "workers",
                    models.ManyToManyField(
                        related_name="trains", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
