from django.db import models


class Workplace(models.Model):
    """Рабочее место."""

    desk_number = models.CharField(
        max_length=20, unique=True, verbose_name="Номер стола"
    )
    description = models.TextField(blank=True, verbose_name="Дополнительная информация")
    employee = models.OneToOneField(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workplace",
        verbose_name="Сотрудник",
    )

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"

    def __str__(self):
        return f"Стол №{self.desk_number}"
