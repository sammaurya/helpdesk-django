from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Ticket(models.Model):

    UNASSIGNED_STATUS = 1
    PENDING_STATUS = 2
    RESOLVED_STATUS = 3

    STATUS_CHOICES = (
        (RESOLVED_STATUS, _('Resolved')),
        (UNASSIGNED_STATUS, _('Unassigned')),
        (PENDING_STATUS, _('Pending')),
    )

    Critical = 1
    High = 2
    Normal = 3
    Low = 4
    PRIORITY_CHOICES = (
        (Critical, _('Critical')),
        (High, _('High')),
        (Normal, _('Normal')),
        (Low, _('Low')),
    )
    IT = 1
    Admin =2
    HR = 3
    Maintenance =4
    DEPARTMENT_CHOICES = (
        (IT, _('IT')),
        (Admin, _('Admin')),
        (HR, _('HR')),
        (Maintenance, _('Maintenance')),
    )

    subject = models.CharField(null=False, max_length=100, verbose_name='Subject')
    description = models.TextField(max_length=250, verbose_name='Description')
    department = models.IntegerField(choices=DEPARTMENT_CHOICES, null=False, blank=False, verbose_name='Department')
    seat_no = models.CharField(max_length=10, verbose_name='Seat No')
    created_on = models.DateTimeField(auto_now=True, verbose_name='Created On')
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNASSIGNED_STATUS, verbose_name='Status')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, null=False, blank=False, verbose_name='Priority')
    created_by = models.EmailField(null=False, verbose_name='Created By')
    accepted_by = models.EmailField(null=True, verbose_name='Accepted By')

    class Meta:
        ordering = ('created_on',)

    def __str__(self):
        return str(self.subject)



class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.TextField(max_length=150, null=False, blank=False, verbose_name='Message')
    published_by = models.CharField(default='user', max_length=5, verbose_name='Published By')
    published_at = models.DateTimeField(auto_now=True, verbose_name='Published At' )



    def __str__(self):
        return str(self.message)