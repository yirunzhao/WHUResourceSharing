# Generated by Django 2.2.5 on 2019-12-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whursauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tagresourcelink',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='tagresourcelink',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='tagresourcelink',
            name='tag_name',
        ),
        migrations.AddField(
            model_name='resource',
            name='department',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='resource',
            name='year',
            field=models.IntegerField(default=2019),
        ),
        migrations.AlterField(
            model_name='resource',
            name='download_count',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='TagList',
        ),
        migrations.DeleteModel(
            name='TagResourceLink',
        ),
    ]
