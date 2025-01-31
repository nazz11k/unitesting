# Generated by Django 5.0.6 on 2024-06-03 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='solution',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.teacher'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['max_score'], name='app_task_max_sco_0abb21_idx'),
        ),
        migrations.AddField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.task'),
        ),
        migrations.AddIndex(
            model_name='courseelement',
            index=models.Index(fields=['name'], name='app_coursee_name_8712a1_idx'),
        ),
        migrations.AddIndex(
            model_name='courseelement',
            index=models.Index(fields=['course'], name='app_coursee_course__5166fb_idx'),
        ),
        migrations.AddIndex(
            model_name='courseelement',
            index=models.Index(fields=['description'], name='app_coursee_descrip_867c29_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['user'], name='app_student_user_id_e4f7f9_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['group'], name='app_student_group_i_d619e2_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['user'], name='app_teacher_user_id_d9c2aa_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['name'], name='app_course_name_c3d697_idx'),
        ),
        migrations.AddIndex(
            model_name='solution',
            index=models.Index(fields=['task'], name='app_solutio_task_id_deeba3_idx'),
        ),
        migrations.AddIndex(
            model_name='solution',
            index=models.Index(fields=['student'], name='app_solutio_student_a724cf_idx'),
        ),
        migrations.AddIndex(
            model_name='solution',
            index=models.Index(fields=['score'], name='app_solutio_score_135b63_idx'),
        ),
    ]
