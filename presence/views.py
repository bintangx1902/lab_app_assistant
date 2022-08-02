import datetime, pytz
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.sites.models import Site
from .forms import *


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


@login_required(login_url='/accounts/login/')
def join_class(request):
    if request.method == 'POST':
        code = request.POST['class_code']
        get_class = ClassName.objects.filter(unique_code=code)
        if not get_class:
            messages.error(request, 'Kode Kelas Tidak Ditemukan')
            return redirect('presence:join-class')
        user = get_object_or_404(User, pk=request.user.pk)

    return render(request, 'presence/join_class.html')


@login_required(login_url='/accounts/login/')
def complete_data(request):
    form = UserCompletionForms()
    e_form = UserDataCompleteForms()
    extend = UserData.objects.filter(user=request.user)
    if extend:
        extend = get_object_or_404(UserData, user=request.user)
        if request.method == 'POST':
            pass

    context = {
        'form': form,
        'e_form': e_form
    }
    return render(request, 'presence/forms.html', context=context)
