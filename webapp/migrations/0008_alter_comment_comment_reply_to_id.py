# Generated by Django 3.2 on 2024-04-01 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_alter_friendlist_friend_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_reply_to_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reply_id', to='webapp.comment'),
        ),
    ]
