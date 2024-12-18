# Generated by Django 5.1.4 on 2024-12-17 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='frequency',
            field=models.CharField(default='Daily', max_length=50, verbose_name='Frequency'),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], default='Yes', max_length=10, verbose_name='Status'),
        ),
    ]
