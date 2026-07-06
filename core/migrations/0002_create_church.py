from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Church',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legacy_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('hierarchy', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('annex_count', models.PositiveIntegerField(default=0)),
                ('domain', models.CharField(max_length=255)),
                ('member_count', models.PositiveIntegerField(default=0)),
                ('founded_at', models.DateField(blank=True, null=True)),
                ('photo_main', models.CharField(blank=True, max_length=255)),
                ('photo_secondary', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='created_churches', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=models.CASCADE, to='core.organization')),
            ],
            options={
                'verbose_name': 'Église',
                'verbose_name_plural': 'Églises',
                'ordering': ['name'],
            },
        ),
    ]
