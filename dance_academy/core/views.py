from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core import models
from django.http import HttpResponse, request
import json
from django.core.files.storage import default_storage
from core.forms import StudentForm, AccountLogForm, EnquiryForm, RentalForm
from core.models import Student as studentModel
from core.models import Account as studentAccount
from core.models import AccountLog as studentAccountLog
from core.models import Enquiry
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from core.models import Rental

from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

from django.http import Http404

from django.db.models import Sum


def has_full_permission(user):
    if user.is_superuser:
        return True
    return False


def check_user_able_to_see_page(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            elif request.user.is_superuser:
                return function(request, *args, **kwargs)
            raise Http404
        return wrapper
    return decorator


@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def RentalMethod(request):
    rental_list = Rental.objects.all()
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "dance_academy/rental_form.html", {"title": "Dance Acadamy","rental_list":rental_list})



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def RentalLogEdit(request,id):
    
    rental_log = Rental.objects.get(id=id)
    if request.method == "POST":
        form = RentalForm(request.POST, instance=rental_log)
        # Save the form if data is valid
        if form.is_valid():
            form.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    rental_log_form = RentalForm(instance=rental_log)
    return render(request, "dance_academy/rental_page_view.html",
        {"title": "Dance Acadamy",
       'rental_log_form':rental_log_form})


@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def EnquiryMethod(request):
    enquiry_list = Enquiry.objects.all().order_by("-created_on")
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "dance_academy/enquiry_form.html", {"title": "Dance Acadamy","enquiry_list":enquiry_list})

@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def Index(request):
    obj = studentModel
    return render(request, "dance_academy/index.html", {"title": "Dance Acadamy",'class_obj':obj})


@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def StudentList(request):
    obj = studentModel.objects.filter(active=True).order_by("-modified_date")
    return render(request, "dance_academy/student_list.html", {"title": "Dance Acadamy",'students':obj})


@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def InactiveStudentList(request):
    obj = studentModel.objects.filter(active=False).order_by("-modified_date")
    return render(request, "dance_academy/student_list.html", {"title": "Dance Acadamy",'students':obj})



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def StudentListBatch(request,batch_id):
    obj = studentModel.objects.filter(batch=batch_id,active=True).order_by("-modified_date")
    return render(request, "dance_academy/student_list.html", {"title": "Dance Acadamy",'students':obj})



@check_user_able_to_see_page("staff_permission_dance_academy")
def FeeReceipt(request,id):
    obj = studentAccountLog.objects.get(id=id)
    return render(request, "dance_academy/student_fee_receipt.html", {"title": "Dance Acadamy","obj":obj})


def is_valid_queryparam(param):
    return param != '' and param is not None



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def PaymentLogs(request):
    obj = studentAccountLog.objects.filter(parent_book__student__active=True)
    accounts = studentAccount.objects.filter(student__active=True)

    payment_month = request.GET.get('payment_month')
    joining_month = request.GET.get('joining_month')
    context = {}
    context["payment_month"] = payment_month
    context["joining_month"] = joining_month
    if  payment_month:
        payment_date = payment_month.split("-")
        payment_year = payment_date[0]
        payment_month = payment_date[1]
    if  joining_month:
        joining_date = joining_month.split("-")
        joining_year = joining_date[0]
        joining_month = joining_date[1]
    student_account = request.GET.get('student_account')
    if student_account:
        context["student_account"] = studentAccount.objects.get(id=student_account)

    clear_check = request.GET.get('clear_check')
    if is_valid_queryparam(clear_check):
        pass
    else:
        if is_valid_queryparam(student_account):
            # accounts = accounts.filter(id=student_account)
            obj = obj.filter(parent_book=student_account)
        
        if is_valid_queryparam(payment_month):
            obj = obj.filter(date__year=payment_year,date__month=payment_month)

        if is_valid_queryparam(joining_month):
            obj = obj.filter(parent_book__joining_date__year=joining_year,parent_book__joining_date__month=joining_month)

    total_received = obj.aggregate(Sum("paid_fees"))
    total_due = obj.aggregate(Sum("due"))

    context["title"] = "Dance Acadamy"
    context["AccountLog"] = obj
    context["all_students"] = accounts
    context["total_received"] = total_received['paid_fees__sum']
    context["total_due"] = total_due['due__sum']

    return render(request, "dance_academy/payment_history.html",context)


