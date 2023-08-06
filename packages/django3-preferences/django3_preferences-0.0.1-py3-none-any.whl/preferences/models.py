from django.db import models
from django.dispatch import receiver

import preferences
from .managers import SingletonManager


class Preferences(models.Model):
    objects = models.Manager()
    singleton = SingletonManager()
    pref_id = models.IntegerField(blank=True, null=True, editable=False)
    
    def __str__(self):
        return "Preferences"


@receiver(models.signals.class_prepared)
def preferences_class_prepared(sender, *args, **kwargs):
    """
    Adds various preferences members to preferences.preferences
    """
    cls = sender
    if issubclass(cls, Preferences):
        # Add singleton manager to subclasses.
        cls.add_to_class('singleton', SingletonManager())
        # Add property for preferences object to preferences.preferences.
        setattr(preferences.Preferences, cls._meta.object_name, property(lambda x: cls.singleton.get()))
