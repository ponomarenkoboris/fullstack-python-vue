# Generated by Django 3.2.6 on 2021-08-27 10:10

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250)),
                ('multiple', models.BooleanField(default=False)),
                ('question_photo', models.TextField(blank=True, default='')),
                ('answer', models.TextField()),
                ('question_max_grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now=True, db_index=True)),
                ('quiz_max_grade', models.IntegerField()),
                ('avaliable_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=255)),
                ('user_name', models.CharField(default='None', max_length=255)),
                ('user_surname', models.CharField(default='None', max_length=255)),
                ('quiz_name', models.CharField(max_length=250)),
                ('date_of_completion', models.DateTimeField(auto_now=True, db_index=True)),
                ('user_grade', models.IntegerField()),
                ('quiz_max_grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('quiz_id', models.IntegerField()),
                ('quiz_name', models.CharField(max_length=250)),
                ('user_grade', models.IntegerField()),
                ('max_grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.CharField(max_length=30)),
                ('score', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='quizapi.question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_name', models.CharField(max_length=250)),
                ('user_answer', models.TextField(blank=True, default='Нет ответа')),
                ('correct_answer', models.TextField()),
                ('user_grade', models.IntegerField()),
                ('question_max_grade', models.IntegerField()),
                ('quiz_statistic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_statistic', to='quizapi.quizstatistic')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='question_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizapi.questiongroup'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizapi.quiz'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('auth_status', models.CharField(default='', max_length=7)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
