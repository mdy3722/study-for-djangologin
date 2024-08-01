# Generated by Django 5.0.7 on 2024-07-26 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acccounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(default='default_nickname', max_length=30, unique=True),
        ),
    ]
