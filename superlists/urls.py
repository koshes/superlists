from django.contrib import admin
from django.urls import path

from lists.views import home_page, view_list, new_list

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('lists/new', new_list, name='new_list'),
    path('lists/GREATEST_LIST/', view_list, name='view_list'),
]
