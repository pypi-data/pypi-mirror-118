from django.shortcuts import render
from dj_ingredient_field import IngredientName
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


# Create your views here.


@require_http_methods(["GET"])
def ingredients(request):
    return JsonResponse({'values': IngredientName.choices})
