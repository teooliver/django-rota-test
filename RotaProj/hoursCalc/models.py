from django.db import models
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User # PermissionsMixin


class Shift(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    clock_in = models.DateTimeField(blank=True, null=True) #not blanck or null
    clock_out = models.DateTimeField(blank=True, null=True)  #not blanck or null
    date = models.DateField(blank=True, null=True) #not blanck or null
    duration  = models.FloatField(default=0)
    break_time = models.DurationField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=600)

    class Meta:
        ordering = ['date']


    #this should became a save method, so I can take the logic out of the views
    def time_diff(self):
        if self.clock_out and self.clock_in:
            self.duration = (self.clock_out - self.clock_in).seconds/60/60
            if self.break_time:
                self.duration = self.duration - self.break_time.seconds/60/60
                self.duration = round(self.duration, 1)
            self.save()      
        else:
            # self.duration = 0 (aready default on the field attr)
            return

    def __str__(self):
        return str(self.name)

    # def get_absolute_url

     