## OBytes Django Payment Tap App

Payment TAP is a Django app for managing payment transactions with TAP. The project consist of wrapper and models to
track transactions, settlement and configuration of tap accounts.


## Quick start

1. Install `ob_dj_payment_tap` latest version `pip install ob_dj_payment_tap`

2. Add "ob_dj_payment_tap" to your `INSTALLED_APPS` setting like this:

```python
   # settings.py
   INSTALLED_APPS = [
        ...
        "ob_dj_payment_tap",
   ]
```

4. Run ``python manage.py migrate`` to create the TAP models.


## Developer Guide

1. Clone github repo `git clone [url]`

2. `pipenv install --dev`

3. `pre-commit install`

4. Run unit tests `pytest`


*Hint* You can install the changes directly in your env using `pip install .`; this should allow you to `pipenv shell` to any env and navigate to the source code and install the package `pip install .`
