from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
from django.conf import settings
from django.shortcuts import redirect

from .models import User, UploadedFile
from .forms import UploadFileForm

# Create your views here.

@login_required(login_url="/login")
def home(request):
    uploadedFiles = UploadedFile.objects.all().filter(user=request.user.id)
    return render(request, "FileApp/home.html", context={"files": uploadedFiles,
                                                         "user": request.user})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            UploadedFileObj = form.save(commit=False)
            UploadedFileObj.user = request.user
            UploadedFileObj.save()
            return redirect("/")

    else:
        form = UploadFileForm()
        return render(request, "FileApp/upload.html", {"form": form})

@csrf_exempt
def delete_upload(request):
    if request.method == 'POST':
        pkValue = int(json.loads(request.body)["pk"])
        fileToDelete = UploadedFile.objects.get(pk=pkValue)
        fileToDelete.delete()
        print(settings.MEDIA_ROOT+"\\"+"uploads\\"+fileToDelete.filename())
        try:   
            os.remove(settings.MEDIA_ROOT+"\\"+"uploads\\"+fileToDelete.filename())
        except:
            print("error")


    return redirect("/")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "FileApp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "FileApp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "FileApp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username,None, password)
            user.save()
        except IntegrityError:
            return render(request, "FileApp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "FileApp/register.html")