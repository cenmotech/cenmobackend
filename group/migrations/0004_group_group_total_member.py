# Generated by Django 4.1.7 on 2023-05-15 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_alter_goods_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_total_member',
            field=models.IntegerField(default=0),
        ),
    ]
