# Generated by Django 3.2 on 2023-08-14 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ds_app', '0005_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='ds_app.project'),
            preserve_default=False,
        ),
    ]
