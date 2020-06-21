# Generated by Django 3.1b1 on 2020-06-21 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=60)),
                ('path', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('write_permission', models.CharField(choices=[('Super', 'Super'), ('Staff', 'Staff'), ('Normal', 'Normal')], default='Normal', max_length=6)),
            ],
            options={
                'db_table': 'boards',
            },
        ),
    ]
