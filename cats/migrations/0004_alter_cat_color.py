# Generated by Django 5.0.8 on 2024-08-16 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0003_achievement_achievementcat_cat_achievements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='color',
            field=models.CharField(choices=[('Gray', 'Серый'), ('Black', 'Чёрный'), ('White', 'Белый'), ('Ginger', 'Рыжий'), ('Mixed', 'Смешанный')], max_length=16),
        ),
    ]
