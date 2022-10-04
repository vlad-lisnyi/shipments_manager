# Generated by Django 4.1.1 on 2022-10-03 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departureLocation', models.CharField(max_length=200)),
                ('destinationLocation', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('In progress', 'Shipment is in progress'), ('Completed', 'Shipment completed'), ('Delayed', 'Shipment is delayed. Await further instructions.')], default='In progress', max_length=200)),
            ],
        ),
    ]
