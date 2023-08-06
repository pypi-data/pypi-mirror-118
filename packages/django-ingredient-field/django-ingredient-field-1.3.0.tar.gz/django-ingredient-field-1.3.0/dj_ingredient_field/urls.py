"""
This module contains urls for retrieving choice data and making lazy loading a possibility.


To use lazy loaded widgets include this module in your urlpatterns::

    urlpatterns = [
        ...
        path('cooking/', include('dj_ingredient_field.urls')),
    ]
"""
from django.urls import path
from .views import ingredients

app_name = 'dj_ingredient_field'
"""
 The app name for `include()` to work without an app name argument 
"""

urlpatterns = [
    path('ingredients/', ingredients, name='ingredients'),
]
"""
    The available endpoints
"""
