from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.utils.safestring import mark_safe
import datetime as datetime_get


# USer class
class User(AbstractUser):
    pass


# ?================== Books Data models ======================================
class Student(models.Model):
    first_name = models.CharField(blank=True,null=True,max_length=250)
    last_name = models.CharField(blank=True,null=True,max_length=250)
    dob =  models.DateField(blank=True, null=True)
    gender_type = [
        (0, "Male"),
        (1, "Female"),
    ]
    gender = models.IntegerField(choices=gender_type, default=0)
    phone_number= models.CharField(max_length=12, null=True, blank=True)
    guardian_name= models.CharField(blank=True,null=True,max_length=250)
    guardian_contact= models.CharField(max_length=12, null=True, blank=True)
    dance_style=models.CharField(max_length=250,null=True,blank=True)
    batch_list = [
        (0, "Morning batch"),
        (1, "Evening Batch"),
        (2, "Zumba"),
    ]
    batch= models.IntegerField(choices=batch_list, default=0)
    timing_list = [
        (0, "05:00 am - 06:00 am"),
        (1, "06:00 am - 07:00 am"),
        (2, "07:00 am - 08:00 am"),
        (3, "08:00 am - 09:00 am"),
        (4, "09:00 am - 10:00 am"),
        (5, "10:00 am - 11:00 am"),
        (6, "11:00 am - 12:00 pm"),
        (7, "12:00 pm - 01:00 pm"),
        (8, "01:00 pm - 02:00 pm"),
        (9, "02:00 pm - 03:00 pm"),
        (10, "03:00 pm - 04:00 pm"),
        (11, "04:00 pm - 05:00 pm"),
        (12, "05:00 pm - 06:00 pm"),
        (13, "06:00 pm - 07:00 pm"),
        (14, "07:00 pm - 08:00 pm"),
        (15, "08:00 pm - 09:00 pm"),
        (16, "09:00 pm - 10:00 pm"),
    ]
    timing = models.IntegerField(choices=timing_list, default=0)
    any_medical_problem=models.BooleanField(default=False)
    medical_certificate=models.FileField(
        upload_to="Dance Academy/medical certificate/", max_length=250, null=True, blank=True
    )
    id_type = [
        (0, "Adhar"),
        (1, "Pan card"),
        (2, "Driving license"),
        (4, "Voter Id"),
    ]
    identity_proof_type = models.IntegerField(choices=id_type, default=0,null=True,blank=True)
    identity_proof_file=models.FileField(
        upload_to="Dance Academy/identify proof/", max_length=250, null=True, blank=True
    )
    noc_document=models.FileField(
        upload_to="Dance Academy/noc document/", max_length=250, null=True, blank=True
    )
    modified_date = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=False)
    student_photo=models.FileField(
        upload_to="Dance Academy/student photo/", max_length=250, null=True, blank=True
    )


    def __str__(self):
        full_name = str(self.first_name) 
        if self.last_name:
            full_name = str(self.first_name) +" "+ str(self.last_name)
        return full_name

    def full_name(self):
        full_name = str(self.first_name) 
        if self.last_name:
            full_name = str(self.first_name) +" "+ str(self.last_name)
        return full_name
    
    def student_picture_view(self):
        if self.student_photo:
            return mark_safe('<img src="{}" width="200" />'.format(self.student_photo.url))
        return None
    
    
class Account(models.Model):
    student = models.ForeignKey(
        Student, null=True, blank=True, on_delete=models.CASCADE
    )
    total_amount = models.FloatField(default=0)
    recieved_amount = models.FloatField(default=0)
    total_due = models.FloatField(default=0.0)
    plan_type = [
        (0, "1 Month"),
        (1, "2 Month"),
        (2, "3 Month"),
        (3, "4 Month"),
        (4, "5 Month"),
        (5, "6 Month"),
        (6, "7 Month"),
        (7, "8 Month"),
        (8, "9 Month"),
        (9, "10 Month"),
        (10, "11 Month"),
        (11, "12 Month"),
    ]
    current_plan = models.IntegerField(choices=plan_type, null=True,blank=True)
    joining_date = models.DateField(auto_now_add=True, null=True,blank=True)
    subscription_start_date = models.DateField(default=None,null=True,blank=True)
    subscription_end_date = models.DateField(default=None,null=True,blank=True)
    last_log = models.ForeignKey(
        "AccountLog", null=True, blank=True, default=None, on_delete=models.SET_NULL
    )
    
    def __str__(self):
        if not self.student:
            return None
        else:
            return self.student.first_name

    def get_due_date(self):
        today = datetime_get.date.today()
        end_date = self.subscription_end_date
        if end_date == None:
            return None
        return (end_date - today).days

class AccountLog(models.Model):
    parent_book = models.ForeignKey(
        Account, null=True, blank=True, on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    subscription_start_date = models.DateField(default=None, null=True,blank=True)
    subscription_end_date = models.DateField(default=None,null=True,blank=True)
    plan_type = [
        (0, "1 Month"),
        (1, "2 Month"),
        (2, "3 Month"),
        (3, "4 Month"),
        (4, "5 Month"),
        (5, "6 Month"),
        (6, "7 Month"),
        (7, "8 Month"),
        (8, "9 Month"),
        (9, "10 Month"),
        (10, "11 Month"),
        (11, "12 Month"),
    ]
    current_plan = models.IntegerField(choices=plan_type,blank=True,null=True)
    total_fees = models.FloatField(default=0.0)
    paid_fees = models.FloatField(default=0.0)
    due = models.FloatField(default=0.0)
    description = models.TextField(max_length=600, blank=True, null=True)

    def __str__(self):
        return str(self.parent_book)
    


    
    
class Enquiry(models.Model):
    name = models.CharField(blank=True,null=True,max_length=250)
    guardian_name= models.CharField(blank=True,null=True,max_length=250)
    guardian_contact= models.CharField(max_length=12, null=True, blank=True)
    age=models.IntegerField(null=True,blank=True)
    note = models.TextField(max_length=600, blank=True, null=True)
    created_on = models.DateField(auto_now_add=True, null=True,blank=True)

    def __str__(self):
        return str(self.name)

class Rental(models.Model):
    client_name = models.CharField(blank=True,null=True,max_length=250)
    purpose = models.CharField(blank=True,null=True,max_length=250)
    timing = models.CharField(blank=True,null=True,max_length=250)
    total_payment = models.FloatField(default=0.0)
    paid_payment = models.FloatField(default=0.0)
    due = models.FloatField(default=0.0)
    note = models.TextField(max_length=600, blank=True, null=True)
    created_on = models.DateField(auto_now_add=True, null=True,blank=True)

    def __str__(self):
        return str(self.client_name)