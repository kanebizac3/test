# Generated by Django 5.1.7 on 2025-04-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='good',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='評価'),
        ),
        migrations.AddField(
            model_name='comments',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
        migrations.AddField(
            model_name='post',
            name='good',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='評価'),
        ),
    ]
