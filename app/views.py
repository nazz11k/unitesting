from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from app.models import *
from app.forms import *
from login.decorators import student_required, teacher_required


def index(request):
    if request.user.is_authenticated:
        return redirect(request, 'profile')
    return redirect(request, 'login')


@method_decorator([login_required], name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'app/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        if self.request.user.is_teacher:
            teacher = Teacher.objects.get(user=self.request.user)
            return Course.objects.filter(teacher=teacher)
        elif self.request.user.is_student:
            student = Student.objects.get(user=self.request.user)
            return Course.objects.filter(groups__in=[student.group])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = {'courses': queryset, 'user': request.user}
        return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    template_name = 'app/course_detail.html'
    context_object_name = 'course'

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        course_elements = CourseElement.objects.filter(course=course)
        course_lectures = Lecture.objects.filter(course__id=course.id)
        course_tasks = Task.objects.filter(course_id=course.id)
        context = {
            'course': course,
            'user': request.user,
            'course_elements': course_elements,
            'lectures': course_lectures,
            'tasks': course_tasks,
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'app/course_create.html'
    form_class = CourseCreateForm
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.instance.teacher = self.get_teacher()
        return super().form_valid(form)

    def get_teacher(self):
        try:
            return Teacher.objects.get(user=self.request.user)
        except Teacher.DoesNotExist:
            raise ValueError("Teacher matching query does not exist")

    def get(self, request, *args, **kwargs):
        teacher = self.get_teacher()
        form = self.form_class(teacher=teacher)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        teacher = self.get_teacher()
        form = self.form_class(request.POST, teacher=teacher)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'app/course_update.html'
    form_class = CourseUpdateForm
    success_url = reverse_lazy('course_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        teacher = self.object.teacher
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureCreateView(CreateView):
    model = Lecture
    template_name = 'app/lecture_create.html'
    form_class = LectureCreateForm
    success_url = reverse_lazy('course_list')

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['pk'])
        form = self.form_class(initial={'course': course})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.course = Course.objects.get(pk=kwargs['pk'])
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


@method_decorator([login_required], name='dispatch')
class LectureDetailView(DetailView):
    model = Lecture
    template_name = 'app/lecture_detail.html'
    context_object_name = 'lecture'

    def get(self, request, *args, **kwargs):
        lecture = self.get_object()
        context = {'lecture': lecture, 'user': request.user}
        return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureDeleteView(DeleteView):
    model = Lecture
    success_url = reverse_lazy('course_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)


@method_decorator([login_required, teacher_required], name='dispatch')
class TaskCreateView(CreateView):
    model = Task
    template_name = 'app/task_create.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('course_list')

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['pk'])
        form = self.form_class(initial={'course': course})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.course = Course.objects.get(pk=kwargs['pk'])
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        message = form.errors
        return render(request, self.template_name, {'form': form, 'message': message})


@method_decorator([login_required], name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'app/task_detail.html'
    context_object_name = 'task'

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        context = {'task': task, 'user': request.user}
        return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('course_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)