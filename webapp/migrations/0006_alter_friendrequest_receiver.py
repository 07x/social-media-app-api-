# Generated by Django 5.0.3 on 2024-03-23 13:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_friendrequest_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request_receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]