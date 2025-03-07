# Generated by Django 4.2.4 on 2023-08-08 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='position',
            new_name='account',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True),
        ),
    ]
