# Generated by Django 4.1.7 on 2023-05-11 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("transaction", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Complain",
            fields=[
                ("complain_id", models.AutoField(primary_key=True, serialize=False)),
                ("complain_text", models.CharField(max_length=400)),
                ("complain_status", models.CharField(max_length=100)),
                (
                    "transaction_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="transaction.transaction",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]