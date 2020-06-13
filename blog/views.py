from django.shortcuts import render, HttpResponse
from .models import Post
import json
# Create your views here.

def index(request):
    context = {
        "posts":Post.objects.all(),
    }
    return render(request, "blog/base.html", context)

def blog(request):
    posts = []
    for post in Post.objects.all():
        p = {
            "title":post.title,
            "content":post.text,
        }
        posts.append(p)
    data = {
        "content":"This is blog content",
        "id":request.path,
        "posts":posts,
    }
    return HttpResponse(json.dumps(data))

def portfolio(request):
    data = {
        "content":"This is portfolio content",
        "id":request.path,
    }
    return HttpResponse(json.dumps(data))