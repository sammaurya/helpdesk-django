from django.urls import path
from . import views

urlpatterns =[
    path('', views.list_tickets, name='list_tickets'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('<int:id>/accept/', views.accept_ticket, name='accept_ticket'),
    path('<int:id>/details/', views.ticket_details, name='ticket_details'),
    path('<int:id>/resolved/', views.ticket_resolved, name='ticket_resolved'),
    path('<int:id>/close/', views.ticket_close, name='ticket_close'),
]