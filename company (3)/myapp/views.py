from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
# Create your views here.
from .models import *

def checksession(request):
    try:
        uid = request.session['log_id']
        user = login_table.objects.get(id=uid)
        teacher = None
        profiledata = None
        teacherprofiledata = None

        if user.userType == "teacher":
            teacher = True

            try:
                teacherprofiledata = Teacher_info.objects.get(user=uid)
            except Teacher_info.DoesNotExist:
                pass
        else:
            try:
                profiledata = user_info.objects.get(user=uid)
            except user_info.DoesNotExist:
                pass

        try:
            userplan = UserSubscription.objects.filter(user_id=login_table(id=uid)).first()
            allsub = subject_table.objects.all()
            allteacher = Teacher.objects.all()

            context = {
                'user': user,
                'teacher': teacher,
                'teacherprofiledata': teacherprofiledata,
                'profiledata': profiledata,
                'userplanrenew': userplan,
                'subject': allsub,
                'teachers': allteacher
            }
            return context

        except:
            pass
    except:
        pass

def index(request):
    context = checksession(request)
    print(context)
    return render(request, 'index.html', context)

def userprofile(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == 'POST':
        dob1 = request.POST.get("dob1")
        address1 = request.POST.get("address")
        enrollment1 = request.POST.get("enroll")
        branch1 = request.POST.get("branch")
        semester1 = request.POST.get("semester")
        userprofiledata1 = user_info(user=login_table(id=uid), dob=dob1, address=address1, enrollment=enrollment1, semester=semester1, branch=branch1)
        userprofiledata1.save()
        return redirect('/')
    return render(request, 'userprofile.html', context)

def teacherprofile(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == 'POST':
        dob1 = request.POST.get("dob3")
        bio = request.POST.get("bio3")
        subject = request.POST.get("Subject3")

        teacherprofiledata1 = Teacher_info(user=login_table(id=uid), date_of_birth=dob1, subject=subject, bio=bio)
        teacherprofiledata1.save()
        return redirect('/')
    return render(request, 'teacherprofile.html', context)

def profile(request):
    context = checksession(request)
    uid = request.session['log_id']
    fetchprofile = user_info.objects.get(user=uid)

    context.update({'user': fetchprofile})

    return render(request, 'profile.html', context)

def showteacher(request):
    context = checksession(request)
    uid = request.session['log_id']
    tprofile = Teacher_info.objects.get(user=uid)

    context.update({'user': tprofile})
    return render(request, 'showteacherprofile.html', context)

def signup(request):
    return render(request,'signup.html')

def Teachersignup(request):
    return render(request, 'Teachersignup.html')
def login(request):
    return render(request,'login.html')

def viewdata(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if login_table.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please choose a different email.")
            return redirect('/')

        if password1 == password2:
            registerdata = login_table(name=name, email=email, phone=phone, password=password1)
            registerdata.save()
            messages.info(request, "Registerd Successfully now you can login.")
            return redirect('/login')
        else:
            messages.error(request, "Passwords are not same")

def teacherdata(request):
    if request.method == 'POST':
        uname = request.POST.get("name")
        uemail = request.POST.get("email")
        ucontact = request.POST.get("contact")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:

            userdata = login_table(name=uname, email=uemail, phone=ucontact, password=password1, userType="teacher")
            userdata.save()

            storedata = Teacher(user=login_table(id=userdata.id), verified=False, is_active=True)
            storedata.save()

            messages.success(request, 'Data Inserted Successfully.')
            return redirect('/login')

        else:
            messages.error(request, 'Passwords are not same')
            redirect('/Teachersignup')

    else:
        messages.error(request, 'error occured')
        redirect('/')

    return render(request, "index.html")

def checklogin(request):
    context = checksession(request)
    if request.method == "POST":
        uemail = request.POST.get("email")
        upwd = request.POST.get("password")
        print(uemail)
        print(upwd)
        try:
            logindata = login_table.objects.get(email=uemail, password=upwd)
            request.session['log_id'] = logindata.id
            request.session.save()

        except login_table.DoesNotExist:
            logindata = None

        if logindata is not None:
            messages.success(request, "Login Successfull !!")
            print(logindata)
            return redirect('/')
        else:
            messages.error(request, "Invalid Details")
            return redirect('/')

    return render(request, 'login.html', context)

def logout(request):
    try:
        del request.session['log_id']
        messages.info(request, "Logout Successfully!")
    except:
        pass

    return render(request, "index.html")

def branches(request):
    context = checksession(request)

    if context is None:
        # Handle the case where checksession returns None
        context = {}

    allbranch = branch_table.objects.all()
    context.update({'allbranch': allbranch})

    return render(request, 'branches.html', context)

def branchwisesem(request, bwsid):
    try:
        uid = request.session['log_id']

        try:
            user = login_table.objects.get(id=uid)
        except login_table.DoesNotExist:
            user = None

        allsem = sem_table.objects.all()
        bid = bwsid
        details = {
            'allsem': allsem,
            'bid': bid,
            'user': user,
        }
        return render(request,'allsem.html', details)

    except:
        pass
    return render(request,'allsem.html')

def sembranchwisedata(request):
    try:
        uid = request.session['log_id']

        try:
            user = login_table.objects.get(id=uid)
        except login_table.DoesNotExist:
            user = None

        sem_id = request.GET.get('semid')
        branch_id = request.GET.get('branchid')

        print(sem_id)
        print(branch_id)

        filtersubjects = subject_table.objects.filter(branch_id=branch_table(id=branch_id), sem_id=sem_table(id=sem_id))

        details = {
            'sem_id': sem_id,
            'branch_id': branch_id,
            'filtersubjects': filtersubjects,
            'user': user,
        }

        return render(request,'viewsubjects.html', details)

    except:
        pass
    return render(request,'viewsubjects.html')


def subjectwisematerial(request, swmid):
    try:
        uid = request.session['log_id']

        try:
            user = login_table.objects.get(id=uid)
        except login_table.DoesNotExist:
            user = None

        subid = swmid

        details = {
            'subid': subid,
            'user': user,
        }
        return render(request, 'subjectwisematerial.html', details)
    except:
        pass
    return render(request,'subjectwisematerial.html')
    return render(request,'subjectwisematerial.html')

def viewbooks(request, vbid):
    try:
        uid = request.session['log_id']

        try:
            user = login_table.objects.get(id=uid)
        except login_table.DoesNotExist:
            user = None

        subid = vbid

        if user.userType == "teacher":
            # If the user is a teacher, retrieve all books regardless of subscription
            getbooks = book_table.objects.filter(sub_id=subject_table(id=subid))
        else:
            # For non-teacher users, check if the user has purchased any plan
            if UserSubscription.objects.filter(user_id=user, status='1').exists():
                # User has purchased plan, allow access to view books
                getbooks = book_table.objects.filter(sub_id=subject_table(id=subid))
            else:
                # User has not purchased any plan, redirect to a page indicating access denied
                messages.error(request, 'You need to purchase a plan to access this material.')
                return redirect('/plans')

        details = {
            'getbooks': getbooks,
            'user': user,
        }
        return render(request, 'viewbooks.html', details)
    except:
        pass
    return render(request, 'viewbooks.html')

def viewvideos(request, vsid):
    try:
        uid = request.session['log_id']

        try:
            user = login_table.objects.get(id=uid)
        except login_table.DoesNotExist:
            user = None

        subid = vsid

        if user.userType == "teacher":
            # If the user is a teacher, allow access to view videos without checking for subscription
            getvids = videos.objects.filter(sub_id=subject_table(id=subid))
        else:
            # For non-teacher users, check if the user has purchased any plan
            if UserSubscription.objects.filter(user_id=user, status='1').exists():
                # User has purchased plan, allow access to view videos
                getvids = videos.objects.filter(sub_id=subject_table(id=subid))
            else:
                # User has not purchased any plan, redirect to a page indicating access denied
                messages.error(request, 'You need to purchase a plan to access this material.')
                return redirect('/plans')

        details = {
            'getvids': getvids,
            'user': user,
        }
        return render(request, 'viewvids.html', details)
    except:
        pass
    return render(request, 'viewvids.html')


def viewmaterial(request, vmid):
    try:
        uid = request.session['log_id']

        try:
            user = login_table.objects.get(id=uid)
        except login_table.DoesNotExist:
            user = None

        subid = vmid

        if user.userType == "teacher":
            # If the user is a teacher, allow access to view materials without checking for subscription
            getmaterial = material_table.objects.filter(sub_id=subject_table(id=subid))
        else:
            # For non-teacher users, check if the user has purchased any plan
            if UserSubscription.objects.filter(user_id=user, status='1').exists():
                # User has purchased plan, allow access to view materials
                getmaterial = material_table.objects.filter(sub_id=subject_table(id=subid))
            else:
                # User has not purchased any plan, redirect to a page indicating access denied
                messages.error(request, 'You need to purchase a plan to access this material.')
                return redirect('/plans')

        details = {
            'getmaterial': getmaterial,
            'user': user,
        }
        return render(request, 'viewmaterial.html', details)
    except:
        pass
    return render(request, 'viewmaterial.html')

def teacherdata1(request):
    context = checksession(request)
    return render(request,'teacherdata.html', context)

def teacherdescription(request):
    context = checksession(request)
    uid = request.session['log_id']
    allbranch = branch_table.objects.all()
    allsem = sem_table.objects.all()
    allsub = subject_table.objects.all()
    context.update({'branch': allbranch, 'semester': allsem, 'subject': allsub})

    if request.method == "POST":
        branches = request.POST.get('branch')
        semesters = request.POST.get('semester')
        subjects = request.POST.get('subject')
        bdesc = request.POST.get('bdescription')
        bookpdf = request.FILES.get('bpdf')

        adddata = book_table(user=login_table(id=uid),branch_id=branch_table(id=branches), sem_id=sem_table(id=semesters), sub_id=subject_table(id=subjects), book_desc=bdesc, book_file=bookpdf)
        adddata.save()

        messages.success(request, "data added successfully.")
        return redirect('/')

    return render(request, 'teacherdata.html', context)

def teachermaterial(request):
    context = checksession(request)
    uid = request.session['log_id']
    allbranch = branch_table.objects.all()
    allsem = sem_table.objects.all()
    allsub = subject_table.objects.all()
    context.update({'branch': allbranch, 'semester': allsem, 'subject': allsub})

    if request.method == "POST":
        branches = request.POST.get('branch')
        semesters = request.POST.get('semester')
        subjects = request.POST.get('subject')

        mdesc = request.POST.get('mdescription')
        materialpdf = request.FILES.get('mpdf')  # Use FILES for file uploads

        material_data = material_table(user=login_table(id=uid),branch_id=branch_table(id=branches), sem_id=sem_table(id=semesters), sub_id=subject_table(id=subjects), material_desc=mdesc, study_material=materialpdf)
        material_data.save()

        messages.success(request, "data added successfully.")
        return redirect('/')

    return render(request, 'teachermaterial.html', context)

def teachervideo(request):
    context = checksession(request)
    uid = request.session['log_id']
    allbranch = branch_table.objects.all()
    allsem = sem_table.objects.all()
    allsub = subject_table.objects.all()
    context.update({'branch': allbranch, 'semester': allsem, 'subject': allsub})

    if request.method == "POST":
        branches = request.POST.get('branch')
        semesters = request.POST.get('semester')
        subjects = request.POST.get('subject')

        vdesc = request.POST.get('vdescription')
        video = request.FILES.get('video')  # Use FILES for file uploads

        video_data = videos(user=login_table(id=uid), branch_id=branch_table(id=branches), sem_id=sem_table(id=semesters), sub_id=subject_table(id=subjects), video_desc=vdesc, video=video)
        video_data.save()
        messages.success(request, "data added successfully.")
        return redirect('/')

    return render(request, 'teachervideo.html', context)

def doughtsolve(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        subjects = request.POST.get('subject1')
        teachers = request.POST.get('teacher1')
        desc = request.POST.get('description1')

        dought1 = dought(user=login_table(id=uid), teacher=Teacher(id=teachers), sub_id=subject_table(id=subjects), description=desc, status='Not Resolve')
        dought1.save()

        messages.success(request, "data added successfully.")
        return render(request,'index.html',context)

    return render(request, 'dought.html', context)

def showdought(request):
    context = checksession(request)

    # Get user_id and teacher_id from the session or wherever they are stored
    uid = request.session['log_id']
    print(uid)
    # Assuming there is a relationship between Teacher and Dought models
    try:
        teacher = Teacher.objects.get(user=uid)
        showdoughts = dought.objects.filter(teacher=teacher)
        context.update({'showdoughtdata': showdoughts})
        return render(request, 'Doughtlist.html', context)
    except :
        # Handle the case where the teacher does not exist
        pass
    return render(request, 'Doughtlist.html', context)

def updatedought(request,did):
    try:
        # Fetch all dought objects related to the teacher
        dought_objects = dought.objects.get(id=did)
        print(dought_objects)
        dought_objects.status = "Resolve"
        dought_objects.save()
        messages.success(request, 'Data Updated Successfully.')
        return redirect('/showdought')
    except:
        messages.error(request, 'Error occurred')
        return redirect(showdought)

def complains(request):
    context = checksession(request)
    uid = request.session['log_id']

    if request.method == "POST":
        teachers = request.POST.get('teacher1')
        comments = request.POST.get('comment1')

        showcomment = complain(user=login_table(id=uid), teacher=Teacher(id=teachers), comment=comments)
        showcomment.save()

        messages.success(request, "data added successfully.")
        return redirect('/')

    return render(request, 'complain.html', context)
def changepw(request):
    uid = request.session['log_id']
    if request.method == 'POST':
      cpw = request.POST.get("oldpassword")
      npw = request.POST.get("password")

      cusercheck = login_table.objects.get(id=uid)

      checkpw = cusercheck.password
      print(checkpw)
      print(cpw)

      if checkpw == cpw:
          cuser1 = login_table.objects.get(id=uid)
          cuser1.password = npw
          cuser1.save(update_fields=['password'])
          messages.success(request, 'Password Changed Successfully.')
      else:
          messages.error(request, 'Current Password is wrong.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def edituser(request):
    uid = request.session['log_id']
    fetchdata = user_info.objects.get(user=uid)
    context = {
        'user': fetchdata,
    }
    return render(request, 'editprofile.html', context)

def updateuser(request):
    uid = request.session['log_id']
    if request.method == 'POST':
      dob = request.POST.get("dob1")
      address = request.POST.get("address")
      enroll = request.POST.get("enroll")
      branch = request.POST.get("branch")
      semester = request.POST.get("semester")

      cuser1 = user_info.objects.get(user=uid)

      cuser1.dob = dob
      cuser1.address = address
      cuser1.enrollment = enroll
      cuser1.branch = branch
      cuser1.semester = semester

      cuser1.save(update_fields=['dob','address','enrollment','branch', 'semester'])

      messages.success(request, 'Data Updated Successfully. ')

      return redirect('/profile')

    else:
      messages.error(request, 'error occured')

    return redirect(edituser)

def editteacher(request):
    uid = request.session['log_id']
    fetchteacher = Teacher_info.objects.get(user=uid)
    context = {
        'user': fetchteacher,
    }
    return render(request, 'editteacher.html', context)

def updateteacher(request):
    uid = request.session['log_id']
    if request.method == 'POST':
      dateob = request.POST.get("dob3")
      bios = request.POST.get("bio3")
      sub = request.POST.get("Subject3")

      object1 = Teacher_info.objects.get(user=uid)

      object1.date_of_birth = dateob
      object1.bio = bios
      object1.subject = sub


      object1.save(update_fields=['date_of_birth','subject','bio'])

      messages.success(request, 'Data Updated Successfully. ')

      return redirect('/showteacher')

    else:
      messages.error(request, 'error occured')


    return redirect('/editteacher')

def plans(request):
    plan = SubscriptionPlan_table.objects.all()
    context = {
        "plandetails": plan,
    }
    return render(request, "plans.html", context)

def userActivePlan(request):
    context = checksession(request)
    uid = request.session["log_id"]
    userplan = UserSubscription.objects.get(user_id=login_table(id=uid))
    plan_id = userplan.plan_id
    plan = SubscriptionPlan_table.objects.get(id=plan_id.id)
    status = userplan.status
    context.update({
        "plandetails": plan,
        'userplan' : userplan
    })
    return render(request, "userActivePlan.html", context)


def payment(request, id):
    plandata = SubscriptionPlan_table.objects.get(id=id)
    amount = plandata.amount
    context = {"plandata": plandata,'amount': amount}
    return render(request, 'payment.html', context)

from datetime import datetime, timedelta
def checkpayment(request):
    if request.method == "POST":
        uid = request.session["log_id"]
        planid = request.POST.get('planid')
        cardNumber = request.POST.get('cardnumber')
        cVV = request.POST.get('cvv1')
        Expiry_date = request.POST.get('expirydate')
        amount = request.POST.get('balance1')

        carddata = Card_table.objects.first()
        number = carddata.card_number
        balance = carddata.card_balance
        ccvv = carddata.cvv
        exdate = carddata.card_expiry_date

        if cardNumber == cardNumber and float(amount) < balance and int(cVV) == ccvv:
            # Check if the user already has an active subscription
            user_subscription = UserSubscription.objects.filter(user_id=uid).first()

            if user_subscription:
                # Renew the existing subscription
                user_subscription.renew()
                messages.success(request, 'Your plan has been renewed successfully.')
            else:
                # Create a new subscription
                import uuid
                trans = str(uuid.uuid4())

                plan_id = SubscriptionPlan_table.objects.get(id=planid)
                duration = int(plan_id.duration)
                amount = int(plan_id.amount)
                current_time = timezone.now()
                start_date = current_time
                end_date = start_date + timedelta(days=duration)

                subscription = UserSubscription(
                    user_id=login_table.objects.get(id=uid),
                    plan_id=plan_id,
                    start_date=start_date,
                    end_date=end_date,
                    amount=amount,
                    status=1
                )
                subscription.save()
                order_id = subscription.id

                insertpayment = payment_table(
                    user_id=login_table.objects.get(id=uid),
                    order_id=UserSubscription.objects.get(id=order_id),
                    transaction_id=trans,
                    a_amount=amount,
                    time=current_time,
                    status1='complete'
                )
                insertpayment.save()

                messages.success(request, 'Payment is done. Your subscription has been activated.')

            return redirect('/branches')
        else:
            return render(request, 'index.html')