@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def DeleteRecord(request):
    if request.method=='POST':
        next = request.POST.get('next', '/')
        id=request.POST.get("id")
        studentModel.objects.filter(id=id).delete()
        return HttpResponseRedirect(next)



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def PaymentDueForm(request):
    if request.method == 'POST':
        account_id = request.POST.get("student_account")
        account_obj = studentAccount.objects.get(id=account_id)
        student_log_book=studentAccountLog(parent_book=account_obj)
        form = AccountLogForm(request.POST, instance=student_log_book)
        # Save the form if data is valid
        if form.is_valid():
            form.save()
            updateAccountDetails(account_obj)
    return HttpResponseRedirect(reverse_lazy("dance-academy:paymentDueList"))



def check_account_created(student_obj):
    student_account = None
    try:
        student_account = studentAccount.objects.get(student=student_obj)
    # If object does not exist create one
    except studentAccount.DoesNotExist:
        student_account = studentAccount(student=student_obj)
        student_account.save()
    return student_account



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def StudentLogEdit(request,id):
    
    account_log_obj = studentAccountLog.objects.get(id=id)
    if request.method == "POST":
        form = AccountLogForm(request.POST, instance=account_log_obj)
        # Save the form if data is valid
        if form.is_valid():
            form.save()
            updateAccountDetails(account_log_obj.parent_book)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
    account_log_form = AccountLogForm(instance=account_log_obj)
    return render(request, "dance_academy/student_account_log_view.html",
        {"title": "Dance Acadamy",
        'account_log_obj':account_log_obj,
       'account_log_form':account_log_form})

    


def updateAccountDetails(account_obj):
    '''
    Get the earlliest Subscription end date and add that to the Student Account Account
    '''
    try:
        student_account_log_obj = studentAccountLog.objects.filter(parent_book=account_obj).order_by('subscription_end_date').last()
        total_fees= studentAccountLog.objects.filter(parent_book=account_obj).aggregate(Sum('total_fees'))
        paid_fees= studentAccountLog.objects.filter(parent_book=account_obj).aggregate(Sum('paid_fees'))
        due= studentAccountLog.objects.filter(parent_book=account_obj).aggregate(Sum('due'))

        if student_account_log_obj:
            account_obj.total_amount = float(total_fees["total_fees__sum"])
            account_obj.recieved_amount = float(paid_fees["paid_fees__sum"])
            account_obj.total_due = float(due["due__sum"])
        else:
            account_obj.total_amount = 0.0
            account_obj.recieved_amount = 0.0
            account_obj.total_due = 0.0

    except Exception as e:
        print(str(e)) 

    if student_account_log_obj:
        account_obj.current_plan = student_account_log_obj.current_plan
        account_obj.subscription_start_date = student_account_log_obj.subscription_start_date
        account_obj.subscription_end_date = student_account_log_obj.subscription_end_date
        account_obj.last_log = student_account_log_obj
        
    else:
        account_obj.current_plan = None
        account_obj.subscription_start_date = None
        account_obj.subscription_end_date = None
        account_obj.last_log = None
    account_obj.save()



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def PaymentDueList(request):
    student_accounts = studentAccount.objects.filter(student__active=True).order_by("subscription_end_date")
    # Get the Account Log form 
    account_log_form = AccountLogForm()
    # Get the list of users
    all_students = student_accounts
    return render(request, "dance_academy/student_due_list.html",
                   {"title": "Dance Acadamy",
                    'account_log_form':account_log_form,
                    'account_log_obj':studentAccount,
                    'student_accounts':student_accounts,
                    "all_students":all_students
                    })



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def deleteStudentAccountLog(request):
    if request.method=='POST':
        next = request.POST.get('next', '/')
        id=request.POST.get("id")
        account_obj=request.POST.get("account_obj")
        student_account_obj = studentAccount.objects.get(id=account_obj)
        student_account_log_obj=studentAccountLog.objects.get(id=id)       
        student_account_log_obj.delete()
        #update the student Account Obj
        try:
            updateAccountDetails(student_account_obj)
        except studentAccountLog.DoesNotExist:
            print("Student Logfile do not exist")
            pass
        # After Deleting Select the Account Logs for Account
        return HttpResponseRedirect(next)



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def UpdateFee(request,id):
    student_obj = studentModel.objects.get(pk=id)
    account_obj = check_account_created(student_obj)
    student_log_book=studentAccountLog(parent_book=account_obj)
    if request.method == 'POST':
        form = AccountLogForm(request.POST, instance=student_log_book)
        # Save the form if data is valid
        if form.is_valid():
            form.save()
            updateAccountDetails(account_obj)
    return HttpResponseRedirect(reverse_lazy("dance-academy:student",kwargs={'id':id}))



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def StudentPrinter(request,id):
    obj = studentModel.objects.get(pk=id)
    return render(request, "dance_academy/student_printer.html",
                   {"title": "Dance Acadamy",'obj':obj,
                    })



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def Student(request,id):  
    ## Student Form 
    # If form is submitted
    obj = studentModel.objects.get(pk=id)

    account_obj = check_account_created(obj)
    student_log_book=studentAccountLog(parent_book=account_obj)
    # Get the Account Log form 
    account_log_form = AccountLogForm(instance=student_log_book)
    # get the lsit of all the account_logs of the student

    all_account_log = studentAccountLog.objects.filter(parent_book=account_obj).order_by("-date")

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=obj)
        # Save the form if data is valid
        if form.is_valid():
            form.save()

    form = StudentForm(instance=obj)
    return render(request, "dance_academy/student_page.html",
                   {"title": "Dance Acadamy",'form':form,'obj':obj,
                    'account_log_form':account_log_form,
                    'student_log_book':student_log_book,
                    'all_account_log':all_account_log,
                    'account_obj':account_obj})



