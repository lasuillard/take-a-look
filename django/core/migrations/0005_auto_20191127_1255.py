# Generated by Django 2.2.5 on 2019-11-27 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20191127_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='model',
            field=models.CharField(choices=[('svm', 'SVM'), ('dt', 'Decision Tree'), ('cnn', 'CNN')], max_length=32),
        ),
    ]
