# Generated by Django 5.0.1 on 2024-02-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profiles_profile_pic_alter_profiles_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100, unique=True)),
                ('profiles', models.ManyToManyField(related_name='user_skills', to='profiles.profiles')),
            ],
        ),
    ]
