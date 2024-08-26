from django.contrib import admin

from .models import *

# Register your models here.

class LOGIN_TABLE(admin.ModelAdmin):
    list_display = ["name","email","password","phone","userType"]
admin.site.register(login_table,LOGIN_TABLE)

class USER_INFORMATION(admin.ModelAdmin):
    list_display = ["user","dob","address","enrollment", "semester", "branch"]
admin.site.register(user_info,USER_INFORMATION)
class TEACHER_INFORMATION(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'subject', 'bio']
admin.site.register(Teacher_info, TEACHER_INFORMATION)
class TEACHER_TABLE(admin.ModelAdmin):
    list_display = ['user', 'verified', 'is_active']
admin.site.register(Teacher, TEACHER_TABLE)
class BRANCH_TABLE(admin.ModelAdmin):
    list_display = ["user","branch_name","branch_photo"]
admin.site.register(branch_table,BRANCH_TABLE)

class SEM_TABLE(admin.ModelAdmin):
    list_display = ["user","semester","sem_photo"]
admin.site.register(sem_table,SEM_TABLE)

class SUB_TABLE(admin.ModelAdmin):
    list_display = ["user","branch_id","sem_id","subject_name","sub_photo"]
admin.site.register(subject_table,SUB_TABLE)

class V_TABLE(admin.ModelAdmin):
    list_display = ["user", "branch_id","sem_id","sub_id","video","video_desc"]
admin.site.register(videos,V_TABLE)

class PDF_TABLE(admin.ModelAdmin):
    list_display = ["user", "branch_id","sem_id","sub_id", "book_desc", "book_file"]
admin.site.register(book_table,PDF_TABLE)

class M_TABLE(admin.ModelAdmin):
    list_display = ["user","branch_id","sem_id","sub_id","study_material","material_desc"]
admin.site.register(material_table,M_TABLE)

class complain_table(admin.ModelAdmin):
    list_display = ["user", "teacher", "comment", "timestamp"]
admin.site.register(complain, complain_table)

class query_table(admin.ModelAdmin):
    list_display = ["user", "teacher", "sub_id", "description", "status", "timestamp"]
admin.site.register(dought, query_table)

class show_subscription(admin.ModelAdmin):
    list_display = ['plan_name', 'duration', 'payment_method', 'amount']
admin.site.register(SubscriptionPlan_table, show_subscription)


class show_card(admin.ModelAdmin):
    list_display = ['card_name', 'card_number', 'cvv', 'card_expiry_date', 'card_balance']
admin.site.register(Card_table, show_card)



class show_payment(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'transaction_id', 'status1', 'time', 'a_amount']
admin.site.register(payment_table, show_payment)

class show_userplan(admin.ModelAdmin):
    list_display = ['user_id', 'plan_id', 'amount','start_date', 'end_date','status']
admin.site.register(UserSubscription, show_userplan)

