import os

from django.contrib.auth.models import User
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    gender = models.CharField(
        max_length=1, choices=Gender.choices, default=Gender.OTHER
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="employees")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class EmployeeImage(models.Model):
    """Галерея изображений сотрудника (К3)."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="employees/")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Изображения сотрудников"

    def __str__(self):
        return f"Фото {self.employee} #{self.order}"


@receiver(models.signals.post_delete, sender=EmployeeImage)
def delete_image_file(sender, instance, **kwargs):
    """Удаляет файл с диска при удалении записи."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
