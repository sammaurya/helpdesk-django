
from .models import Ticket
from django import forms
from django.utils.timezone import now

class CreateTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'department', 'priority', 'seat_no']

    def clean(self):
        cleaned_data = super(CreateTicketForm, self).clean()
        subject = cleaned_data.get('subject')
        description = cleaned_data.get('description')
        department = cleaned_data.get('department')
        seat_no = cleaned_data.get('seat_no')
        priority = cleaned_data.get('priority')
        ticket = super().save(commit=False)
        ticket.subject = subject
        ticket.description = description
        ticket.department = department
        ticket.seat_no = seat_no
        ticket.priority = priority
        ticket.created_on = now()
        ticket = super().save(commit=False)

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if commit:
            ticket.save()
        return ticket
