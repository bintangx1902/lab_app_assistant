from django.shortcuts import render, redirect, reverse
from .forms import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class UploadFile(CreateView):
    model = Files
    template_name = 'file/upload.html'
    form_class = FileUploadForms

    def get_success_url(self):
        return reverse('file:upload')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UploadFile, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFile, self).dispatch(request, *args, **kwargs)


class MyFiles(ListView):
    model = Files
    template_name = 'file/list.html'
    context_object_name = 'files'

    def get_queryset(self):
        model = self.model
        return model.objects.filter(user=self.request.user)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(MyFiles, self).dispatch(request, *args, **kwargs)
