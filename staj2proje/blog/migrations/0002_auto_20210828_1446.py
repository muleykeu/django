# Generated by Django 3.2.6 on 2021-08-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(height_field=80, upload_to='', width_field=80),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=700),
        ),
    ]