# Generated by Django 5.1.7 on 2025-04-08 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_comments_good'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='good',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='評価'),
        ),
    ]
