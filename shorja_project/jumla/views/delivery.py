from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ..decorators import *
from ..models import *
from ..utilities import *


@allowed_users(allowed_roles=['delivery'])
def home(request):
    return render(request, "jumla/vender/home.html")
