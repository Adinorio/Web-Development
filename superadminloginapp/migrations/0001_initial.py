# Generated by Django 5.2.1 on 2025-06-03 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('password_changed_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
