import datetime
import os
import csv

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q as __
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import *

from .forms import *
from .utils import *


def templates(temp: str):
    return "temp_/{}.html".format(temp)


class AssistantLanding(TemplateView):
    template_name = templates('landing')

    def get_context_data(self, *args, **kwargs):
        context = super(AssistantLanding, self).get_context_data(*args, **kwargs)
        a = list(range(20))
        class_ = ClassName.objects.all().count()
        student = UserData.objects.all().exclude(__(user__username__contains='admin'))
        context['loop'] = a
        context['class'] = class_
        context['student'] = student
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AssistantLanding, self).dispatch(request, *args, **kwargs)


class SeeAllFiles(ListView):
    model = Files
    context_object_name = 'files'
    template_name = templates('list_')

    def get_queryset(self):
        get_date = self.request.GET.get('date')
        model = self.model
        return model.objects.filter(class_name__link=self.kwargs['link']).filter(
            __(time_stamp__date=get_date)) if get_date else model.objects.filter(class_name__link=self.kwargs['link'])

    def get_context_data(self, **kwargs):
        context = super(SeeAllFiles, self).get_context_data(**kwargs)
        class_ = ClassName.objects.get(link=self.kwargs['link'])

        context['class'] = class_
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(SeeAllFiles, self).dispatch(request, *args, **kwargs)


