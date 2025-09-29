from django.db import models
from django.core.exceptions import ValidationError


class NetworkLink(models.Model):
    LEVEL_ZERO = 0
    LEVEL_FIRST = 1
    LEVEL_LAST = 2

    LEVEL_CHOICES = (
        (LEVEL_ZERO, 'Завод'),
        (LEVEL_FIRST, 'Уровень сети №1'),
        (LEVEL_LAST, 'Уровень сети №2'),
    )

    FACTORY = 'factory'
    RETAIL = 'retail'
    ENTREPRENEUR = 'entrepreneur'

    NETWORK_TYPE_CHOICES = (
        (FACTORY, 'Завод'),
        (RETAIL, 'Розничная сеть'),
        (ENTREPRENEUR, 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=255, verbose_name='Название')
    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома')
    # Поле для определения типа звена сети для валидации
    network_type = models.CharField(
        max_length=20,
        choices=NETWORK_TYPE_CHOICES,
        verbose_name='Тип звена сети'
    )
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients',
        verbose_name='Поставщик'
    )
    debt_to_supplier = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name='Задолженность перед поставщиком'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        null=True,  # Можно NULL в базе
        blank=True,  # Можно пустое в формах
        editable=False,  # Не показывать в админке и формах
        verbose_name='Уровень иерархии'
    )

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'

    def clean(self):
        """Валидация бизнес-правил перед сохранением"""
        super().clean()

        # Правило 1: Завод не может иметь поставщика
        if self.network_type == self.FACTORY and self.supplier is not None:
            raise ValidationError({'supplier': 'Завод не может иметь поставщика'})

        # Правило 2: Розничная сеть и ИП должны иметь поставщика
        if self.network_type in [self.RETAIL, self.ENTREPRENEUR] and self.supplier is None:
            raise ValidationError({'supplier': 'Розничная сеть или ИП должны иметь поставщика'})

        # Правило 3: Нельзя ссылаться на самого себя
        if self.supplier and self.supplier == self:
            raise ValidationError({'supplier': 'Нельзя указывать самого себя в качестве поставщика'})

    def save(self, *args, **kwargs):
        # Автоматическое определение уровня иерархии
        if self.supplier is None:
            self.level = self.LEVEL_ZERO  # Если поставщика нет, устанавливается уровень 0, это Завод
        else:
            # Уровень = уровень поставщика + 1
            self.level = self.supplier.level + 1
            # Ограничиваем максимальный уровень
            if self.level > self.LEVEL_LAST:
                self.level = self.LEVEL_LAST

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, уровень сети: {self.level}"


class Product(models.Model):
    network_link = models.ForeignKey(
        NetworkLink,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Звено сети'
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} ({self.model})"
