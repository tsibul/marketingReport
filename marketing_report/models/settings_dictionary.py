from django.db import models


class SettingsDictionary(models.Model):
    name = models.CharField(max_length=140)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @staticmethod
    def order_default():
        return ['name']
