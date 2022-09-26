from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q as __
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import *

from .forms import *


def templates(temp: str):
    return f'presence/{temp}.html'


class LandingView(View):
    def get(self, *args, **kwargs):
        return render(self.request, templates('mhs_landing'))

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        get_user = self.request.user
        return super(LandingView, self).dispatch(request, *args, **kwargs)


class JoinClass(View):
    def get(self, *args, **kwargs):
        return render(self.request, templates('join_class'))

    def post(self, *args, **kwargs):
        code = self.request.POST['class_code']
        get_class = ClassName.objects.filter(unique_code=code)
        if not get_class:
            messages.error(self.request, 'Kode Kelas Tidak Ditemukan')
            return redirect('presence:join-class')
        get_class = get_class[0]
        user = get_object_or_404(User, pk=self.request.user.pk)
        """ checking join is creator or not """
        if user == get_class.creator:
            messages.info(self.request, "Kamu tidak bisa menjadi murid kelas sekaligus penanggung jawab!")
            return redirect('presence:join-class')

        if get_class in user.stud.all():
            messages.info(self.request, f"Kamu sudah masuk kedalam kelas '{get_class.name}'")
            return redirect('presence:join-class')

        get_class.students.add(self.request.user)
        get_class.save()

        messages.info(self.request, f"Kamu sudah berhasil masuk kedalam kelas {get_class.name}")
        return redirect("presence:join-class")

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(user_passes_test(lambda u: (u.user if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(JoinClass, self).dispatch(request, *args, **kwargs)


class DataComplement(View):
    form_class = UserCompletionForms
    e_form_class = UserDataCompleteForms
    model = UserData
    template_name = templates('forms')

    def get(self, *args, **kwargs):
        form = self.form_class(instance=self.request.user)
        get_data = self.model.objects.filter(user=self.request.user)
        e_form = self.e_form_class(instance=self.request.user.user) if get_data else UserDataCompleteForms()

        context = {
            'form': form,
            'e_form': e_form
        }

        return render(self.request, self.template_name, context=context)

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST or None, self.request.FILES or None, instance=self.request.user)
        get_data = self.model.objects.filter(user=self.request.user)
        e_form = self.e_form_class(self.request.POST or None, self.request.FILES or None,
                                       instance=self.request.user.user) if get_data else UserDataCompleteForms(
            self.request.POST or None, self.request.FILES or None)

        if form.is_valid():
            form.save()
            messages.info(self.request, 'Data akun anda berhasil di update')

        if e_form.is_valid():
            phone = e_form.cleaned_data['phone_number']
            nim = e_form.cleaned_data['nim']

            get_user_data = UserData.objects.filter(user=self.request.user)
            if not get_user_data:
                instance = UserData(
                    user=self.request.user,
                    nim=nim,
                    phone_number=phone
                )

            else:
                instance = get_user_data[0]
                instance.phone_number = phone
                instance.nim = nim

            instance.save()
            messages.info(self.request, 'Profile anda berhasil di update')
        return redirect('presence:complete-data')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(DataComplement, self).dispatch(request, *args, **kwargs)


class ClassList(ListView):
    model = ClassName
    context_object_name = 'classes'
    template_name = templates('class_list')

    def get_queryset(self):
        model = self.model
        return model.objects.filter(students=self.request.user)

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(user_passes_test(lambda u: (u.user if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ClassList, self).dispatch(request, *args, **kwargs)


class Presence(View):
    def get(self, *args, **kwargs):
        return render(self.request, templates('cam'))

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(user_passes_test(lambda u: (u.user if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Presence, self).dispatch(request, *args, **kwargs)


class UploadFileByClass(CreateView):
    model = Files
    slug_url_kwarg = 'link'
    slug_field = 'link'
    form_class = UploadFileForms
    query_pk_and_slug = True
    template_name = templates('upload')

    def get_success_url(self):
        return reverse('presence:file-list-class', kwargs={'link': self.kwargs['link']})

    def form_valid(self, form):
        class_ = ClassName.objects.get(link=self.kwargs['link'])
        form.instance.user = self.request.user
        form.instance.class_name = class_
        return super(UploadFileByClass, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileByClass, self).dispatch(request, *args, **kwargs)


class FileListClass(ListView):
    model = Files
    template_name = templates('file_list_class')
    context_object_name = 'files'

    def get_queryset(self):
        get_date = self.request.GET.get('date')
        model = self.model
        return model.objects.filter(class_name__link=self.kwargs['link']).filter(
            __(time_stamp__date=get_date)) if get_date else model.objects.filter(class_name__link=self.kwargs['link'])

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(FileListClass, self).dispatch(request, *args, **kwargs)


class MyPresenceRecaps(ListView):
    model = Recap
    template_name = templates('recaps')
    context_object_name = 'recaps'

    def get_queryset(self):
        model = self.model
        return model.objects.filter(user=self.request.user, qr__class_name__link=self.kwargs['link'])

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(MyPresenceRecaps, self).dispatch(request, *args, **kwargs)
