# Generated by Django 4.0 on 2022-02-01 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employ',
            old_name='fname',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='employ',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employ',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='employ',
            name='password',
        ),
        migrations.AddField(
            model_name='employ',
            name='employe',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
