# Generated by Django 2.0 on 2017-12-14 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yyfeed', '0003_auto_20170107_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='link',
            field=models.URLField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='feeditem',
            name='link',
            field=models.URLField(max_length=4000),
        ),
    ]
