# Generated by Django 2.2.1 on 2019-05-21 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appQRMusical', '0006_auto_20190520_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro_sesion',
            name='multimediaRespuesta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='multimediaRespuesta+', to='appQRMusical.Multimedia'),
        ),
    ]
