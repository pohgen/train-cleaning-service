# Generated by Django 5.1.3 on 2024-12-03 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cleaning", "0007_alter_train_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approval",
            name="status",
            field=models.BooleanField(),
        ),
    ]
