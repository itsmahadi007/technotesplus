# Generated by Django 3.2.6 on 2021-08-15 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_notes_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]