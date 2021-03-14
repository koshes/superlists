from django.contrib import admin
from django.urls import path

from lists.views import add_item, home_page, view_list, new_list

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('lists/new', new_list, name='new_list'),
    path('lists/<int:list_id>/', view_list, name='view_list'),
    path('lists/<int:list_id>/add_item', add_item, name='add_item'),
]
