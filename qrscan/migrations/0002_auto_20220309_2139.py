# Generated by Django 3.2.3 on 2022-03-09 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrscan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('name', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('monument', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('payment_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('count', models.IntegerField()),
                ('ticket_price', models.DecimalField(decimal_places=1, max_digits=7)),
                ('total_cost', models.CharField(max_length=20)),
                ('order_id', models.CharField(blank=True, max_length=100)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='ticket_booking',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
