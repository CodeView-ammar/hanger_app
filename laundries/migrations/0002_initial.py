# Generated by Django 5.1.3 on 2025-07-19 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('laundries', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundry',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laundries', to='users.users'),
        ),
        migrations.AddField(
            model_name='laundryhours',
            name='laundry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hours', to='laundries.laundry'),
        ),
        migrations.AddField(
            model_name='userlaundrymark',
            name='laundry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laundry_users', to='laundries.laundry'),
        ),
        migrations.AddField(
            model_name='userlaundrymark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_laundries', to='users.users'),
        ),
        migrations.AlterUniqueTogether(
            name='userlaundrymark',
            unique_together={('user', 'laundry')},
        ),
    ]
