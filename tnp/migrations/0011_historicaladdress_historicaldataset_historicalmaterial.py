# Generated by Django 3.2.12 on 2022-03-01 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tnp', '0010_auto_20220301_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalMaterial',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('active', 'active'), ('deactivated', 'deactivated')], default='active', max_length=50)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical material',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalDataset',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('category', models.CharField(choices=[('1', '1 - high risk / hohes Risiko '), ('2', '2 - moderate risk / mittleres Risiko'), ('3', '3 - low risk / geringes Risiko')], default='3', help_text='Kategorie', max_length=2)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Menge', max_digits=10)),
                ('reminder_disposal', models.DateField(blank=True, null=True)),
                ('date_of_disposal', models.DateField(blank=True, help_text='Entsorgungsdatum', null=True)),
                ('creation_date', models.DateTimeField(blank=True, editable=False)),
                ('status', models.CharField(choices=[('o', 'open'), ('c', 'closed')], default='o', max_length=2)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('disposal_type', models.ForeignKey(blank=True, db_constraint=False, help_text='Entsorgungsart', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.disposal_type')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('lab', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.lab')),
                ('material', models.ForeignKey(blank=True, db_constraint=False, help_text='Material', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.material')),
                ('point_of_origin', models.ForeignKey(blank=True, db_constraint=False, help_text='Herstellungsort', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.address')),
                ('recipient', models.ForeignKey(blank=True, db_constraint=False, help_text='Empfänger', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.address')),
                ('sender', models.ForeignKey(blank=True, db_constraint=False, help_text='Absender', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.address')),
                ('specie', models.ForeignKey(blank=True, db_constraint=False, help_text='Tierart', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.specie')),
                ('unit', models.ForeignKey(blank=True, db_constraint=False, help_text='Einheit', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tnp.unit')),
            ],
            options={
                'verbose_name': 'historical dataset',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAddress',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=200)),
                ('street', models.CharField(help_text='Straße', max_length=200)),
                ('postal_code', models.CharField(help_text='PLZ', max_length=10)),
                ('city', models.CharField(help_text='Stadt', max_length=30)),
                ('country', models.CharField(default='Deutschland', help_text='Land', max_length=30)),
                ('status', models.CharField(choices=[('active', 'active'), ('deactivated', 'deactivated')], default='active', max_length=50)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical address',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]