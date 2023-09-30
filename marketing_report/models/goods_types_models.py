from django.db import models


class GoodMatrixType(models.Model):
    matrix_name = models.CharField(max_length=140)
    deleted = models.BooleanField(default=False)

    def __repr__(self):
        return self.matrix_name

    def __str__(self):
        return str(self.matrix_name)


class GoodCrmType(models.Model):
    crm_name = models.CharField(max_length=140)
    deleted = models.BooleanField(default=False)

    def __repr__(self):
        return self.crm_name

    def __str__(self):
        return str(self.crm_name)
