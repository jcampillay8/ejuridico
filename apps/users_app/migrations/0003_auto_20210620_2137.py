# Generated by Django 3.1.7 on 2021-06-21 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0002_lawsuithistory_docfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawsuit',
            name='cause_rol',
            field=models.CharField(default='no asignado', max_length=45),
        ),
    ]
