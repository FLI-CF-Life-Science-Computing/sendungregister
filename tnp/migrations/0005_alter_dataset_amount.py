# Generated by Django 3.2.12 on 2022-02-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnp', '0004_alter_dataset_disposal_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]