from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import *
from .forms import *


def templates(temp: str):
    return f'presence/{temp}.html'


# def main_redirection(req):
#     # if req.GET:
#     #     link = req.GET.get('link')
#     #     link = InvitationLink.objects.filter(link=link)
#     #     if not link:
#     #         return redirect('dash:landing')
#     #     link = get_object_or_404(InvitationLink, link=link)
#     #     return reverse('dash:invitation', args=[link.link])
#
#     if req.user.is_authenticated:
#         get_user = UserExtended.objects.filter(user=req.user)
#         if not get_user:
#             return HttpResponseRedirect(reverse('dash:landing'))
#         get_user = get_object_or_404(UserExtended, user=req.user)
#
#         if get_user.agency:
#             if get_user.is_controller:
#                 return HttpResponseRedirect(reverse('dash:agency-dashboard', args=[get_user.agency.link]))
#             return HttpResponseRedirect(reverse('dash:user-dashboard', args=[get_user.agency.link]))
#         return redirect('/landfed')
#     return redirect('dash:landing')


class LandingView(View):
    def get(self, *args, **kwargs):
        return render(self.request, templates('mhs_landing'))

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        get_user = self.request.user
        return super(LandingView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
def join_class(request):
    user = UserData.objects.filter(user=request.user)
    if not user:
        messages.warning(request, "Kamu Belum Melengkapi Datamu!")
        return redirect('presence:complete-data')

    if request.method == 'POST':
        code = request.POST['class_code']
        get_class = ClassName.objects.filter(unique_code=code)
        if not get_class:
            messages.error(request, 'Kode Kelas Tidak Ditemukan')
            return redirect('presence:join-class')
        get_class = get_class[0]
        user = get_object_or_404(User, pk=request.user.pk)
        """ checking join is creator or not """
        if user == get_class.creator:
            messages.info(request, "Kamu tidak bisa menjadi murid kelas sekaligus penanggung jawab!")
            return redirect('presence:join-class')

        if get_class in user.stud.all():
            messages.info(request, f"Kamu sudah masuk kedalam kelas '{get_class.name}'")
            return redirect('presence:join-class')

        get_class.students.add(request.user)
        get_class.save()

        """ backup """
        bc_class = ClassName.objects.using('backup').get(unique_code=code)
        bc_user = User.objects.using('backup').get(username=request.user.username)
        bc_class.students.add(bc_user)
        bc_class.save(using='backup')

    return render(request, templates('join_class'))


@login_required(login_url='/accounts/login/')
def complete_data(request):
    form = UserCompletionForms(instance=request.user)
    get_data = UserData.objects.filter(user=request.user)
    e_form = UserDataCompleteForms(instance=request.user.user) if get_data else UserDataCompleteForms()

    if request.method == 'POST':
        form = UserCompletionForms(request.POST or None, request.FILES or None, instance=request.user)
        e_form = UserDataCompleteForms(request.POST or None, request.FILES or None,
                                       instance=request.user.user) if get_data else UserDataCompleteForms(
            request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            user = User.objects.using('backup').get(username=request.user.username)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save(using='backup')
            messages.info(request, 'Data akun anda berhasil di update')

        if e_form.is_valid():
            phone = e_form.cleaned_data['phone_number']
            nim = e_form.cleaned_data['nim']

            get_user_data = UserData.objects.filter(user=request.user)
            bc_user = User.objects.using('backup').get(pk=request.user.pk)
            if not get_user_data:
                instance = UserData(
                    user=request.user,
                    nim=nim,
                    phone_number=phone
                )

            else:
                instance = get_user_data[0]
                instance.phone_number = phone
                instance.nim = nim

            instance.save()
            instance.save(using='backup')
            messages.info(request, 'Data Profile anda berhasil di update')
        return redirect('presence:complete-data')

    context = {
        'form': form,
        'e_form': e_form
    }
    return render(request, templates('forms'), context=context)


class ClassList(ListView):
    model = ClassName
    context_object_name = 'classes'
    template_name = templates('class_list')

    def get_queryset(self):
        model = self.model
        return model.objects.filter(students=self.request.user)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ClassList, self).dispatch(request, *args, **kwargs)


class Presence(View):
    def get(self, *args, **kwargs):
        return render(self.request, templates('cam'))


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
        x = form.save()
        x.save(using='backup')
        return super(UploadFileByClass, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileByClass, self).dispatch(request, *args, **kwargs)


class FileListClass(View):
    def get(self, *args, **kwargs):
        return render(self.request, templates('file_list_class'))
