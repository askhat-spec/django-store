from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
