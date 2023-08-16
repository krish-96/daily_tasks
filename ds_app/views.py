from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage

import datetime

from .models import Ticket, Stream, Project, UserProfile
from .decorators import  check_authentication, check_superadmin_authentication
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"username : {username} ==> password {password}")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("User Exist")
            try:

                login(request, user)
                # if UserProfile.objects.get(user=user) and not UserProfile.objects.get(user=user).password_changed:
                #     print("User has not changed password!")
                # elif UserProfile.objects.get(user=user) and UserProfile.objects.get(user=user).password_changed:
                #     login(request, user)
                #     messages.success(request, f"Hi {user.username}! You're logged in now, Please change your password to secure your data!")
                #     return redirect('password_change')
                # messages.success(request, f"Hi {user.username}! You're logged in now!")
                return redirect('home')
            except Exception as E:
                print(f"Error in Login ->>", E)
                messages.info(request, f"Please ask your administrator to create a profile for you!")
                redirect('login')

        else:
            messages.success(request, "Invalid Credentials were provided! Please try again.")
            return redirect('login')

    context = {
        'user': request.user,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    return render(request, 'login.html', context=context)


def logout_view(request):
    if request.user.is_authenticated:
        messages.success(request, f"Hi {request.user.username}! You're logged out now!")
        logout(request)
        return redirect('login')
    else:
        messages.error(request, f"There was a problem with Logout. Please try again!")
        return redirect('home')

@check_authentication
def change_password_view(request):
    user_prof = UserProfile.objects.get(user=request.user)
    if request.user.is_authenticated and user_prof and not user_prof.password_changed:
        print("User has not changed the password!")
        if request.method == 'POST':
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            if pass1 == pass2:
                user = User.objects.get(username=request.user)
                print('Password => for user :', user)
                user.set_password(pass1)
                print("pass set")
                user.save()
                print("user saved!")
                user_prof.password_changed=True
                print("user profile pass changed!")
                user_prof.save()
                print("user profile pass changed saved!")
                return redirect('login')

        context = {}
        return render(request, 'password_change.html', context)
    else:
        messages.info(f"{request.user} has already changed the password!")
        return redirect('home')


def get_details(pk):
    try:
        return Ticket.objects.get(pk=pk)
    except Exception:
        return None


@check_authentication
def home(request):
    print(2)

    if request.method == 'POST':
        print(3)
        if  not request.POST.get('ticket_id'):
            title = request.POST.get('title')
            status = request.POST.get('status')
            print(f"title : {title} ==> status {status}")
            Ticket.objects.create(title=title, status=status, user=UserProfile.objects.get(user=request.user))
            messages.success(request, f"Ticket Title : {title} & Status {status} was created successfully.")
            # return redirect("home")
        elif request.POST.get('ticket_id'):
            print(4)
            print("else")
            ticket_id = request.POST.get('ticket_id')
            print(f"ticket_id : {ticket_id}")
            print("ticket_id",  request.POST.get('detail-title'),  request.POST.get('detail-status'))
            # details = Ticket.objects.get(id=ticket_id)
            details = get_details(pk=ticket_id)
            # details = Ticket.objects.filter(id=ticket_id)
            # details.update(title = request.POST.get('title'), status = request.POST.get('status'))
            print("afjbajskhfbsajkvh")
            details.title = request.POST.get('detail-title')
            details.status = request.POST.get('detail-status')
            # details.update(title = request.POST.get('detail-title'), status = request.POST.get('detail-status'))
            details.save()
            print('dasdsa')

    print(5)
    try:
        queryset = Ticket.objects.filter(user__user=request.user)
        # today = str(datetime.datetime.now()+datetime.timedelta(days=1))[:10]
        today = str(datetime.datetime.now())[:10]
        print("today", today)
        print("queryset.created_time", [ q for q in queryset if str(q.created_time)[:10] ==today])
        queryset = [ q for q in queryset if str(q.created_time)[:10] ==today]
    except Exception as E:
        print("Error : ", E)
        queryset = Ticket.objects.all()

    context = {
        'user': request.user,
        'tickets': queryset,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        'stream': UserProfile.objects.get(user=request.user.id)

    }
    return render(request, 'ticket.html', context=context)



@check_authentication
def ticket_details(request, pk):
    details = get_details(pk)
    if details:
        print(f"ticket found for : {request.user.username}")
        context = {
            "id": details.id,
            "title":details.title,
            "status":details.status,
        }
        return JsonResponse(context)
    return render(request, 'ticket.html')

@check_authentication
def ticket_update(request):
    print(f"ticket_update is called")
    if request.method == 'POST':
        details = get_details(request.post.get('id'))
        print(f"ticket_update is called : {details}")
        if details:
            print(f"ticket found for : {request.user.username}")
            context = {
                "title":details.title,
                "status":details.status,
            }
    return render(request, 'ticket.html')

@check_authentication
def ticket_delete(request, pk):
    details = get_details(pk)
    if details:
        title = details.title
        print('Deleting ticket')
        details.delete()
        return JsonResponse({'data':f'{title} is deleted successfully!'})
    return render(request, 'ticket.html')

@check_authentication
def all_tickets_for_mail(request):
    print("Path ; ", request.path)
    if request.user.is_authenticated and not request.user.is_superuser:
        messages.success(request, f"Only admins can access Viewing Tickets and Sending Mail page! Please contact your administrator.")
        return redirect('home')
    if request.method == 'POST':
        print(3)
        if  not request.POST.get('ticket_id'):
            title = request.POST.get('title')
            status = request.POST.get('status')
            print(f"title : {title} ==> status {status}")
            Ticket.objects.create(title=title, status=status, user=request.user)
            messages.success(request, f"Ticket Title : {title} & Status {status} was created successfully.")
        elif request.POST.get('ticket_id'):
            ticket_id = request.POST.get('ticket_id')
            details = Ticket.objects.get(id=ticket_id)
            details.title = request.POST.get('detail-title')
            details.status = request.POST.get('detail-status')
            details.save()
    try:
        # users = [u[0] for u in UserProfile.objects.filter(project__name='ChargeSavvy').values_list('user')]
        users = UserProfile.objects.filter(project__name='ChargeSavvy')
        print('======-==-0=0=0=0- users', users)
        queryset = Ticket.objects.filter(user__in=users).order_by('user')
        # today = str(datetime.datetime.now()+datetime.timedelta(days=1))[:10]
        today = str(datetime.datetime.now())[:10]
        print("today", today)
        print("queryset.created_time", [ q for q in queryset if str(q.created_time)[:10] ==today])
        queryset = [ q for q in queryset if str(q.created_time)[:10] ==today]


    except Exception as E:
        print("Error :=:>" , E)
        queryset = Ticket.objects.all()
    streams = [s for s in Stream.objects.all()]
    ordered_queryset = [query_s for s in streams for query_s in queryset if query_s.user.stream.id == s.id]
    print(f"streams ; {[s.name for s in streams]}")


    context = {
        'user': request.user,
        'tickets': ordered_queryset,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        'stream': UserProfile.objects.get(id=request.user.id)
    }
    return render(request, 'tickets_mail.html', context=context)

def send_email(body, subject='', from_email=None, to_email=None, cc=None, bcc=None):
    try:
        email = EmailMessage(
            "Hello",
            "Body goes here",
            "from@example.com",
            ["to1@example.com", "to2@example.com"],
            ["bcc@example.com"],
            reply_to=["another@example.com"],
            headers={"Message-ID": "foo"},
        )
        email.attach("design.png", 'img_data', "image/png")
        email.send()
        return True
    except Exception as E:
        print(f"Error while sending email to the provided list. ({E})")
        return False

@check_superadmin_authentication
def send_mail_view(request):
    if request.method == 'POST':
        from_mail = request.POST.get('from_mail', None)
        to_list = request.POST.get('to_list', None)
        cc_list = request.POST.get('cc_list', '')
        bcc_list = request.POST.get('bcc_list', '')
        consent = request.POST.get('consent')
        print(f"{from_mail} : {to_list} : {cc_list} : {bcc_list} : {consent}")
        to_list = to_list.split(',') if ',' in to_list else to_list
        cc_list = cc_list.split(',') if ',' in cc_list else cc_list
        bcc_list = bcc_list.split(',') if ',' in bcc_list else bcc_list
        if from_mail and to_list:
            subject = "subject"
            body = "body"
            is_mail_sent = send_email(body=body, subject=subject, from_email=from_mail, to_email=to_list, cc=cc_list, bcc=bcc_list)
            if is_mail_sent:
                print(f"Mail sent successfully")
            else:
                print(f"Mail sent failed!")

        print(f"{from_mail} : {to_list} : {cc_list} : {bcc_list} : {consent}")
        messages.success(request, f"Mail Sent From : {request.POST['from_mail']} To : {request.POST['to_list']} CC : {request.POST['cc_list']} BCC : {request.POST['bcc_list']} Consent: {request.POST['consent']}  ")
        return redirect('all_tickets')
    messages.success(request, f"Only admin can send the mail!")
    return redirect('home')

