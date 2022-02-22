from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import os, sys
from django.core.mail import send_mail
from .models import Profile, Dataset
from .filters import DatasetFilter
from .forms import AddDatasetForm


def send_info_mail_to_tec_admin(e,procedure):
    tec_admin_mail = getattr(settings, "TEC_ADMIN_EMAIL", None)
    send_mail("Error Sendungsregister","Sendungsregister error {} in procedure {} in line {} ".format(e,procedure,sys.exc_info()[2].tb_lineno) , "sendungsregister@leibniz-fli.de",[tec_admin_mail])

def send_info_mail_about_new_user(user):
    tec_admin_mail = getattr(settings, "TEC_ADMIN_EMAIL", None)
    send_mail("Sendungsregister Nutzerverwaltung","Nutzer {} ist noch keiner Gruppe zugefügt".format(user), "sendungsregister@leibniz-fli.de",[tec_admin_mail])


@login_required
def overview(request):
    try:
        profile = get_object_or_404(Profile, user=request.user)
        if profile.lab:
            entries = Dataset.objects.filter(lab=profile.lab)
            f = DatasetFilter(request.GET, queryset=entries)
            return render(request, 'home.html', {'filter': f})
        else:
            messages.error(request, 'You are not member of a lab. The administrator is informed about it to fix it')
            send_info_mail_about_new_user(request.user)
            return HttpResponseRedirect('/accounts/logout')
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"overview")
        messages.error(request, 'Error: {}'.format(e))
        return HttpResponseRedirect('/')  # Redirect after POST

@login_required
def addDataset(request):
    try:
        if request.method == 'POST':  # If the form has been submitted...
            form = AddDatasetForm(request.POST, request.FILES)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                new_dataset = form.save()
                new_dataset.added_by = request.user
                new_dataset.save()
                messages.success(request, 'Dataset created')
                return HttpResponseRedirect('/')  # Redirect after POST
            else:
                messages.error(request, 'The form is not valid. Please try it again')
                return render(request, 'add_entry.html', {'form': AddDatasetForm()})
        else:
            return render(request, 'add_entry.html', {'form': AddDatasetForm()})
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"addDataset")
        messages.error(request, 'Error creating a new dataset {}'.format(e))
        return HttpResponseRedirect('/') 



