# Generated by Django 5.1.3 on 2024-12-02 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0005_alter_train_cleaning_type_delete_cleaningtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='approval',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cleaning.approval'),
        ),
    ]
