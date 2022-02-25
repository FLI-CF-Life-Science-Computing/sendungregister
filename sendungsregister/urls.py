"""sendungsregister URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
import tnp
from tnp.models import Address
from tnp import views
from tnp import autocompleteviews
#from tnb import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tnp.views.overview, name='startview'),
    path('history/', tnp.views.historyView, name='history'),
    path('addentry/', tnp.views.addDataset, name='addDataset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('edit/<int:primary_key>', tnp.views.editDatasetView, name="editDataset"),
    re_path(r'^create/material', login_required(tnp.views.addMaterialPopup), name = "addMaterial"),
    re_path(r'^create/sender_address', login_required(tnp.views.addAddressSenderPopup), name = "addAddressSender"),
    re_path(r'^create/origin_address', login_required(tnp.views.addAddressOriginPopup), name = "addAddressOrigin"),
    re_path(r'^create/recipient_address', login_required(tnp.views.addAddressRecipientPopup), name = "addAddressRecipient"),
    #re_path(r'^address-autocomplete/$', autocomplete.Select2QuerySetView.as_view(model=Address), name = "address-autocomplete"),
    #re_path(r'^address-autocomplete/$', autocompleteviews.AddressAutocomplete.as_view(), name = "address-autocomplete"),
    path("select2/", include("django_select2.urls")),
    path("dataset/create", login_required(views.DatasetCreateView.as_view()), name="dataset-create"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
