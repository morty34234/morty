from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = [
    ]
    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('date', models.DateTimeField(verbose_name='Дата и время')),
                ('location', models.CharField(max_length=200, verbose_name='Место проведения')),
                ('event_type', models.CharField(choices=[('concert', 'Концерт'), ('exhibition', 'Выставка'), ('theater', 'Театр'), ('festival', 'Фестиваль'), ('sport', 'Спорт'), ('conference', 'Конференция'), ('other', 'Другое')], max_length=20, verbose_name='Тип мероприятия')),
                ('image', models.ImageField(blank=True, null=True, upload_to='events/', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
                'ordering': ['date'],
            },
        ),
    ]
