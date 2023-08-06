<p align="center">
  <img src="docs/_static/logo.png" width="200" alt="django-jsonform icon">
</p>

<p align="center">
    A user-friendly JSON editing form for django admin.
</p>

## Install

Install via pip:

```sh
$ pip install django-jsonform
```

Edit your *settings.py* file:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'django_jsonform'
]
```

## Documentation

Quickstart and usage docs can be found at [http://django-jsonform.rtfd.io](http://django-jsonform.rtfd.io).

## Features

 - [x] File uploads
 - [x] Many inputs and field types
 - [x] UI matches with Django admin's
 - [ ] Validation
 - [ ] Recursion (nesting with self references)

## Screenshots

Here's a screenshot of items being added to a shopping list (JSON array) dynamically:

![django-jsonform screenshot](docs/_static/quickstart.gif)

## License

[BSD-3-Clause](LICENSE.txt)
