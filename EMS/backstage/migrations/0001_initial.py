# Generated by Django 2.1.3 on 2019-05-09 14:15

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'db_table': 'adm_class',
            },
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('crno', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('crtype', models.CharField(max_length=10)),
                ('contain_num', models.IntegerField()),
            ],
            options={
                'db_table': 'class_room',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('short_name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'db_table': 'college',
            },
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mno', models.CharField(max_length=20, unique=True)),
                ('mname', models.CharField(default='', max_length=128)),
                ('short_name', models.CharField(max_length=20)),
                ('in_college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstage.College')),
            ],
            options={
                'db_table': 'major',
            },
        ),
        migrations.CreateModel(
            name='MajorPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('cls_num', models.IntegerField()),
                ('people_num', models.IntegerField()),
                ('score_grad', models.IntegerField()),
                ('stu_years', models.IntegerField()),
                ('course_num', models.IntegerField()),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstage.Major')),
            ],
            options={
                'db_table': 'major_plan',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=128)),
                ('sex', models.BooleanField(default=True)),
                ('score_got', models.IntegerField()),
                ('in_year', models.IntegerField()),
                ('in_cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstage.AdmClass')),
            ],
            options={
                'db_table': 'student',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=128)),
                ('sex', models.BooleanField(default=True)),
                ('in_year', models.IntegerField()),
                ('edu_background', models.CharField(max_length=128, null=True)),
                ('title', models.CharField(default='讲师', max_length=128)),
                ('description', models.TextField(null=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstage.College')),
            ],
            options={
                'db_table': 'teacher',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='admclass',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstage.MajorPlan'),
        ),
        migrations.AlterUniqueTogether(
            name='majorplan',
            unique_together={('year', 'major')},
        ),
        migrations.AlterUniqueTogether(
            name='major',
            unique_together={('mno', 'mname')},
        ),
    ]
