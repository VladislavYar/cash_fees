# Generated by Django 5.0.4 on 2024-04-28 01:05

import autoslug.fields
import django.core.validators
import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultCover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Название', help_text='Название', max_length=50, unique=True, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, db_comment='Slug-название', editable=False, help_text='Slug-название', max_length=100, populate_from='name', unique=True, verbose_name='Slug-название')),
                ('default_cover', django_resized.forms.ResizedImageField(crop=None, db_comment='Дефолтная обложка', force_format=None, help_text='Дефолтная обложка', keep_meta=True, quality=-1, scale=None, size=(1500, 1500), upload_to='default_cover/', verbose_name='Дефолтная обложка')),
            ],
            options={
                'verbose_name': 'Дефолтная обложка',
                'verbose_name_plural': 'Дефолтные обложки',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Название', help_text='Название', max_length=50, unique=True, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, db_comment='Slug-название', editable=False, help_text='Slug-название', max_length=100, populate_from='name', unique=True, verbose_name='Slug-название')),
            ],
            options={
                'verbose_name': 'Повод для сбора',
                'verbose_name_plural': 'Поводы для сбора',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_first_name', models.CharField(db_comment='Имя пльзователя', help_text='Имя пльзователя', max_length=150, verbose_name='Имя пльзователя')),
                ('user_last_name', models.CharField(db_comment='Фамилия пользователя', help_text='Фамилия пользователя', max_length=150, verbose_name='Фамилия пользователя')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, db_comment='Дата и время создания', help_text='Дата и время создания', verbose_name='Дата и время создания')),
                ('comment', models.TextField(blank=True, db_comment='Комментарий', help_text='Комментарий', null=True, verbose_name='Комментарий')),
                ('payment_amount', models.PositiveIntegerField(db_comment='Сумма платежа', help_text='Сумма платежа', validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(999999)], verbose_name='Сумма платежа')),
            ],
            options={
                'verbose_name': 'Платёж',
                'verbose_name_plural': 'Платежи',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Название', help_text='Название', max_length=50, unique=True, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, db_comment='Slug-название', editable=False, help_text='Slug-название', max_length=100, populate_from='name', unique=True, verbose_name='Slug-название')),
                ('cover', django_resized.forms.ResizedImageField(crop=None, db_comment='Обложка', force_format=None, help_text='Обложка', keep_meta=True, quality=-1, scale=None, size=(1500, 1500), upload_to='covers/', verbose_name='Обложка')),
                ('description', models.TextField(db_comment='Описание', help_text='Описание', validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Описание')),
                ('user_first_name', models.CharField(db_comment='Имя пльзователя', help_text='Имя пльзователя', max_length=150, verbose_name='Имя пльзователя')),
                ('user_last_name', models.CharField(db_comment='Фамилия пользователя', help_text='Фамилия пользователя', max_length=150, verbose_name='Фамилия пользователя')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, db_comment='Дата и время создания', help_text='Дата и время создания', verbose_name='Дата и время создания')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, db_comment='Изображение', force_format=None, help_text='Изображение', keep_meta=True, null=True, quality=-1, scale=None, size=(1500, 1500), upload_to='images/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(db_comment='Активность сбора', default=True, help_text='Активность сбора', verbose_name='Активность сбора')),
                ('url_video', models.URLField(blank=True, db_comment='URL видео', help_text='URL видео', null=True, verbose_name='URL видео')),
                ('close_datetime', models.DateTimeField(blank=True, db_comment='Дата и время закрытия', help_text='Дата и время закрытия', null=True, verbose_name='Дата и время закрытия')),
                ('required_amount', models.PositiveIntegerField(blank=True, db_comment='Необходимая сумма', help_text='Необходимая сумма', null=True, validators=[django.core.validators.MinValueValidator(500), django.core.validators.MaxValueValidator(99999999)], verbose_name='Необходимая сумма')),
                ('organization', models.ForeignKey(db_comment='Некоммерческая организация', help_text='Некоммерческая организация', on_delete=django.db.models.deletion.PROTECT, related_name='collectings', to='organizations.organization', verbose_name='Некоммерческая организация')),
            ],
            options={
                'verbose_name': 'Групповой сбор',
                'verbose_name_plural': 'Групповые сборы',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
    ]
