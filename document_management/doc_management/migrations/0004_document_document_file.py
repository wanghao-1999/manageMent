# Generated by Django 4.2.4 on 2023-08-07 22:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('doc_management', '0003_alter_document_document_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_file',
            field=models.FileField(default=django.utils.timezone.now, upload_to='documents/'),
            preserve_default=False,
        ),
    ]
