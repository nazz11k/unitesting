from django import forms
from app import models
from datetime import datetime


class CourseCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Course description'}))
    groups = forms.ModelMultipleChoiceField(queryset=models.Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        super(CourseCreateForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = models.Group.objects.all()

    class Meta:
        model = models.Course
        fields = ['name', 'description', 'groups']

    def save(self, commit=True):
        course = super(CourseCreateForm, self).save(commit=False)
        course.teacher = self.teacher
        if commit:
            course.save()
            self.save_m2m()
        return course


class CourseUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Course description'}))
    groups = forms.ModelMultipleChoiceField(queryset=models.Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.Course
        fields = ['name', 'description', 'groups']

    def save(self, commit=True):
        instance = super(CourseUpdateForm, self).save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class GroupCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Group name'}))

    class Meta:
        model = models.Group
        fields = ['name']

    def save(self, commit=True):
        group = super(GroupCreateForm, self).save(commit=False)
        group.save()
        return group


class LectureCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lecture name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Lecture description'}))
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(LectureCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Lecture
        fields = ['name', 'description', 'file']

    def save(self, commit=True):
        lecture = super(LectureCreateForm, self).save(commit=False)
        lecture.save()
        self.save_m2m()
        return lecture


class LectureUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lecture name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Lecture description'}))
    course = forms.ModelChoiceField(queryset=models.Course.objects.all(), widget=forms.Select(attrs={'class': 'pretty-input'}))
    file = forms.FileField(required=False)

    def __init__(self, teacher, *args, **kwargs):
        super(LectureUpdateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher
        self.fields['course'].queryset = models.Course.objects.filter(teacher=self.teacher)

    class Meta:
        model = models.Lecture
        fields = ['name', 'description', 'course', 'file']

    def save(self, commit=True):
        lecture = super(LectureUpdateForm, self).save(commit=False)
        lecture._teacher = self.teacher
        lecture.save()
        self.save_m2m()
        return lecture


class TaskCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task description'}))
    max_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Task max score'}))
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'class': 'form-control datetimepicker', 'placeholder': 'Task deadline', 'value': f'{datetime.now().strftime("%Y-%m-%d %H:%M")}'})
    )
    test_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Task
        fields = ['name', 'description', 'max_score', 'deadline', 'test_file']

    def save(self, commit=True):
        task = super(TaskCreationForm, self).save(commit=False)
        task.save()
        self.save_m2m()
        return task


class TaskUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Task name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-input', 'placeholder': 'Task description'}))
    max_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'pretty-input', 'placeholder': 'Task max score'}))
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'pretty-input', 'placeholder': 'Task deadline'}))
    test_file = forms.FileField()
    course = forms.ModelChoiceField(queryset=models.Course.objects.all(), widget=forms.Select(attrs={'class': 'pretty-input'}))

    def __init__(self, teacher, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher
        self.fields['course'].queryset = models.Course.objects.filter(teacher=self.teacher)

    class Meta:
        model = models.Task
        fields = ['name', 'description', 'max_score', 'deadline', 'test_file', 'course']

    def save(self, commit=True):
        task = super(TaskUpdateForm, self).save(commit=False)
        task._teacher = self.teacher
        task.save()
        self.save_m2m()
        return task


class SolutionForm(forms.ModelForm):
    solution = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-text', 'placeholder': 'Solution'}))

    def __init__(self, student, task, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)
        self.student = student
        self.task = task

    class Meta:
        model = models.Solution
        fields = ['solution']

