from django.contrib import admin
from network.models import NetworkLink, Product
from django.contrib import messages


@admin.register(NetworkLink)
class NetworkLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "country", "city", "street", "house_number", "network_type",
                    "supplier", "supplier_id", "debt_to_supplier", "created_at", "level")
    list_filter = ("city", "country", "created_at")
    search_fields = ("name", "email", "city", "country")

    # 1. Регистрируем действие в админке
    actions = ['clear_debt']

    # 2. Создаем метод действия
    def clear_debt(self, request, queryset):
        """
        Это метод действия, который будет вызываться когда
        пользователь выберет это действие в админке
        """
        # queryset - это все объекты, отмеченные галочками
        # Массово обновляем задолженность на 0
        updated = queryset.update(debt_to_supplier=0.00)

        # Показываем сообщение пользователю
        self.message_user(
            request,
            f'Задолженность очищена для {updated} объектов.',
            level=messages.SUCCESS  # Можно указать уровень сообщения
        )

    # 3. Добавляем описание для кнопки
    clear_debt.short_description = 'Очистить задолженность перед поставщиком'


@admin.register(Product)
class ProductkAdmin(admin.ModelAdmin):
    list_display = ("id", "network_link", "name", "model", "release_date")
    list_filter = ("network_link", "name", "release_date")
    search_fields = ("name",)
