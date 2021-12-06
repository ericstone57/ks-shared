import os
from datetime import datetime
from io import BytesIO
from urllib.request import urlopen

import shortuuid
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel, SoftDeletableModel
from requests.models import Response


def generate_uuid() -> str:
    """Generate a UUID."""
    return shortuuid.ShortUUID().random(length=12)


def upload_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return "upload/{instance}/{year}/{month}/{name}{extension}".format(
        instance=slugify(instance._meta.model_name),
        year=datetime.now().strftime("%Y"),
        month=datetime.now().strftime("%m"),
        name=slugify(datetime.now().strftime("%d%H%M%S%f")),
        extension=filename_ext.lower(),
    )


def upload_to_without_rename(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return "upload/{instance}/{year}/{month}/{name}{extension}".format(
        instance=slugify(instance._meta.model_name),
        year=datetime.now().strftime("%Y"),
        month=datetime.now().strftime("%m"),
        name=filename_base,
        extension=filename_ext.lower(),
    )


class BaseModelSoftDeletable(TimeStampedModel, SoftDeletableModel):
    id = models.CharField(
        max_length=30,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel):
    id = models.CharField(
        max_length=30,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    class Meta:
        abstract = True


def load_image_from_url(file, filename):
    f = BytesIO()
    if isinstance(file, str):
        content = urlopen(file).read()
    elif isinstance(file, Response):
        content = file.content
    else:
        raise Exception('unknown file type.')
    f.write(content)
    return InMemoryUploadedFile(f, None, filename, None, len(content), None, None)
