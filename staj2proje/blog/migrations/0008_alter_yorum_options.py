# Generated by Django 3.2.6 on 2021-09-14 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_yorum'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yorum',
            options={'verbose_name_plural': 'Yorumlar'},
        ),
    ]
