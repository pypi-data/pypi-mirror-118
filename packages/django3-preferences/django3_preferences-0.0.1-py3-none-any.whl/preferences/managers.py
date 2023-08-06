from django.db import models


class SingletonManager(models.Manager):
    """
    Returns a single preferences object.
    """
    def get_queryset(self):
        """
        Return the first preferences object.
        Create it if it doesn't exist.
        """

        queryset = super(SingletonManager, self).get_queryset()

        queryset = queryset.filter(pref_id=1)

        if not queryset.exists():
            obj = self.model(pref_id=1)
            obj.save()

        return queryset
