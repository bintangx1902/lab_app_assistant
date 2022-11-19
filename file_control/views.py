from django.shortcuts import render, redirect, reverse
from .forms import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.apps import apps


ClassName = apps.get_model('presence', 'ClassName')

def templates(name: str):
    return f"file/{name}.html"


class UploadFile(CreateView):
    model = Files
    template_name = templates('upload')
    form_class = FileUploadForms

    def get_success_url(self):
        return reverse('file:upload')

    def form_valid(self, form):
        form.instance.user = self.request.user
        get_class = ClassName.objects.get(unique_code=self.request.POST.get('class_'))
        form.instance.class_name = get_class
        return super(UploadFile, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UploadFile, self).get_context_data(**kwargs)
        my_class = self.request.user.stud.all()

        context['my_class'] = my_class
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFile, self).dispatch(request, *args, **kwargs)


class MyFiles(ListView):
    model = Files
    template_name = templates('list')
    context_object_name = 'files'

    def get_queryset(self):
        model = self.model
        return model.objects.filter(user=self.request.user)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(MyFiles, self).dispatch(request, *args, **kwargs)
