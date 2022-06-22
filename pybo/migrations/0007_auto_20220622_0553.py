# Generated by Django 3.1.3 on 2022-06-21 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0006_auto_20220524_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('has_answer', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_question', to='pybo.category'),
        ),
    ]
