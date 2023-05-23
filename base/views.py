from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from .models import New, User, About, Message, File, Event,\
    Task, UserFiles, GroupNumber
from django.contrib.auth import authenticate, login, logout
from .forms import NewForm, RegistrationForm, AboutForm, \
    FileUploadForm, EventCreationForm, TaskCreationForm, \
    FileUUploadForm, UserForm
from django.shortcuts import get_object_or_404
import mimetypes
from datetime import datetime

# Create your views here.


def home(request):
    news = New.objects.order_by('-created')[:3]
    about = About.objects.get(id = 1)
    context = {'news':news, 'about':about}
    return render(request, 'base/home.html', context)


def new(request, pk):
    new = New.objects.get(id=pk)
    prev = New.objects.filter(id__lt=pk).last()
    next = New.objects.filter(id__gt=pk).first()
    prev_new = New.objects.filter(id__lt=pk).order_by('-id').first()
    next_new = New.objects.filter(id__gt=pk).order_by('id').first()
    context = {'new': new, 'prev':prev, 'next':next, 'prev_new':prev_new, 'next_new':next_new}
    return render(request, 'base/news.html', context)


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "Такого пользователя не существует")
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("123")
            #messages.error(request, 'Некорректный логин ИЛИ пароль. Проверьте введённые давнные.')


    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(requset):
    logout(requset)
    return redirect('home')


def registerPage(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Во время регистрации возникла ошибка')

    return render(request, 'base/login_register.html', {'form' : form})


def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return render(request, 'base/admin_page.html')

@login_required(login_url='/login')
def userProfile(request, pk):
    user = User.objects.get(id = pk)
    msgs = user.message_set.all().order_by('-created')
    files = UserFiles.objects.filter(user=user)
    tasks = Task.objects.filter(groups__in=user.groups.all())
    if request.method == 'POST':
        msg = Message.objects.create(
            user = request.user,
            body=request.POST.get('body')
        )
        return redirect('user-profile', request.user.id)
    context = {'user' : user, 'msgs':msgs, 'tasks':
               tasks, 'files':files}
    return render(request, 'base/profile.html', context)


def admin_page(request, pk):
    messages = Message.objects.all()
    admin = User.objects.get(id=pk)
    selected_option = request.POST.get('btnradio')
    collective = UserFiles.objects.get(user__fio=admin.fio, type='collective')
    working = UserFiles.objects.get(user__fio=admin.fio, type='working')
    type = 'buff'
    if selected_option == 'Академическое':
        type = 'academy'
    elif selected_option == 'Методическое':
        type = 'method'
    elif selected_option == 'Воспитательное':
        type = 'treat'
    if request.method == 'POST':
        print(1)
        msg = Message.objects.create(
            user = request.user,
            body=request.POST.get('body'),
            type = type,
        )
        return redirect('admin-page', request.user.id)
    context = {'admin':admin, 'messages':messages, 'collective': collective, 'working': working}
    return render(request, 'base/admin_page.html', context)


def group_info(request, pk):
    group = GroupNumber(id=pk)
    students = User.objects.filter(groups=group)
    context = {'group': group, 'students': students}
    return render(request, 'base/group_info.html', context)


def create_student(request):
    form = RegistrationForm()

    if request.method == 'POST':
        print('yes')
        fio = request.POST.get('name')
        department = request.POST.get('department')
        instrument = request.POST.get('instrument')
        teacher_name = request.POST.get('teacher-name')
        teacher_number = request.POST.get('teacher-number')
        number = request.POST.get('number')
        learning_duration = request.POST.get('learning-duration')
        grade = request.POST.get('grade')
        parent_name_1 = request.POST.get('parent-name-1')
        parent_number_1 = request.POST.get('parent-number-1')
        parent_name_2 = request.POST.get('parent-name-2')
        parent_number_2 = request.POST.get('parent-number-2')
        awards = request.POST.get('awards')
        avatar = request.POST.get('student-photo')
        password = request.POST.get('password')
        user = User(fio=fio, department_name=department, instrument_name=instrument, teacher_name=teacher_name, teacher_number=teacher_number,
                                user_number=number, years=learning_duration, start_year=grade, parent_first_name=parent_name_1, parent_first_number=parent_number_1,
                                parent_second_name=parent_name_2, parent_second_number=parent_number_2, rewards=awards, avatar=avatar, password=password, username=fio)
        user.save()
        if user:
            return render(request, 'base/home.html')
    return render(request, 'base/create_student.html')


def create_teacher(request):
    return render(request, 'base/create_teacher.html')


def create_group(request):
    return render(request, 'base/create_group.html')


def switch(request):
    return render(request, 'base/switch.html')


def teacher_page(request, pk):
    teacher = User.objects.get(id=pk)
    messages = Message.objects.all()
    context = {'teacher': teacher, 'messages': messages}
    return render(request, 'base/teacher_page.html', context)


@login_required(login_url = "/login")
def createNew(request):
    form = NewForm()
    if request.method == 'POST':
        form = NewForm(request.POST)
        if 'preview' in request.POST:
            if form.is_valid():
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                context = {'title':title, 'description':description}
                return render(request, 'base/preview.html', context)
        elif 'publish' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('home')

    context = {'form' : form}
    return render(request, 'base/new_form.html', context)


def newsPage(request):
    news = New.objects.order_by('-created')
    context = {'news' : news}
    return render(request, 'base/article_list.html', context)


def deleteNew(request, pk):
    new = New.objects.get(id=pk)
    new.delete()
    return redirect('news')


def delete_file(request, pk):
    file = File.objects.get(id=pk)
    file.delete()
    return redirect('music-library')


def editNew(request, pk):
    new = New.objects.get(id = pk)
    form = NewForm()
    if request.method == 'POST':
        form = NewForm(request.POST, instance=new)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewForm(instance=new)

    context = {'new':new, 'form':form}
    return render(request, 'base/edit-new.html', context)


def about(request):
    about = About.objects.get(id = 1)
    context = {'about':about}
    return render(request, 'base/about.html', context)


def editAbout(request):
    about = About.objects.get(id=1)
    form = AboutForm()
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=about)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AboutForm(instance=about)

    context = {'about':about, 'form':form}

    return render(request, 'base/edit-about.html', context)


