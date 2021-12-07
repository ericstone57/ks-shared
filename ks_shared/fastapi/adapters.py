from typing import Type, TypeVar

from django.db import models
from fastapi import HTTPException, Path


ModelT = TypeVar("ModelT", bound=models.Model)


def retrieve_object(model_class: Type[ModelT], id: int) -> ModelT:
    instance = model_class.objects.filter(pk=id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Object not found.")
    return instance
