from django.db import models

# Модель опроса
class Quiz(models.Model):
    vin = models.CharField(verbose_name='Вин', db_index=True, max_length=64)
    color = models.CharField(verbose_name='Цвет', max_length=64)
    brand = models.CharField(verbose_name='Брэнд', max_length=64)
    CAR_TYPES = (
        (1, 'Купе'),
        (2, 'Кросовер'),
        (3, 'Универсал'),
        (4, 'Внедородник'),
    )
    car_type = models.IntegerField(
        verbose_name='Тип машины', choices=CAR_TYPES)
    user = models.CharField(verbose_name='Пользователь', max_length=65)

# Модель пользователя
class User(models.Model):
    email = models.TextField(verbose_name='Email',
                             db_index=True, max_length=40)
    name = models.CharField(verbose_name='User name', max_length=25)
    password = models.TextField(verbose_name='Password')
    doneQuiz = models.IntegerField(verbose_name='Done qiezes')
    undoneQuiz = models.IntegerField(verbose_name='Undone quizes')