def preview(request):
    if request.method == 'GET':
        form_data = request.POST
        context = {'form_data':form_data}
        return render(request, 'base/preview.html', context)


def teachers(request):
    teacher_list = User.objects.filter(status='teacher')
    context = {'teachers':teacher_list}
    return render(request, 'base/teacher_list.html', context)


def musicLib(request):
    if request.method == 'GET':
        query = request.GET.get('queryInput')
        subject = request.GET.get('subjectInput')
        author = request.GET.get('authorInput')
        department = request.GET.get('departmentInput')
        if query:
            files = File.objects.filter(file_name__icontains=query)
        elif subject:
            files = File.objects.filter(subject__contains=subject)
        elif author:
            files = File.objects.filter(author__contains=author)
        elif department:
            files = File.objects.filter(department__contains=department)
        else:
            files = File.objects.all()

        context = {'files': files}
        return render(request, 'base/music_library.html', context)

    if request.method == 'POST':
        name = request.POST.get('file_name')
        print(name)
        department = request.POST.get('departmentCreate')
        author = request.POST.get('authorCreate')
        subject = request.POST.get('subjectCreate')
        file = request.FILES.get('fileToUpload')

        file_obj = File(file_name=name, department=department, author=author, subject=subject, file_upload=file)
        file_obj.save()

        return redirect('home')
    else:
        form = FileUploadForm()
    files = File.objects.all()
    context = {'files':files}
    return render(request, 'base/music_library.html', context)


def file_upload(request):
    if request.method == 'POST':
        name = request.POST.get('file_name')
        print(name)
        department = request.POST.get('departmentCreate')
        author = request.POST.get('authorCreate')
        subject = request.POST.get('subjectCreate')
        file = request.FILES.get('fileToUpload')

        file_obj = File(file_name=name, department=department, author=author, subject=subject, file_upload=file)
        file_obj.save()

        return redirect('home')
    else:
        form = FileUploadForm()
    context = {'form': form}
    return render(request, 'base/file_upload.html', context)


