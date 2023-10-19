# Generated by Django 4.2.6 on 2023-10-18 10:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecoshop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='delivery_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='review_time',
            new_name='date',
        ),
        migrations.CreateModel(
            name='VendorRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecoshop.customer')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecoshop.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecoshop.vendor')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecoshop.customer')),
            ],
        ),
    ]
