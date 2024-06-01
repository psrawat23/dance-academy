
from django.contrib import admin
from django.urls import path, include
from core import views

app_name = "dance-academy"


urlpatterns = [
    path("", views.Index, name="index"),
    path("student-list/", views.StudentList, name="studentList"),
    path("delete-record/", views.DeleteRecord, name="deleteRecord"),
    path("student/<slug:id>", views.Student, name="student"),
    path("student-printer/<slug:id>", views.StudentPrinter, name="studentPrinter"),
    path("payment-due-list/", views.PaymentDueList, name="paymentDueList"),
    path("payment-due-form/", views.PaymentDueForm, name="paymentDueForm"),
    path("inactive-student-list/", views.InactiveStudentList, name="inactiveStudentList"),
    path("student-account-log-delete/", views.deleteStudentAccountLog, name="studentAccountLogDelete"),
    path("student-account-log-edit/<slug:id>", views.StudentLogEdit, name="studentAccountLogEdit"),
    path("update-subscription/<slug:id>",views.UpdateFee,name="updateFee"),
    path("student-list/<slug:batch_id>", views.StudentListBatch, name="studentListBatch"),
    path("student-registration-request/", views.StudentRegistrationRequest, name="student_registration_request"),
    path("payment-logs/", views.PaymentLogs, name="paymentLog"),
    path("fee-receipt/<slug:id>", views.FeeReceipt, name="feeReceipt"),
    path("enquiry/", views.EnquiryMethod, name="enquiry"),
    path("rental/", views.RentalMethod, name="rental"),
    path("rental-log-edit/<slug:id>", views.RentalLogEdit, name="rentalLogEdit"),
    path("signout/", views.signout, name="logout"),
    # path("landing-page/", views.landingPage, name="landing_page"),

]