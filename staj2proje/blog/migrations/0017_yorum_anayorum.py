# Generated by Django 3.2.6 on 2021-09-22 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='yorum',
            name='anayorum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.yorum'),
        ),
    ]
