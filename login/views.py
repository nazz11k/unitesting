from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.models import Student, Teacher, Course
from login.forms import LogInForm, SignUpForm, PersonalDataForm
from login.models import User, PersonalData


class LogInView(LoginView):
    model = User
    form_class = LogInForm
    template_name = 'login/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')

        next_page = request.GET.get('next') or ''
        form = LogInForm()
        return render(request, self.template_name, {'form': form, 'next': next_page})


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'login/signup.html'

    def get(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        form = SignUpForm(user_type=user_type)
        return render(request, self.template_name, {'form': form, 'user_type': user_type})

    def post(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        form = SignUpForm(request.POST, user_type=user_type)
        if form.is_valid():
            user = form.save(user_type)
            login(self.request, user)
            return redirect('profile')
        else:
            return render(request, self.template_name, {'form': form, 'user_type': user_type})


@login_required
def profile(request):
    user: User = request.user
    personal_data = PersonalData.objects.get(user=user)
    personal_data_form = PersonalDataForm(instance=personal_data)
    if user.is_student:
        user_type = 'student'
        info = Student.objects.get(user=user)
        group = info.group
        courses = Course.objects.all()
        courses = [course for course in courses if group in course.groups.all()]
    elif user.is_teacher:
        user_type = 'teacher'
        info = Teacher.objects.get(user=user)
    else:
        user_type = None
        info = None
    return render(request, 'login/profile.html',
                  {
                      'user': user,
                      'user_type': user_type,
                      'info': info,
                      'courses': courses if user.is_student else '',
                      'personal_data': personal_data,
                      'personal_data_form': personal_data_form,
                  })


class PersonalDataView(CreateView):
    model = PersonalData
    form_class = PersonalDataForm
    template_name = 'login/personal_data.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        user = request.user
        personal_data = PersonalData.objects.get(user=user)
        form = PersonalDataForm(instance=personal_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        personal_data = PersonalData.objects.get(user=user)
        form = PersonalDataForm(request.POST, instance=personal_data)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, self.template_name, {'form': form})