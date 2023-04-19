from django.db import models
from uuid import uuid4

# Create your models here.

class data(models.Model):
    """_summary_
    use this models pk to connect every other model and data.
    Args:
        models (_type_): _description_
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    heart = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)


class acc(models.Model):
    index = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    acc_x = models.FloatField(max_length=10)
    acc_y = models.FloatField(max_length=10)
    acc_z = models.FloatField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    connected_to = models.ForeignKey(data, on_delete=models.PROTECT)


class gyro(models.Model):
    index = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    gyro_x = models.FloatField(max_length=10)
    gyro_y = models.FloatField(max_length=10)
    gyro_z = models.FloatField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    connected_to = models.ForeignKey(data, on_delete=models.PROTECT)

