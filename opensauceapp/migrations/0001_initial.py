# Generated by Django 2.1.7 on 2019-03-13 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('additional_informations', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ReportCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ReportReportCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opensauceapp.Report')),
                ('report_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opensauceapp.ReportCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Sauce',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=200)),
                ('answer', models.CharField(max_length=200)),
                ('difficulty', models.IntegerField()),
                ('media_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SauceCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='sauce',
            name='sauce_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opensauceapp.SauceCategory'),
        ),
        migrations.AddField(
            model_name='report',
            name='sauce',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opensauceapp.Sauce'),
        ),
    ]
