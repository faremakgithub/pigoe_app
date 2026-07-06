from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('core', '0002_create_church'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legacy_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=models.CASCADE, to='core.organization')),
            ],
            options={
                'verbose_name': 'Type d\'événement',
                'verbose_name_plural': 'Types d\'événements',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='event',
            name='church',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='events', to='core.church'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='events', to='events.eventtype'),
        ),
        migrations.AddField(
            model_name='event',
            name='legacy_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=None),
            preserve_default=False,
        ),
    ]
