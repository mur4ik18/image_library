# Generated by Django 4.1 on 2023-04-03 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_edited_data_post_tags_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='website',
            field=models.CharField(blank=True, default='0', max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]