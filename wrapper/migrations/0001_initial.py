# Generated by Django 4.2.1 on 2023-05-14 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serv_name', models.CharField(max_length=50)),
                ('serv_record_id', models.IntegerField()),
                ('content', models.TextField()),
            ],
        ),
    ]
