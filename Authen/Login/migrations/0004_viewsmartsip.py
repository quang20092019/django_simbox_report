# Generated by Django 2.1.15 on 2022-08-01 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0003_bookinstance'),
    ]

    operations = [
        migrations.CreateModel(
            name='viewsmartsip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('smartsip', 'View smartsip'),),
            },
        ),
    ]
