# Generated by Django 5.1.3 on 2024-11-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_alter_question_pub_date_alter_question_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(verbose_name='pub_date(發布日期)'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200, verbose_name='question_text(問題描述)'),
        ),
    ]