@check_user_able_to_see_page("staff_permission_dance_academy")
@login_required(login_url="/signin")
def StudentRegistrationRequest(request):
    response_data = {}
    if request.method == "POST":
        try:
            fname=request.POST.get("firstName")
            lname=request.POST.get("lastName")
            dob=request.POST.get("birthDate")
            phone=request.POST.get("phoneNumber")
            gender=request.POST.get("gender")
            guardianName=request.POST.get("guardianName")
            guardianNo=request.POST.get("guardianNo")
            danceStyle=request.POST.get("danceStyle")
            batch=request.POST.get("batch")
            timing=request.POST.get("timing")  
            medicalProblem=request.POST.get('medicalProblem')
            medicalFitnessCertificate=request.FILES.get("medicalFitnessCertificate")   
            id_type=request.POST.get("id_type")
            id_document=request.FILES.get("id_document")
            student_photo=request.FILES.get("studentPhoto")

            # Files upload
            if medicalFitnessCertificate:
                medicalFitnessCertificate = default_storage.save('Dance Academy/medical certificate/' + medicalFitnessCertificate.name, medicalFitnessCertificate)
            if id_document:
                id_document = default_storage.save('Dance Academy/identify proof/' + id_document.name, id_document)
            if student_photo:
                student_photo = default_storage.save('Dance Academy/student photo/' + student_photo.name, student_photo)
        
            #Save the object
            obj = studentModel(
                first_name = fname,
                last_name = lname,
                dob = dob,
                gender = gender,
                phone_number = phone,
                guardian_name = guardianName,
                guardian_contact = guardianNo,
                dance_style = danceStyle,
                batch = batch,
                timing = timing,
                any_medical_problem = medicalProblem,
                medical_certificate = medicalFitnessCertificate,
                identity_proof_type = id_type,
                identity_proof_file = id_document,
                student_photo = student_photo,
                active = True
            )
            obj.save()
            
            response_data["success"]="True"
            response_data["result"]="Student Registration Completed"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        
        except Exception as e:
            print(str(e))
            response_data["success"]="False"
            response_data["result"]="Student Registration couldn't Completed"
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

@login_required(login_url="/signin")
def signout(request):
    logout(request)
    messages.success(request, "You have been Logged out Successfully!")
    # return redirect('/')
    return redirect(reverse_lazy("admin"))



def landingPage(request):
    if request.user.is_authenticated:
        return render(request, "dance_academy/landing_page.html", {'is_authenticated':request.user.is_authenticated})