def file_uupload(request):
    if request.method == 'POST':
        form = FileUUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FileUUploadForm
    context = {'form':form}
    return render(request, 'base/file_upload.html', context)


def download_file(request, pk):
    file = get_object_or_404(File, id=pk)
    response = HttpResponse(file.file_upload)
    response['Content-Disposition'] = f'attachment; filename="{file.file_upload.name}"'
    return response


def download_ufile(request, pk):
    file = get_object_or_404(UserFiles, id = pk)
    response = HttpResponse(file.file_upload)
    response['Content-Disposition'] = f'attachment; filename="{file.file_upload.name}"'
    return response


def rewards(request):
    info = About.objects.get(id = 1)
    context = {'info':info}
    return render(request, 'base/rewards.html', context)


def teachersInfo(request, pk):
    teacher = User.objects.get(id=pk)
    students = User.objects.get(id=pk).students.all()
    passport = UserFiles.objects.get(user__fio=teacher.fio, type='passport')
    vzaim = UserFiles.objects.get(user__fio = teacher.fio, type='vzaim')
    context = {'teacher':teacher, 'students':students, 'passport':passport, 'vzaim':vzaim}
    return render(request, 'base/teacher_info.html', context)


def teacher_edit(request, pk):
    teacher = User.objects.get(id=pk)
    context = {'teacher':teacher}
    return render(request, 'base/teacher_edit.html', context)


def piano_department(request):
    return render(request, 'base/piano_department.html')


def folk_department(request):
    return render(request, 'base/folk_department.html')


def strings_department(request):
    return render(request, 'base/string_department.html')


def folk_strings_department(request):
    return render(request, 'base/folk-string_department.html')


def choir_department(request):
    return render(request, 'base/choral_department.html')

def theory_department(request):
    return render(request, 'base/theoretical_department.html')


def get_piano(request):
    events = Event.objects.filter(department='piano').values('title', 'description', 'date')
    return JsonResponse(list(events), safe=False)


def get_strings(request):
    events = Event.objects.filter(department="strings").values('title', 'description', 'date')
    return JsonResponse(list(events), safe=False)


def get_folk(request):
    events = Event.objects.filter(department="folk").values('title', 'description', 'date')
    return JsonResponse(list(events), safe=False)


def get_string_folk(request):
    events = Event.objects.filter(department="string-folk").values('title', 'description', 'date')
    return JsonResponse(list(events), safe=False)


def get_choir(request):
    events = Event.objects.filter(department="choir").values('title', 'description', 'date')
    return JsonResponse(list(events), safe=False)


def get_theory(request):
    events = Event.objects.filter(department="theory").values('title', 'description', 'date')
    return JsonResponse(list(events), safe=False)


#def get_uni(request, pk):
    # events = Event.objects.filter(department=pk)
    # return JsonResponse(list(events), safe=False)


def new_event(request):
    form = EventCreationForm()
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base/profile.html')

    context = {'form' : form}
    return render(request, 'base/new_event.html', context)


def contingent(request):
    students = User.objects.filter(status='student')
    groups = GroupNumber.objects.all()
    context = {'students': students, 'groups': groups}
    return render(request, 'base/contingent.html', context)


def student_info(request, pk):
    student = User.objects.get(id=pk)
    groups = User.objects.get(id=pk).groups.all()
    current_year = datetime.now().year
    start_year = student.start_year.year
    grade = current_year - start_year + 1
    plan = UserFiles.objects.get(user__fio=student.fio, type='individual')
    if datetime.now().month < 9:
        grade -= 1
    context = {"student": student, "groups":groups, "grade":grade, 'plan': plan}
    return render(request, 'base/student_info.html', context)


def diary(request, pk):
    user = User.objects.get(id=pk)
    tasks = Task.objects.all()
    context = {'tasks':tasks, 'user':user}
    return render(request, 'base/diary.html', context)


def homework(request):
    form = TaskCreationForm()
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/homework.html', context)


def student_edit(request, pk):
    student = User.objects.get(id=pk)
    user = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        print(123)

        form = RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            print(2)
            form.save()
            return redirect(request, 'base/student-info/')
    else:
        form = UserForm(instance=user)

    context = {'form':form, 'user':user, 'student':student}
    return render(request, 'base/student_edit.html', context)
