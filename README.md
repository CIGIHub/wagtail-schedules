# Wagtail Schedules
a report module giving users an overview of all pages that have been scheduled for publishing

## Getting started
Assuming you have a Wagtail project up and running:

`pip install wagtailschedules`

Add `wagtailschedules` to your settings.py in the INSTALLED_APPS section, before the core wagtail packages:

```python
INSTALLED_APPS = [
    # ...
    'wagtailschedules',
    # ...
]
```

