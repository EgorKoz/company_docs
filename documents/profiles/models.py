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

    date_of_birth = models.DateField(blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def directory(self):
        return settings.MEDIA_ROOT / self.user.username


class Questionnaire(models.Model):
    fio = models.CharField(max_length=100)
    test_date = models.DateField()
