from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import *
from django.http import HttpResponse, Http404
import os
from django.conf import settings
import string
from .forms import *
from .utils import slug_generator, check_slug
from django.contrib.auth.models import User

class_list = [f"Kelas {char}" for char in string.ascii_uppercase]


class AssistantLanding(TemplateView):
    template_name = 'temp_/landing.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AssistantLanding, self).get_context_data(*args, **kwargs)
        a = list(range(20))
        context['loop'] = a
        return context


class SeeAllFiles(ListView):
    model = Files
    context_object_name = 'files'
    template_name = 'temp_/list_.html'

    def get_queryset(self):
        return self.model.objects.all()

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(SeeAllFiles, self).dispatch(request, *args, **kwargs)


def download_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fp:
            response = HttpResponse(fp.read(), content_type='application/file')
            response['Content-Disposition'] = f"inline; filename={os.path.basename(file_path)}"
            return response
    raise Http404


class PresenceRecap(ListView):
    template_name = ''
    model = Recap

    def get_queryset(self):
        """ my class only """
        model = self.model
        get_mine = self.request.GET.get
        query = model.objects.filter(
            user=self.request.user,
            class_name=get_mine
        )

        return query


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


class MyClass(DetailView):
    model = ClassName
    template_name = 'temp_/my_class.html'
    slug_field = 'link'
    slug_url_kwarg = 'link'
    context_object_name = 'class'


def create_class(request):
    # form = ClassCreationForms()
    if request.method == 'POST':
        # form = ClassCreationForms(request.POST or None, request.FILES or None)
        start = request.POST['start']
        end = request.POST['end']
        class_ = request.POST.get('class')
        gen = request.POST.get('gen')

        if not class_ or not start or not end:
            return redirect(reverse('assist:create-class'))
        else:
            class_ = class_list[int(class_) - 1]
        name = f"{class_} {gen} Jam {start}-{end}"
        code = slug_generator(10)
        code_list = [c.unique_code for c in ClassName.objects.all()]
        code = check_slug(code, code_list, 10)

        c_name = ClassName(
            name=name,
            link=name.replace(' ', '-'),
            unique_code=code,
            creator=request.user
        )
        c_name.save()
        c_name.save(using='backup')

        """ class name backup """
        bc_user = User.objects.using('backup').get(pk=request.user.id)
        bc_class = ClassName.objects.using('backup').get(pk=c_name.pk)
        bc_class.pr.add(bc_user)

        return redirect(reverse('assist:landing'))
        # print(class_list[int(class_)-1])

    context = {
        'class_list': class_list,
        # 'form': form
    }

    return render(request, 'temp_/create.html', context)


def delete_class(request, link):
    if request.method == "POST":
        model = get_object_or_404(ClassName, link=link)
        model.delete()
        bc_model = model.objects.using('backup').get(link=link)
        bc_model.delete()

    return render(request, 'temp_/delete.html')


def backup(request):
    if request.method == 'POST':
        database = [User, Recap, Files, GenerateQRCode, UserData]
        for db in database:
            db_temp = db.objects.all()
            if db_temp:
                for db_save in db_temp:
                    db_save.save(using='backup')

    return render(request, 'temp_/backup.html')
