# Generated by Django 5.1.2 on 2025-05-03 08:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_amc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_document_number', models.CharField(blank=True, max_length=100, null=True)),
                ('call_type', models.CharField(choices=[('Normal Call', 'Normal Call'), ('AMC Call', 'AMC Call'), ('Job Call', 'Job Call'), ('Service Call', 'Service Call')], max_length=20)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', max_length=10)),
                ('executive_designation', models.CharField(blank=True, max_length=100, null=True)),
                ('attend_date', models.DateTimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('amc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='admins.amc')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='admins.customer')),
                ('executives', models.ManyToManyField(related_name='calls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