class DeleteFile(View):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        item = Files.objects.get(pk=kwargs['item_pk'])
        messages.info(self.request, f"Item {item} has been deleted")
        item.delete()

        return redirect(reverse('assist:file-class', kwargs={'link': kwargs['link']}))

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False)))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteFile, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@method_decorator(
    user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
def download_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fp:
            response = HttpResponse(fp.read(), content_type='application/file')
            response['Content-Disposition'] = f"inline; filename={os.path.basename(file_path)}"
            return response
    raise Http404


class QRGeneratedList(ListView):
    model = GenerateQRCode
    template_name = templates('qr_list')
    context_object_name = 'qrcodes'

    def get_queryset(self):
        model = self.model
        class_name = ClassName.objects.get(link=self.kwargs['link'])
        query = model.objects.filter(class_name=class_name).order_by('-pk')
        return query

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(QRGeneratedList, self).dispatch(request, *args, **kwargs)


class PresenceRecap(ListView):
    template_name = templates('recaps')
    model = Recap
    context_object_name = 'recaps'

    def get_queryset(self):
        """ my class only """
        model = self.model
        get_code = GenerateQRCode.objects.get(qr_code=self.kwargs['qr_code'])
        return model.objects.filter(qr=get_code)

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(PresenceRecap, self).dispatch(request, *args, **kwargs)


class QRCodeView(View):
    def get(self, *args, **kwargs):
        file = GenerateQRCode.objects.filter(qr_img=f"qr/{self.kwargs['name']}")
        if not file:
            messages.warning(self.request, 'file not found')
            return redirect(reverse('assist:generated-qr', kwargs={'link': self.kwargs['link']}))
        img = open(os.path.join(settings.MEDIA_ROOT, file[0].qr_img.name), 'rb').read()
        return HttpResponse(img, content_type='image/png')

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(QRCodeView, self).dispatch(request, *args, **kwargs)


#
# class CreateClass(CreateView):
#     template_name = 'temp_/create.html'
#     form_class = ClassCreationForms
#     model = ClassName
#
#     def form_valid(self, form):
#         return super(CreateClass, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(CreateClass, self).get_context_data(**kwargs)
#         context['class_list'] = class_list
#
#         return context

class MyClassList(ListView):
    model = ClassName
    template_name = templates('class_list')
    context_object_name = 'classes'

    def get_queryset(self):
        model = self.model
        return model.objects.filter(__(pr=self.request.user) | __(creator=self.request.user)).distinct()

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(MyClassList, self).dispatch(request, *args, **kwargs)


class MyClass(DetailView):
    model = ClassName
    template_name = templates('my_class')
    slug_field = 'link'
    slug_url_kwarg = 'link'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super(MyClass, self).get_context_data(**kwargs)
        qr_active = GenerateQRCode.objects.filter(class_name__link=self.kwargs['link'])

        context['class_list'] = class_list
        context['course_list'] = course_list
        context['links'] = qr_active if qr_active.exists() else None
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(MyClass, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('assist:my-class-list')


class CreateClass(CreateView):
    form_class = CreateClassForms
    template_name = templates('create')
    success_url = reverse_lazy('assist:my-class-list')

    def form_valid(self, form):
        start = self.request.POST.get('start')
        end = self.request.POST.get('end')
        class_ = self.request.POST.get('class')
        gen = self.request.POST.get('gen')
        course = self.request.POST.get('course')

        if not class_ or not start or not end or not course:
            messages.warning(self.request, 'Mohon lengkapi data dengan benar')
            return redirect(reverse('assist:create-class'))
        else:
            class_ = class_list[int(class_) - 1]
            course = course_list[int(course) - 1]

        name, link = set_class_name(start, end, class_, gen, course)

        code = slug_generator(10)
        code_list = [c.unique_code for c in ClassName.objects.all()]
        code = check_slug(code, code_list, 10)

        form.instance.name = name
        form.instance.link = link
        form.instance.unique_code = code
        form.instance.creator = self.request.user
        return super(CreateClass, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateClass, self).get_context_data(**kwargs)

        context['class_list'] = class_list
        context['course_list'] = course_list
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateClass, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/')
def update_class_detail(request, link):
    form_class = CreateClassForms
    if request.method == 'POST':
        lecture = request.POST.get('lecture')
        start = request.POST.get('start')
        class_ = request.POST.get('class')
        end = request.POST.get('end')
        gen = request.POST.get('gen')
        course = request.POST.get('course')

        class_name = ClassName.objects.get(link=link)
        form = form_class(request.POST or None, instance=class_name)

        if not start or not class_ or not course or not end:
            messages.warning(request, 'Mohon lengkapi data dengan benar')
            return redirect(reverse('assist:my-class', args=[link]))
        else:
            class_ = class_list[int(class_) - 1]
            course = course_list[int(course) - 1]

        name, link = set_class_name(start, end, class_, gen, course)

        form.instance.name = name
        form.instance.link = link
        form.instance.lecture_name = lecture
        form.save()
    return redirect(reverse('assist:my-class', kwargs={'link': link}))


class GenerateQRCodeView(CreateView):
    model = GenerateQRCode
    template_name = templates('qr_generate')
    slug_url_kwarg = 'link'
    slug_field = 'link'
    form_class = GenerateQRCodeForms
    query_pk_and_slug = True

    def get_success_url(self):
        return reverse('assist:generated-qr', kwargs={'link': self.kwargs['link']})

    def form_valid(self, form):
        valid_until = timezone.now() + datetime.timedelta(minutes=20) if form.cleaned_data['valid_until'] is None else \
            form.cleaned_data['valid_until']
        code = slug_generator(16)
        get_all_code = [x.qr_code for x in GenerateQRCode.objects.all()]
        code = check_slug(code, get_all_code, 16)
        class_ = ClassName.objects.get(link=self.kwargs['link'])

        form.instance.valid_until = valid_until
        form.instance.qr_code = code
        form.instance.class_name = class_
        form.instance.creator = self.request.user
        return super(GenerateQRCodeView, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        today = timezone.now().date()
        latest_gen = GenerateQRCode.objects.filter(class_name__link=self.kwargs['link'], created__date=today)
        if latest_gen:
            messages.info(request, 'Kode Qr tidak bisa di buat 2 di hari yang sama!')
            return redirect(reverse('assist:generated-qr', kwargs={'link': self.kwargs['link']}))
        return super(GenerateQRCodeView, self).dispatch(request, *args, **kwargs)


class JoinAssistantClas(View):
    def get(self, *args, **kwargs):
        return render(self.request, templates('join_class'))

    def post(self, *args, **kwargs):
        code = self.request.POST.get('class_code')
        get_class = ClassName.objects.filter(unique_code=code)
        if not get_class:
            messages.warning(self.request, 'Kelas dengan kode {} tidak terdaftar'.format(code))
            return redirect('assist:join-class')
        get_class = get_class[0]
        pr_list = [user for user in get_class.pr.all()]
        if get_class.creator == self.request.user:
            messages.warning(self.request, "Kamu adalah PJ kelas ini maka tidak bisa sebgai asisten!")
            return redirect('assist:join-class')
        if self.request.user in pr_list:
            messages.info(self.request, 'Kamu sudah terdaftar sebagai assisten di kelas ini')
            return redirect('assist:join-class')
        get_class.pr.add(self.request.user)
        get_class.save()

        messages.info(self.request, f'Kamu sekarang terdaftar asisten kelas {get_class.name}')
        return redirect('assist:join-class')

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(JoinAssistantClas, self).dispatch(request, *args, **kwargs)


class AssistantChangeUsername(View):
    form_class = UserChangeDataForms

    def get(self, *args, **kwargs):
        return render(self.request, templates('c_log'), {'form': self.form_class()})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST or None, instance=self.request.user)
        username_list = User.objects.filter(username=self.request.POST.get('username'))
        if username_list:
            if username_list[0].username == self.request.user.username:
                messages.warning(self.request, "username sama dengan yang sekarang")
            else:
                messages.warning(self.request,
                                 "username '{}' tidak tersedia!".format(self.request.POST.get('username')))
            return redirect('assist:change-username')
        if form.is_valid():
            messages.info(self.request, 'Username anda berhasil di ubah!')
            form.save()
        else:
            messages.warning(self.request, 'Username anda tidak dapat di Ubah!')

        return redirect('assist:change-username')

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AssistantChangeUsername, self).dispatch(request, *args, **kwargs)


class AssistantChangePassword(PasswordChangeView):
    template_name = templates('c_log')
    success_url = reverse_lazy('assist:landing')

    def get_success_url(self):
        messages.info(self.request, 'Data anda berhasil di Ubah!')
        return self.success_url

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AssistantChangePassword, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.is_staff and (u.user.is_controller if hasattr(u, 'user') else False), '/')
def recaps_csv(request, link, qr_code):
    if request.method == "POST":
        generated_qr = GenerateQRCode.objects.get(qr_code=qr_code)
        response = HttpResponse('')
        response['Content-Disposition'] = f'attachment; filename=rekap_presensi_{generated_qr.stamp()}.csv'
        recaps = Recap.objects.filter(qr=generated_qr)
        writer = csv.writer(response)
        writer.writerow(['no', 'nim', 'nama', 'kelas', 'time_stamp'])
        for index, recap in enumerate(recaps):
            writer.writerow([int(index + 1), recap.user.user.nim, f"{recap.user.first_name} {recap.user.last_name}", recap.qr.class_name, recap.stamp()])
        return response
    return redirect(reverse('assist:recaps', kwargs={'link': link, 'qr_code': qr_code}))
