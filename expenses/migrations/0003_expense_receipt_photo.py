# Generated by Django 5.1.6 on 2025-03-07 00:47

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_remove_expense_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='receipt_photo',
            field=models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='./photos'), upload_to=''),
        ),
    ]
