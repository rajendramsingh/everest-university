from django.shortcuts import render, redirect
from .models import StudentLeave
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def contact(request):
    return render(request, 'main/contact.html')

def edit(request, id):
    data = StudentLeave.objects.get(id=id)

    if request.method == "POST":
        data.roll_number = request.POST.get('roll_number')
        data.full_name = request.POST.get('full_name')
        data.faculty = request.POST.get('faculty')
        data.semester = request.POST.get('semester')
        data.start_date = request.POST.get('start_date')
        data.end_date = request.POST.get('end_date')
        data.reason = request.POST.get('reason')
        data.leave_type = request.POST.get('leave_type')
        data.student_mail = request.POST.get('student_mail')
        data.guardian_contact = request.POST.get('guardian_contact')

        data.save() # updated data is saved to the existing row
        messages.success(request, "Leave request updated")

        return redirect('/form/#leave-status')

    return render(request, 'main/edit.html', {'data' : data})

def form(request):
    if request.method == 'POST':
        try:
            roll_number = request.POST.get('roll_number')
            full_name = request.POST.get('full_name')
            faculty = request.POST.get('faculty')
            semester = request.POST.get('semester')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            reason = request.POST.get('reason')
            leave_type = request.POST.get('leave_type')
            student_mail = request.POST.get('student_mail')
            guardian_contact = request.POST.get('guardian_contact')

            StudentLeave.objects.create(
                roll_number = roll_number,
                full_name = full_name,
                faculty = faculty,
                semester = semester,
                start_date = start_date,
                end_date = end_date,
                reason = reason,
                leave_type =leave_type,
                student_mail = student_mail,
                guardian_contact = guardian_contact
            )

            send_mail(
                # subject = 'New Leave Form Entry',
                # message = render_to_string('msg.html',
                #     {
                        # "roll_number" : roll_number,
                        # "full_name" : full_name,
                        # "faculty" : faculty,
                        # "semester" : semester,
                        # "start_date" : start_date,
                        # "end_date" : end_date,
                        # "reason" : reason,
                        # "leave_type" : leave_type,
                        # "student_mail" : student_mail,
                        # "guardian_contact" : guardian_contact,
                        # "date" : datetime.now()
                        'Test email',
                        'This is a test from my Render Django application.',
                        settings.EMAIL_HOST_USER,
                        [settings.EMAIL_HOST_USER],
                        fail_silently=False,
                    # }),
                # from_email = settings.EMAIL_HOST_USER,
                # recipient_list = [student_mail],
                # fail_silently=True,
            )
        except Exception as e:
            print("========== FORM ERROR ==========")
            print(type(e).__name__)
            print(str(e))
            print("================================")
            raise

        #send_mail(subject, message,from_email,recipient_list, fail_silently=True)

        messages.success(request, f"{full_name}, your form has been submitted!!!")
        return redirect('/form/#leave-status')
    
    # Search
    query = request.GET.get('q')

    if query:
        student_leave = StudentLeave.objects.filter(
            is_delete=False
        ).filter(
            Q(roll_number__icontains=query) |
            Q(full_name__icontains=query) |
            Q(faculty__icontains = query) |
            Q(semester__icontains=query) |
            Q(student_mail__icontains=query) |
            Q(reason__icontains = query) |
            Q(leave_type__icontains=query)
        )
    else:
        student_leave = StudentLeave.objects.filter(is_delete=False)

    # Pagination
    paginator = Paginator(student_leave,3)
    page_number = request.GET.get('page')
    student_leave = paginator.get_page(page_number)
    
    return render(
        request, 
        'main/form.html', 
        {
            'student_leave':student_leave
        }
    )


def delete_entry(request, id):
    data = StudentLeave.objects.get(id=id)
    data.is_delete = True
    data.deleted_time = datetime.now()
    data.save()
    messages.warning(request, f'Entry Deleted for {data.full_name} !!!')
    return redirect('/form/#leave-status')

def recycle(request):
    student_leave = StudentLeave.objects.filter(is_delete=True)
    # After 30 days, form entries are automatically deleted
    threshold = datetime.now() - timedelta(days=30)
    expired = StudentLeave.objects.filter(is_delete=True, deleted_time__lt = threshold)
    deleted_count = expired.count()
    if deleted_count > 0:
        expired.delete()
        messages.info(request, f'{deleted_count} forms entries are automatically deleted')
    else:
        messages.info(request,'No expired form entris to auto-remove')
    return render(request, 'main/recycle.html', {'student_leave':student_leave})

def restore(request, id):
    data = StudentLeave.objects.get(id=id)
    data.is_delete = False
    data.save()
    messages.success(request, f"Form entry restored for {data.full_name}")
    return redirect('/form/#leave-status')

def restore_all(request):
    restore_count = StudentLeave.objects.filter(is_delete = True).update(is_delete=False)
    if restore_count:
        messages.success(request,'Restored all Form entries')
    else:
        messages.info(request, 'Nothing to restore')
    return redirect('/form/#leave-status')

def clear_all(request):
    clear_count = StudentLeave.objects.filter(is_delete = False).update(is_delete=True)
    current_time = datetime.now()
    StudentLeave.objects.all().update(is_delete = True, deleted_time = current_time)
    if clear_count:
        messages.warning(request, 'All form entries deleted!!!')
    else:
        messages.info(request, 'Nothing to delete')
    return redirect('/form/#leave-status')

def delete_hard(request, id):
    data = StudentLeave.objects.get(id=id)
    full_name = data.full_name
    data.delete()
    messages.warning(request, f'Form entry PERMANENTLY deleted for {full_name}!!!')
    return redirect('/recycle')