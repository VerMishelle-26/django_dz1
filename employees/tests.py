from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from workplaces.models import Workplace

from .models import Employee, Skill


class HomeViewTests(TestCase):
    """Тесты главной страницы (К1)."""

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test12345")
        Employee.objects.create(
            user=self.user,
            first_name="Иван",
            last_name="Иванов",
            role=Employee.Role.DEVELOPER,
        )

    def test_home_url_accessible(self):
        """Главная доступна без авторизации."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_context_contains_total(self):
        """В контексте есть total = количество сотрудников."""
        response = self.client.get(reverse("home"))
        self.assertIn("total", response.context)
        self.assertEqual(response.context["total"], 1)

    def test_home_context_contains_employees(self):
        """В контексте есть employees (4 последних)."""
        response = self.client.get(reverse("home"))
        self.assertIn("employees", response.context)
        self.assertEqual(len(response.context["employees"]), 1)


class EmployeeListTests(TestCase):
    """Тесты списка сотрудников (К2)."""

    def setUp(self):
        for i in range(15):
            user = User.objects.create_user(username=f"user{i}", password="test12345")
            Employee.objects.create(
                user=user,
                first_name=f"Имя{i}",
                last_name=f"Фамилия{i}",
                role=Employee.Role.DEVELOPER,
                hire_date=date.today() - timedelta(days=i),
            )

    def test_list_url_accessible(self):
        """Список доступен без авторизации."""
        response = self.client.get(reverse("employee_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_pagination_10_per_page(self):
        """Пагинация: на первой странице 10 сотрудников."""
        response = self.client.get(reverse("employee_list"))
        self.assertEqual(len(response.context["page_obj"]), 10)

    def test_list_pagination_second_page(self):
        """На второй странице 5 сотрудников (15 - 10)."""
        response = self.client.get(reverse("employee_list"), {"page": 2})
        self.assertEqual(len(response.context["page_obj"]), 5)


class EmployeeDetailTests(TestCase):
    """Тесты подробной карточки (К3, К4)."""

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test12345")
        self.employee = Employee.objects.create(
            user=self.user,
            first_name="Иван",
            last_name="Иванов",
            role=Employee.Role.DEVELOPER,
        )
        self.url = reverse("employee_detail", args=[self.employee.pk])

    def test_detail_redirects_anonymous(self):
        """Аноним → редирект на логин."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_detail_accessible_for_authenticated(self):
        """Авторизованный → 200."""
        self.client.login(username="test", password="test12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_context_contains_employee(self):
        """В контексте есть employee."""
        self.client.login(username="test", password="test12345")
        response = self.client.get(self.url)
        self.assertEqual(response.context["employee"], self.employee)


class ValidatorTests(TestCase):
    """Тест валидатора соседних столов (К5)."""

    def setUp(self):

        qa_user = User.objects.create_user(username="qa", password="test12345")
        self.qa = Employee.objects.create(
            user=qa_user,
            first_name="Тест",
            last_name="Тестов",
            role=Employee.Role.TESTER,
        )
        Workplace.objects.create(desk_number="2", employee=self.qa)

    def test_validator_blocks_developer_next_to_tester(self):
        """Разработчик рядом с тестировщиком → ValidationError."""
        dev_user = User.objects.create_user(username="dev", password="test12345")
        dev = Employee.objects.create(
            user=dev_user,
            first_name="Раз",
            last_name="Разработчиков",
            role=Employee.Role.DEVELOPER,
        )
        Workplace.objects.create(desk_number="3", employee=dev)

        with self.assertRaises(ValidationError):
            dev.clean()

    def test_validator_allows_far_desk(self):
        """Разработчик далеко от тестировщика → без ошибок."""
        dev_user = User.objects.create_user(username="dev", password="test12345")
        dev = Employee.objects.create(
            user=dev_user,
            first_name="Раз",
            last_name="Разработчиков",
            role=Employee.Role.DEVELOPER,
        )
        Workplace.objects.create(desk_number="10", employee=dev)

        try:
            dev.clean()
        except ValidationError:
            self.fail("Валидатор ошибочно сработал для далёкого стола")
