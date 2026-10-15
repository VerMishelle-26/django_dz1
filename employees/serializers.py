from rest_framework import serializers
from .models import Employee, Skill, EmployeeImage


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "level"]


class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = ["id", "image", "order"]


class EmployeeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all(),
        source="skills",
        write_only=True,
        required=False,
    )
    experience_days = serializers.IntegerField(read_only=True)
    workplace_desk = serializers.CharField(
        source="workplace.desk_number", read_only=True
    )
    images = EmployeeImageSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "role",
            "skills",
            "skill_ids",
            "description",
            "hire_date",
            "experience_days",
            "workplace_desk",
            "images",
        ]

    def validate(self, attrs):
        """Прогоняем через full_clean, чтобы сработала валидация clean()."""
        instance = self.instance or Employee()
        for field, value in attrs.items():
            setattr(instance, field, value)
        instance.full_clean(exclude=["user"], validate_unique=False)
        return attrs

    def create(self, validated_data):
        skills = validated_data.pop("skills", [])
        employee = Employee.objects.create(**validated_data)
        if skills:
            employee.skills.set(skills)
        return employee

    def update(self, instance, validated_data):
        skills = validated_data.pop("skills", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if skills is not None:
            instance.skills.set(skills)
        return instance