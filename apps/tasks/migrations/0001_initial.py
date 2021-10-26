# Generated by Django 3.2.8 on 2021-10-25 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Time')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Last Update Time')),
                ('name', models.CharField(max_length=126, verbose_name='Name')),
                ('status', django_fsm.FSMField(choices=[('PLANNING', 'Планируется'), ('ACTIVE', 'Активная'), ('CONTROLLING', 'Контроль'), ('FINISHED', 'Завершена')], default='PLANNING', max_length=50, verbose_name='Status')),
                ('deadline_at', models.DateTimeField(help_text='Planning to finish at', verbose_name='Deadline')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('observers', models.ManyToManyField(related_name='observing_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Observers')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_status', models.CharField(choices=[('PLANNING', 'Планируется'), ('ACTIVE', 'Активная'), ('CONTROLLING', 'Контроль'), ('FINISHED', 'Завершена')], max_length=126, verbose_name='Previous Status')),
                ('next_status', models.CharField(choices=[('PLANNING', 'Планируется'), ('ACTIVE', 'Активная'), ('CONTROLLING', 'Контроль'), ('FINISHED', 'Завершена')], max_length=126, verbose_name='Next Status')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to='tasks.task', verbose_name='Task')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to=settings.AUTH_USER_MODEL, verbose_name='Formatter')),
            ],
            options={
                'verbose_name': 'Transition',
                'verbose_name_plural': 'Transitions',
            },
        ),
    ]
