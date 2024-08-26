from django.db import models
from django.utils.safestring import mark_safe
from datetime import timedelta
from django.utils import timezone
# Create your models here.
from datetime import datetime, timedelta



order_status = [
    ('placed', 'placed'),
    ('pending', 'pending'),
    ('complete', 'complete'),
]

class login_table(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default="admin@123")
    phone = models.CharField(max_length=20, null=True, blank=True)
    userType = models.CharField(max_length=50, choices=(("user", "user"), ("teacher", "teacher")), default="user")

    def __str__(self):
        return self.name

class user_info(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.CharField(max_length=128)
    enrollment = models.CharField(max_length=100)
    semester = models.IntegerField()
    branch = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name

class Teacher(models.Model):
    user = models.ForeignKey(login_table, models.CASCADE)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.name

class Teacher_info(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    date_of_birth = models.DateField()
    subject = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True)

class branch_table(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    branch_name = models.CharField(max_length=100)
    bimage = models.ImageField(upload_to='photos', default='default.jpg')

    def branch_photo(self):
        return mark_safe('<img src="{}" width="100"/'.format(self.bimage.url))

    branch_photo.allow_tags = True

    def __str__(self):
        return self.branch_name

class sem_table(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    semester = models.CharField(max_length=25)
    semimage = models.ImageField(upload_to='photos', default='default.jpg')

    def sem_photo(self):
        return mark_safe('<img src="{}" width="100"/'.format(self.semimage.url))

    sem_photo.allow_tags = True

    def __str__(self):
        return self.semester

class subject_table(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    branch_id = models.ForeignKey(branch_table, on_delete=models.CASCADE, default="")
    sem_id = models.ForeignKey(sem_table, on_delete=models.CASCADE, default="")
    subject_name = models.CharField(max_length=100)
    subimage = models.ImageField(upload_to='photos', default='default.jpg')

    def sub_photo(self):
        return mark_safe('<img src="{}" width="100"/'.format(self.subimage.url))

    sub_photo.allow_tags = True

    def __str__(self):
        return self.subject_name

class videos(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    branch_id = models.ForeignKey(branch_table, on_delete=models.CASCADE, default="")
    sem_id = models.ForeignKey(sem_table, on_delete=models.CASCADE, default="")
    sub_id = models.ForeignKey(subject_table, on_delete=models.CASCADE, default="")
    video_desc = models.CharField(max_length=250)
    video = models.FileField(upload_to='videos')

class book_table(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    branch_id = models.ForeignKey(branch_table, on_delete=models.CASCADE, default="")
    sem_id = models.ForeignKey(sem_table, on_delete=models.CASCADE, default="")
    sub_id = models.ForeignKey(subject_table, on_delete=models.CASCADE, default="")
    book_desc = models.CharField(max_length=250)
    book_file = models.FileField(upload_to='pdfs')

class material_table(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    branch_id = models.ForeignKey(branch_table, on_delete=models.CASCADE, default="")
    sem_id = models.ForeignKey(sem_table, on_delete=models.CASCADE, default="")
    sub_id = models.ForeignKey(subject_table, on_delete=models.CASCADE, default="")
    material_desc = models.CharField(max_length=250)
    study_material = models.FileField(upload_to='material')

class complain(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default='', null=True, blank=True)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

class dought(models.Model):
    user = models.ForeignKey(login_table, on_delete=models.CASCADE, default='')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default='', null=True, blank=True)
    sub_id = models.ForeignKey(subject_table, on_delete=models.CASCADE, default="")
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=[('Resolve', 'Resolve'), ('Not Resolve', 'Not resolve')])


class SubscriptionPlan_table(models.Model):
    plan_name = models.CharField(max_length=20)
    duration = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.plan_name

class Card_table(models.Model):
    user_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=30)
    card_number = models.CharField(max_length=16, default="")
    cvv = models.IntegerField()
    card_expiry_date = models.CharField(max_length=20, default='')
    card_balance = models.FloatField()



class UserSubscription(models.Model):
    user_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(SubscriptionPlan_table, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    amount = models.FloatField()
    status = models.IntegerField(default=1)

    def is_active(self):
        return self.end_date >= timezone.now()


    def renew(self):
        duration = timedelta(days=int(self.plan_id.duration))
        current_date = datetime.now().date()
        self.end_date = current_date + duration
        self.save()

    def __str__(self):
        return f"{self.user_id} - {self.plan_id}"

class payment_table(models.Model):
    order_id = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    user_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=10)
    status1 = models.CharField(max_length=20, choices=order_status, default='')
    time = models.DateTimeField()
    a_amount = models.FloatField()