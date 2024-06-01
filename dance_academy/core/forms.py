from django.forms import ModelForm
from core.models import Student, Account, AccountLog,Enquiry, Rental


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name","dob", "gender","phone_number",
                  "guardian_name","guardian_contact","dance_style","batch",
                  "timing","any_medical_problem","medical_certificate","identity_proof_type","noc_document",
                  "identity_proof_file","student_photo","active"]


# class AccountForm(ModelForm):
#     class Meta:
#         model = Account
#         fields = ["student", "total_amount","recieved_amount", "total_due","plan_type",
#                   "current_plan","joining_date","subscription_start_date","subscription_end_date"]

class AccountLogForm(ModelForm):
    class Meta:
        model = AccountLog
        fields = ["subscription_start_date","subscription_end_date",
                  "current_plan","total_fees","paid_fees","due",
                  "description"]


class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name","guardian_name","guardian_contact","age","note"]
        

class RentalForm(ModelForm):
    class Meta:
        model = Rental
        fields = ["client_name","purpose","timing","total_payment","paid_payment","due","note"]
        