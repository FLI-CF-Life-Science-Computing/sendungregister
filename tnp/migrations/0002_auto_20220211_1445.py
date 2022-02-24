# Generated by Django 3.2.12 on 2022-02-11 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tnp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='disposal_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tnp.disposal_type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataset',
            name='material',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tnp.material'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataset',
            name='specie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tnp.specie'),
            preserve_default=False,
        ),
    ]
