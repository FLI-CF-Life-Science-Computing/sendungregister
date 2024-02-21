from cgitb import text
import profile
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
from .forms import AddDatasetForm, MaterialForm, AddressForm, DatasetEditForm
from django.views import generic

# inform it nerd about bad programming code. A 
def send_info_mail_to_tec_admin(e,procedure):
    tec_admin_mail = getattr(settings, "TEC_ADMIN_EMAIL", None)
    if tec_admin_mail:
        send_mail("Error Sendungsregister","Sendungsregister error {} in procedure {} in line {} ".format(e,procedure,sys.exc_info()[2].tb_lineno) , "sendungsregister@leibniz-fli.de",[tec_admin_mail])

# Notify a manager of a new user so he/she can assign the new user to a lab
def send_info_mail_about_new_user(user):
    admin_mail = getattr(settings, "ADMIN_EMAIL", None)
    if admin_mail:
        send_mail("Sendungsregister Nutzerverwaltung","Nutzer {} ist noch keiner Gruppe zugefügt".format(user), "sendungsregister@leibniz-fli.de",[admin_mail])


# main start page
@login_required
def overview(request):
    try:
        end_date = datetime.date(datetime.today())
        start_date = end_date - timedelta(days=365*2)
        profile = get_object_or_404(Profile, user=request.user)
        if profile.lab:
            if profile.lab.name == "Admin": # All members of the Admin group can see all datasets
                entries = Dataset.objects.all().filter(creation_date__range=(start_date, end_date)).order_by('-status','creation_date') # list only datasets with the status open
            else:
                entries = Dataset.objects.filter(creation_date__range=(start_date, end_date)).filter(lab=profile.lab).order_by('-status','creation_date') # the user can only see datasets from their own lab
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

# lists all entries that have the status closed
@login_required
def historyView(request):
    try:
        profile = get_object_or_404(Profile, user=request.user)
        if profile.lab:
            if profile.lab.name == "Admin": # All members of the Admin group can see all datasets
                entries = Dataset.objects.filter(status='c').order_by('creation_date') # list only datasets with the status closed
            else:
                entries = Dataset.objects.filter(lab=profile.lab).filter(status='c').order_by('creation_date') # the user can only see datasets from their own lab
            f = DatasetFilter(request.GET, queryset=entries)
            return render(request, 'history.html', {'filter': f})
        else:
            messages.error(request, 'You are not member of a lab. The administrator is informed about it to fix it')
            send_info_mail_about_new_user(request.user)
            return HttpResponseRedirect('/accounts/logout')
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"historyView")
        messages.error(request, 'Error: {}'.format(e))
        return HttpResponseRedirect('/')  # Redirect after POST

# creates a new dataset
"""@login_required
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
"""
# needed to add new material on the addentry page
@login_required
def addMaterialPopup(request):
    try:
        form = MaterialForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "{}", "{}", "#id_material");</script>'.format(instance.pk, instance))
        return render(request, "material_form.html", {"form" : form})
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"addMaterialPopup")
        messages.error(request, 'Error creating a new Material {}'.format(e))
        return HttpResponseRedirect('/') 

# needed to add a new origin address on the addentry page
@login_required
def addAddressOriginPopup(request):
    try:
        form = AddressForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "{}", "{}", "#id_point_of_origin");</script>'.format(instance.pk, instance))
        return render(request, "address_form.html", {"form" : form})
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"addAddressOriginPopup")
        messages.error(request, 'Error creating a new Address {}'.format(e))
        return HttpResponseRedirect('/') 

# needed to add a new sender address on the addentry page
@login_required
def addAddressSenderPopup(request):
    try:
        form = AddressForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "{}", "{}", "#id_sender");</script>'.format(instance.pk, instance))
        return render(request, "address_form.html", {"form" : form})
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"addAddressSenderPopup")
        messages.error(request, 'Error creating a new Address {}'.format(e))
        return HttpResponseRedirect('/') 


# needed to add a new recipient address on the addentry page
@login_required
def addAddressRecipientPopup(request):
    try:
        form = AddressForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "{}", "{}", "#id_recipient");</script>'.format(instance.pk, instance))
        return render(request, "address_form.html", {"form" : form})
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"addAddressRecipientPopup")
        messages.error(request, 'Error creating a new Address {}'.format(e))
        return HttpResponseRedirect('/') 

 # used to edit a dataset
@login_required
def editDatasetView(request, primary_key):
    try:
        profile = get_object_or_404(Profile, user=request.user)
        dataset = get_object_or_404(Dataset, pk=primary_key)
        if dataset.lab == profile.lab or profile.lab.name == 'Admin': # The admin can edit all datasets. A normal user only datasets from their lab 
            if request.method == 'POST':
                form = DatasetEditForm(request.POST, instance=dataset)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Data saved successfully / Daten erfolgreich gespeichert')
                    return HttpResponseRedirect('/') 
                else:
                    messages.error(request, 'Form is invalid. Please check your values: {}'.format(form.errors))
                    return render(request, 'tnp/dataset_edit_form.html', {'form': DatasetEditForm(instance=dataset),'pk':dataset.pk})
            return render(request, 'tnp/dataset_edit_form.html', {'form': DatasetEditForm(instance=dataset),'pk':dataset.pk})
        else:
            messages.error(request, 'You don\'t have the permission to edit this dataset')
            return HttpResponseRedirect('/') 
    except BaseException as e:
        send_info_mail_to_tec_admin(e,"editDatasetView")
        messages.error(request, 'Error edit a Dataset {}'.format(e))
        return HttpResponseRedirect('/') 
       

class DatasetCreateView(generic.CreateView):
    model = Dataset
    form_class = AddDatasetForm
    initial = {'amount':'2'}
    success_url = "/"

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.lab = profile.lab
        return super().form_valid(form)
