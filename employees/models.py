from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    """Навык сотрудника."""
    name = models.CharField(max_length=100, unique=True)
    level = models.PositiveSmallIntegerField(
        default=1,
        choices=[(i, str(i)) for i in range(1, 11)],
        help_text="Уровень освоения от 1 до 10",
    )

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return f"{self.name} (уровень {self.level})"


class Employee(models.Model):
    """Профиль сотрудника (расширение User)."""
    class Gender(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"
        OTHER = "O", "Другой"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee",
        verbose_name="Пользователь",
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.OTHER,
        verbose_name="Пол",
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(
        max_length=100, blank=True, verbose_name="Отчество"
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="employees",
        verbose_name="Навыки",
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"