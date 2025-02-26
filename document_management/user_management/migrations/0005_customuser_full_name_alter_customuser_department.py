# Generated by Django 4.2.4 on 2023-08-09 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_remove_customuser_account_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.department'),
        ),
    ]
