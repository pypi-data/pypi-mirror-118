# Django 3 Preferences
__A Django app and fork of [django_preferences](https://pypi.org/project/django-preferences/) allowing the creation of site preferences in the Django admin panel__

## What does it do?
Provides a singleton view in the Admin panel for Preferences objects and an interface to allow the preferences to be used in code or in templates.

## How is it different from django_preferences?

This is a fork and revision of the [django_preferences](https://pypi.org/project/django-preferences/) package, which has not been updated in a number of years. The main changes are:
1. Since most users only manage one site, the dependency on `django.contrib.sites` has been removed, which makes for a nicer user experience.
2. The ability to save and add more records has been disabled in this version, so that only one preferences object can ever exist.
3. This package is built to work with Django 3.1 and above.

## Requirements
1. Python 3
2. Django 3.1 and above

## Installation

1. Run `pip3 install django3-preferences`
2. Add `preferences` to your `INSTALLED_APPS`
3. If you want your preferences exposed in your templates, then add the `preferences.context_processors.preferences_context_processor` to your `TEMPLATES` > `OPTIONS` > `context-processors` setting:
```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'preferences.context_processors.preferences_context_processor',
            ],
        },
    },
]
```

## Usage

To create preferences for your app, create a Django model with the model inheriting from preferences.models.Preferences.
```python
from django.db import models
from preferences.models import Preferences

class SitePreferences(Preferences):
    logged_in_user_can_view = models.BooleanField(default=False)
```

You can then access these preferences in views or other modules by importing the `preferences` module. The preferences are exposed under `preferences.<Model_Name>.<Preference_Name>`
```python
from preferences import preferences

logged_in_user_can_view = preferences.SitePreferences.logged_in_user_can_view
```

To manage the preferences in the Admin panel (which is the whole point of installing this package!!), register them in your app's `admin.py`:
```python
from django.contrib import admin
from preferences.admin import PreferencesAdmin
from <App_Name>.models import SitePreferences

admin.site.register(SitePreferences, PreferencesAdmin)
```

Finally, if you've added the context processor in step 3 of the usage section, then you can access your preferences in the template by typing:
```python
{{ preferences.SitePreferences.logged_in_user_can_view }}
```

## Credits

Original project: [django_preferences](https://pypi.org/project/django-preferences/)

Django 3 revision: [Matt Rudge](https://github.com/lechien73/django3-preferences)