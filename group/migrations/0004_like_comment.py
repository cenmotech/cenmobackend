# Generated by Django 4.1.7 on 2023-05-09 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("group", "0003_alter_goods_stock"),
    ]

    operations = [
        migrations.CreateModel(
            name="Like",
            fields=[
                ("like_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "like_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="group.post"
                    ),
                ),
                (
                    "like_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("comment_text", models.CharField(max_length=400)),
                ("user_username", models.CharField(max_length=400)),
                (
                    "comment_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="group.post"
                    ),
                ),
                (
                    "comment_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]