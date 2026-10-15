import os
from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Навык")
    level = models.PositiveSmallIntegerField(
        default=1,
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name="Уровень",
    )

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return f"{self.name} (уровень {self.level})"


class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"
        OTHER = "O", "Другой"

    class Role(models.TextChoices):
        DEVELOPER = "dev", "Разработчик"
        TESTER = "qa", "Тестировщик"
        MANAGER = "pm", "Менеджер"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    gender = models.CharField(
        max_length=1, choices=Gender.choices, default=Gender.OTHER
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.DEVELOPER,
        verbose_name="Роль",
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    skills = models.ManyToManyField(Skill, blank=True, related_name="employees")
    description = models.TextField(blank=True, verbose_name="Описание")
    hire_date = models.DateField(
        default=date.today, verbose_name="Дата приёма на работу"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["-hire_date"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def experience_days(self):
        """Стаж работы в компании в днях (К2, К6)."""
        return (date.today() - self.hire_date).days

    def first_image(self):
        """Первое изображение галереи."""
        return self.images.order_by("order").first()

    def other_images(self):
        """Галерея без первого изображения."""
        return self.images.order_by("order")[1:]

    def clean(self):
        """Валидация: тестировщик и разработчик не за соседними столами (К8)."""
        super().clean()

        try:
            workplace = self.workplace
        except Workplace.DoesNotExist:
            return

        if not workplace:
            return

        current = workplace.desk_number
        try:
            current_num = int(current)
        except (ValueError, TypeError):
            return

        for neighbor_num in (current_num - 1, current_num + 1):
            neighbor = (
                Workplace.objects.filter(desk_number=str(neighbor_num))
                .select_related("employee")
                .first()
            )
            if not neighbor or not neighbor.employee:
                continue

            roles = {self.role, neighbor.employee.role}
            if {Employee.Role.TESTER, Employee.Role.DEVELOPER} <= roles:
                raise ValidationError(
                    f"Сотрудник с ролью '{self.get_role_display()}' не может "
                    f"сидеть за столом {current} рядом с "
                    f"'{neighbor.employee.get_role_display()}' "
                    f"(стол {neighbor.desk_number})."
                )


class EmployeeImage(models.Model):
    """Галерея изображений сотрудника (К3)."""

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="employees/")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Изображения сотрудников"

    def __str__(self):
        return f"Фото {self.employee} #{self.order}"


from workplaces.models import Workplace  # noqa: E402


@receiver(models.signals.post_delete, sender=EmployeeImage)
def delete_image_file(sender, instance, **kwargs):
    """Удаляет файл с диска при удалении записи (К4 из ДЗ 3)."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
