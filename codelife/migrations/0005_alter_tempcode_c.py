# Generated by Django 5.0.6 on 2025-01-07 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codelife', '0004_tempcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempcode',
            name='c',
            field=models.TextField(default='#include<stdio.h>\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}'),
        ),
    ]
