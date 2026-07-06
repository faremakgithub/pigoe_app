from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('core', '0002_create_church'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='church',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='members', to='core.church'),
        ),
        migrations.AddField(
            model_name='member',
            name='legacy_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='member',
            name='membership_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='member',
            name='has_left',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_deceased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='sex',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[('masculin', 'Masculin'), ('feminin', 'Féminin')]),
        ),
        migrations.AddField(
            model_name='member',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='birth_place',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='member',
            name='profession',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='member',
            name='nationality',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='member',
            name='baptism_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='baptism_place',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='member_group',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='conversion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='conversion_place',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='holy_spirit_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='holy_spirit_place',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='marital_status',
            field=models.CharField(choices=[('celibataire', 'Célibataire'), ('marie', 'Marié(e)'), ('divorce', 'Divorcé(e)'), ('veuf', 'Veuf(ve)')], default='celibataire', max_length=12),
        ),
        migrations.AddField(
            model_name='member',
            name='children_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='spouse',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='guardian',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='parent_contact',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='member',
            name='activities',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='member_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='member',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
