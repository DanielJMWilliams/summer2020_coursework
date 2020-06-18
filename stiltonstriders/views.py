from django.shortcuts import render, HttpResponse

from stiltonstriders.models import *

from datetime import datetime
import json

import calendar
import math

# Create your views here.
def index(request):
    return render(request, "stiltonstriders/index.html")

def juniors(request):
    return render(request, "stiltonstriders/juniors.html")

def seniors(request):
    return render(request, "stiltonstriders/seniors.html")

def news(request):
    return render(request, "stiltonstriders/news.html")

def events(request):
    return render(request, "stiltonstriders/events.html")

def getEvents(request):
    if request.method == "POST":
        year = int(request.POST.get('year', 2020))
        month = int(request.POST.get('month', 6))
        day = int(request.POST.get('day', 15))
        date = datetime(year, month, day)
        eventObjects = Event.objects.all().filter(dateTime__year=date.year, dateTime__month=date.month, dateTime__day=date.day)
        events = []
        for event in eventObjects:
            e = {
                "name":event.name,
                "description":event.description,
                "event_type":event.event_type,
            }
            events.append(e)
        return HttpResponse(json.dumps(events))

def getMonth(request):
    if request.method == "POST":
        month_offset = int(request.POST.get('month_offset', 0))
        year_offset=0
        month = int(datetime.now().month) + month_offset
        while month>12:
            year_offset+=1
            month-=12
        while month<1:
            year_offset-=1
            month+=12
        year = datetime.now().year+year_offset
        data = {
            "month_name": datetime(year, month, 1).strftime("%B"),
            "month_num":datetime(year, month, 1).month,
            "year":year,
            "weeks":getWeeks(year, month),
        }
        return HttpResponse(json.dumps(data))

def view_calendar(request):
    month = datetime.now().month
    year = datetime.now().year
    context={
        "month_name": datetime(year, month, 1).strftime("%B"),
        "month_num":datetime(year, month, 1).month,
        "year":year,
    }
    return render(request, "stiltonstriders/calendar.html", context)

def getWeeks(year, month):
    month_range = calendar.monthrange(year, month)
    weeks = []
    week=[]
    for i in range(0,month_range[0]):
        week.append("")
    day=0
    while day < month_range[1]:
        if(len(week)%7==0 and len(week)!=0):
            weeks.append(week)
            week=[]
        else:
            day+=1
            week.append(str(day))
    if(len(week)!=0):
        while len(week)<7:
            week.append("")
        weeks.append(week)

    return weeks