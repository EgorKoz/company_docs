from pathlib import Path

from django.db import models
from django.conf import settings


class Position(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class Company(models.Model):
    value = models.CharField(max_length=100)
    header = models.TextField(max_length=1000)
    main_page_info = models.TextField(max_length=1000)
    footer = models.TextField(max_length=1000)

    def __str__(self):
        return self.value


class News(models.Model):
    value = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.id} News for {self.company}'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    is_admin = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def directory(self):
        return settings.MEDIA_ROOT / self.user.username


class Questionnaire(models.Model):
    GROUP_CHOICES = (
        ('F', 'I'),
        ('S', 'II'),
        ('T', 'III'),
    )
    REASON_CHECK_CHOICES = (
        ('F', 'Первичная'),
        ('S', 'Повторная')
    )
    FIRE_CHECK_CHOICES = (
        ('IN', 'Вводный'),
        ('FR', 'Первичный на рабочем месте'),
        ('SC', 'Повторный'),
        ('UN', 'Внеплановый'),
        ('TA', 'Целевой'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fio = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    test_date = models.DateField()
    chairman = models.CharField(max_length=100)
    chairman_post = models.CharField(max_length=100)
    first_man = models.CharField(max_length=100)
    first_man_post = models.CharField(max_length=100)
    second_man = models.CharField(max_length=100)
    second_man_post = models.CharField(max_length=100)
    responsible_electrical = models.CharField(max_length=100)
    reason_check = models.CharField(max_length=1, choices=REASON_CHECK_CHOICES)
    fire_check = models.CharField(max_length=2, choices=FIRE_CHECK_CHOICES)
    post_code = models.IntegerField()
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    experience = models.IntegerField()
    certificate = models.CharField(max_length=100)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def get_file_name(self):
        return Path(self.file.name).stem
