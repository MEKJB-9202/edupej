# Generated by Django 5.1.3 on 2025-02-28 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edupejapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='mentors/')),
                ('capacites', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='coursressource',
            name='duree',
            field=models.PositiveIntegerField(blank=True, help_text='Durée de la vidéo en minutes, si applicable', null=True),
        ),
    ]
