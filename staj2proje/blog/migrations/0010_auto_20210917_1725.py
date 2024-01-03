# Generated by Django 3.2.6 on 2021-09-17 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_mesaj'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mesaj',
            options={'verbose_name_plural': 'Mesajlar'},
        ),
        migrations.RenameField(
            model_name='mesaj',
            old_name='mesaj',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='mesaj',
            old_name='tarih',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='mesaj',
            old_name='okundu',
            new_name='is_read',
        ),
        migrations.RenameField(
            model_name='mesaj',
            old_name='alici',
            new_name='recipient',
        ),
        migrations.RenameField(
            model_name='mesaj',
            old_name='gonderen',
            new_name='sender',
        ),
    ]
