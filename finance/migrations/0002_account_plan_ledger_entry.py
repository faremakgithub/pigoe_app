from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
        ('core', '0002_create_church'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legacy_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('account_number', models.CharField(blank=True, max_length=20)),
                ('account_type', models.CharField(choices=[('debit', 'Débit'), ('credit', 'Crédit'), ('les_deux', 'Les deux')], default='les_deux', max_length=10)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='created_account_plans', to=settings.AUTH_USER_MODEL)),
                ('church', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='account_plans', to='core.church')),
                ('organization', models.ForeignKey(on_delete=models.CASCADE, to='core.organization')),
            ],
            options={
                'verbose_name': 'Plan comptable',
                'verbose_name_plural': 'Plans comptables',
                'ordering': ['account_number'],
            },
        ),
        migrations.CreateModel(
            name='LedgerEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legacy_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('debit', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('operation_date', models.DateField(blank=True, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=50)),
                ('description', models.TextField(blank=True)),
                ('reference_number', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('account_plan', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='ledger_entries', to='finance.accountplan')),
                ('church', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='ledger_entries', to='core.church')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='created_ledger_entries', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=models.CASCADE, to='core.organization')),
            ],
            options={
                'verbose_name': 'Écriture comptable',
                'verbose_name_plural': 'Écritures comptables',
                'ordering': ['-operation_date', '-created_at'],
            },
        ),
    ]
