# Generated by Django 3.2.5 on 2022-01-19 04:47

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ebook', '0035_alter_chapter_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
