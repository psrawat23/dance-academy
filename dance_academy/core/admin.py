from django.contrib import admin
from core.models import User, Student,Account,AccountLog

# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(AccountLog)
