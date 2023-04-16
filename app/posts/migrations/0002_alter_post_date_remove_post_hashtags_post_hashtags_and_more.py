# Generated by Django 4.0 on 2022-01-17 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.RemoveField(
            model_name='post',
            name='hashtags',
        ),
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='post',
            name='unique_field',
            field=models.CharField(default='<django.db.models.fields.CharField>_<django.db.models.fields.CharField>', max_length=500, unique=True),
        ),
        migrations.DeleteModel(
            name='Hashtag',
        ),
    ]