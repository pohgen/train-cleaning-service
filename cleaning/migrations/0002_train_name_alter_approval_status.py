# Generated by Django 5.1.3 on 2024-11-30 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cleaning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="train",
            name="name",
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="approval",
            name="status",
            field=models.BooleanField(null=True),
        ),
    ]
