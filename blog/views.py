from django.shortcuts import render, HttpResponse
from .models import Post, Project
import json
# Create your views here.

def index(request):
    context = {
        "posts":Post.objects.all(),
    }
    return render(request, "blog/base.html", context)

def blog(request):
    posts = []
    for post in Post.objects.all().order_by('created_date'):
        p = {
            "title":post.title,
            "content":post.text,
            "author":post.author.username,
            "date":str(post.created_date),
        }
        posts.append(p)
    data = {
        "content":"This is blog content",
        "id":request.path,
        "posts":posts,
    }
    return HttpResponse(json.dumps(data))

def portfolio(request):
    projects = []
    for project in Project.objects.all():
        p = {
            "title":project.title,
            "description":project.description,
            "link":project.link,
        }
        projects.append(p)
    data = {
        "content":"This is portfolio content",
        "id":request.path,
        "projects":projects,
    }
    return HttpResponse(json.dumps(data))