# Wagtail Schedules
a report module giving users an overview of all pages that have been scheduled for publishing

## Getting started
Assuming you have a Wagtail project up and running, install from source:

`pip install -e git+https://github.com/overcastsoftware/wagtail-schedules.git#egg=wagtailschedules`

Add `wagtailschedules` to your settings.py in the INSTALLED_APPS section, before the core wagtail packages:

```python
INSTALLED_APPS = [
    # ...
    'wagtailschedules',
    # ...
]
```

