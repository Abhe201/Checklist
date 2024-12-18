# Generated by Django 5.1.4 on 2024-12-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('serial', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Service Name')),
                ('category', models.CharField(blank=True, max_length=200, null=True, verbose_name='Category')),
                ('ip', models.CharField(blank=True, max_length=18, null=True, verbose_name='IP Address')),
                ('status', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], default='N/A', max_length=10, verbose_name='Status')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Remarks')),
            ],
        ),
    ]