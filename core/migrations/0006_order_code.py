# Generated by Django 5.0.6 on 2024-07-27 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
