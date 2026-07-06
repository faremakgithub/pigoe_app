from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_type_and_event_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='role',
            field=models.CharField(choices=[('Principal', 'Principal'), ('Témoin', 'Témoin'), ('Participant', 'Participant'), ('Autre', 'Autre')], default='Participant', max_length=20),
        ),
        migrations.AddField(
            model_name='attendance',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=None),
            preserve_default=False,
        ),
    ]
