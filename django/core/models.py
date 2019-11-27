""" /core/models.py
    django ORMs for service

"""
import os
from uuid import uuid4
from django.db import models


def _get_image_uuid4(instance, filename):
    return os.path.join('upload', f"{uuid4()}.{filename.split('.')[-1]}")


class History(models.Model):
    CLASSES = (
        (0, 'Cat'),
        (1, 'Dog'),
    )
    SUPPORTED_MODELS = (
        ('svm', 'SVM'),
        ('dt', 'Decision Tree'),
        ('cnn', 'CNN')
    )

    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to=_get_image_uuid4)
    label = models.CharField(max_length=16, choices=CLASSES)
    model = models.CharField(max_length=32, choices=SUPPORTED_MODELS)
    prediction = models.CharField(max_length=16, choices=CLASSES)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # delete image media file on delete
        if os.path.exists(self.img.path):
            self.img.delete(save=False)
        super().delete(*args, **kwargs)
