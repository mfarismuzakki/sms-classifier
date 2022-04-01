# Generated by Django 4.0.3 on 2022-03-31 13:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Personal'), (3, 'Fraud'), (2, 'Advertisement')])),
            ],
        ),
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('create_dt', models.DateTimeField(default=datetime.datetime.now)),
                ('message', models.TextField(blank=True, null=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='user.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='user.user')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.smsclass')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]