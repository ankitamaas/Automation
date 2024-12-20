# Generated by Django 4.2.16 on 2024-11-15 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('page_number', models.IntegerField()),
                ('position', models.IntegerField()),
                ('scrape_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='keyword',
            old_name='keyword_text',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='keyword',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.AddField(
            model_name='scrapedresult',
            name='keyword',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.keyword'),
        ),
    ]
