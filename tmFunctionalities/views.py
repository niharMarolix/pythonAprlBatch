from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
def register(request):
    return JsonResponse({
        "message":"Hello World"
    })
