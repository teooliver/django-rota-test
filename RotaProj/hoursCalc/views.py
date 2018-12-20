from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from . import forms
from .models import Shift

from django.db.models import Sum, Count

def index(request):

    objects_id = list(Shift.objects.all().values_list('id', flat=True))

    for id in objects_id: # Calculate Interval and Save
        ShiftObject = get_object_or_404(Shift, id=id)
        ShiftObject.time_diff()

    users = User.objects.all()
    form = forms.ClockInOutForm()
    shift = Shift.objects.all() #.order_by('date')
    
    total_hours = 0
    for i in shift:
        total_hours = total_hours + i.duration

    context = {
        'shift': shift,
        'users': users,
        'form':form,
        'total_hours':total_hours,
    }

    return render(request, 'hoursCalc/index.html', context)


def submitForm(request):
    
    if request.method == 'POST':
        form = forms.ClockInOutForm(request.POST)

        if form.is_valid():  

            new_clock_in = str(form.cleaned_data['date'])+ ' ' + str(form.cleaned_data['clock_in'])  
            new_clock_out = str(form.cleaned_data['date'])+ ' ' + str(form.cleaned_data['clock_out'])

            Shift.objects.create(name=form.cleaned_data['name'], 
                                    clock_in=new_clock_in, 
                                    clock_out=new_clock_out,
                                    break_time = form.cleaned_data['break_time'],
                                    date=form.cleaned_data['date'] )
            
    return redirect(index)

            
def remove(request, pk):
    post = get_object_or_404(Shift, pk=pk)
    post.delete()
    return redirect(index)


def selectDate(request):

    users = User.objects.all()
    select_date_form = forms.SelectDateForm()
    total_user_hours = User.objects.annotate(total_duration=Sum('shift__duration'))
    
    objects = []
    shifts = []

    dt="2000-01-01"
    df="2000-01-01"

    if request.method == 'POST':
        select_date_form = forms.SelectDateForm(request.POST)

        if select_date_form.is_valid():

            print("VALIDATION SUCCESS!")
            print("date_from: ", select_date_form.cleaned_data['date_from'])
            print("date_to: ", select_date_form.cleaned_data['date_to'])

            df = select_date_form.cleaned_data['date_from']
            dt = select_date_form.cleaned_data['date_to']
            
            shifts = Shift.objects.select_related('name').filter(date__gte=df, date__lte=dt).order_by('name')

    
    context = {
        'select_date_form': select_date_form,
        'users': users,
        'objects':objects,
        'total_user_hours':total_user_hours,
        'shifts':shifts
    }

    return render(request, 'hoursCalc/select.html', context)
    

def select_periods(request, date_from, date_to):

    users = User.objects.all()
    objects = Shift.objects.filter(date__gte=date_from).filter(date__lte=date_to)

    total_hours = 0
    for i in objects:
        total_hours = total_hours + i.duration
        

    context = {
        'users': users,
        'objects':objects,
        'total_hours':total_hours
    }
    
    return render(request, 'hoursCalc/select.html', context)


