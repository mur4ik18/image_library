# Generated by Django 4.1 on 2023-04-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ai_text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=500)),
                ('ai_caption', models.TextField(blank=True, max_length=1000)),
                ('ai_description', models.TextField(blank=True, max_length=1000)),
            ],
        ),
    ]