from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q as __
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import *

from .forms import *
from .utils import *


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
        user = User.objects.get(pk=self.request.user.pk)
        data = self.model.objects.filter(user=self.request.user)
        context = {'user': user}
        if hasattr(self.request.user, 'user'):
            context['profile'] = data[0]

        return render(self.request, self.template_name, context=context)

    def post(self, *args, **kwargs):
        first_name = self.request.POST.get('f_name')
        last_name = self.request.POST.get('l_name')
        email = self.request.POST.get('email')
        nim = self.request.POST.get('nim')
        phone = self.request.POST.get('phone')

        get_data = self.model.objects.filter(user=self.request.user)
        nim_list = [x.nim for x in self.model.objects.all()]
        msg, check = check_nim(nim_list, nim)

        """ check nim first """
        if hasattr(self.request.user, 'user'):
            get_user = User.objects.get(pk=self.request.user.pk)
            if get_user.user.nim != nim:
                if check:
                    messages.warning(self.request, msg)
                    return redirect('presence:complete-data')

            instance = get_data[0]
            instance.nim = nim
            instance.phone_number = phone
            instance.save()
            messages.info(self.request, 'data nim dan nomor telepon telah disimpan!')

        else:
            if check:
                messages.warning(self.request, msg)
                return redirect('presence:complete-data')

            instance = UserData(
                user=self.request.user,
                nim=nim,
                phone_number=phone
            )
            instance.save()

        user = User.objects.get(pk=self.request.user.pk)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

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


class ResetPassword(View):
    template_name = templates('reset')
    model = [UserData, TokenToResetPassword, ResetPasswordRequest]

    def get(self, *args, **kwargs):
        token = self.model[1].objects.get(token=self.kwargs['token'])
        now = timezone.now()
        if now > token.valid_until:
            return HttpResponse(status=HTTPStatus.NOT_ACCEPTABLE)

        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        nim = self.request.POST.get('nim')
        pass1 = self.request.POST.get('password1')
        pass2 = self.request.POST.get('password2')
        token = get_object_or_404(self.model[1], token=kwargs['token'])

        get_nim = self.model[0].objects.filter(nim=nim)
        if not get_nim:
            messages.warning(self.request, f"NIM {nim} tidak terdata di sistem!")
            return redirect(reverse('presence:reset-password', kwargs={'token': self.kwargs['token']}))

        nim = get_nim[0]
        if pass1 != pass2:
            messages.warning(self.request, "password harus sama")
            return redirect(reverse('presence:reset-password', kwargs={'token': self.kwargs['token']}))

        passw = pass2
        user = User.objects.get(username=nim.user.username)
        user.set_password(passw)
        user.save()

        to_update = ResetPasswordRequest.objects.get(user=nim.user, token=token, is_done=False)
        to_update.is_done = True
        to_update.save()

        messages.info(self.request, f"Password berhasil di ganti!")
        return redirect(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if not token:
            raise Http404
        # find token
        token = self.model[1].objects.filter(token=token)
        if not token:
            raise Http404("token not found")
        return super(ResetPassword, self).dispatch(request, *args, **kwargs)


class SeeMyScoreView(ListView):
    model = StudentScore
    template_name = templates('my-score')
    context_object_name = 'scores'

    def get_queryset(self):
        model = self.model
        get_classification = self.request.GET.get('class')
        if get_classification is not None:
            try:
                get_classification = int(get_classification)
            except Exception:
                raise Http404
            if int(get_classification) > 6:
                get_classification = 6
        get_classification = classification[int(get_classification) - 1] if get_classification is not None else None
        return model.objects.filter(user=self.request.user,
                                    classification=get_classification) if get_classification else model.objects.filter(
            user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SeeMyScoreView, self).get_context_data(**kwargs)
        *_, score = total_average(self.get_queryset(), models.Avg).values()

        context['class'] = classification
        context['score'] = score
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(SeeMyScoreView, self).dispatch(request, *args, **kwargs)


class RequestPasswordReset(View):
    model = ResetPasswordRequest
    template_name = templates('request-reset')

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        nim = get_object_or_404(UserData, nim=self.request.POST.get('NIM'))
        if check_request(self.model, nim.user):
            return
        instance = self.model(user=nim.user)
        instance.save()
        return redirect(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
