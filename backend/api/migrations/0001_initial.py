# Generated by Django 5.1.7 on 2025-03-07 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_url', models.URLField()),
                ('signature_url', models.URLField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('renewal_score', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('expired', 'Expired')], max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.company')),
            ],
        ),
        migrations.CreateModel(
            name='Clause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clause_text', models.TextField()),
                ('clause_type', models.CharField(max_length=50)),
                ('risk_level', models.CharField(choices=[('low', 'Low'), ('high', 'High')], max_length=10)),
                ('mou', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clauses', to='api.mou')),
            ],
        ),
    ]
