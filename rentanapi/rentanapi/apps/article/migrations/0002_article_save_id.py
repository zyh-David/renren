# Generated by Django 2.2 on 2020-01-16 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='save_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='编辑次数'),
        ),
    ]
