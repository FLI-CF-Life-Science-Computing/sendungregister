# Generated by Django 3.2.12 on 2022-02-24 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tnp', '0002_auto_20220211_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sender_address', to='tnp.address'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('co_authors', models.ManyToManyField(related_name='co_authored_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]