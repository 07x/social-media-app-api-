# Generated by Django 5.0.3 on 2024-03-20 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customusermodel',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]