# Generated by Django 4.0 on 2022-01-29 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_caption_alter_post_hashtags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='imagines/images/'),
        ),
    ]
