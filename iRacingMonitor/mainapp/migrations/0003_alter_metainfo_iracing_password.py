# Generated by Django 4.2.3 on 2023-07-14 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_metainfo_iracing_password_metainfo_iracing_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="metainfo",
            name="iRacing_password",
            field=models.BinaryField(),
        ),
    ]
