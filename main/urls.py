from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('form/' , form, name='form'),
    path('edit/<int:id>' , edit, name='edit'),
    path('delete/<int:id>', delete_entry, name='delete_entry'),
    path('recycle/', recycle, name='recycle'),
    path('restore/<int:id>', restore, name='restore'),
    path('restore_all/', restore_all, name='restore_all'),
    path('clear_all/', clear_all, name='clear_all'),
    path('delete_hard/<int:id>', delete_hard, name='delete_hard'),
]
