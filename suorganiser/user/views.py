from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.urls import reverse_lazy
from .utils import MailContextViewMixin, ProfileGetObjectMixin
from .forms import UserCreationForm, ResendActivationEmailForm, ProfileForm
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.messages import success, error
from django.views.decorators.cache import never_cache
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from .models import Profile
from .decorators import class_login_required
from django.shortcuts import get_object_or_404


class DisableAccount(View):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = ('user/user_confirm_delete.html')

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request, 
            self.template_name)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request):
        user = get_user(request)
        user.set_unusable_password()
        user.is_active = False
        user.save()
        logout(request)
        return redirect(self.success_url)

class CreateAccount(MailContextViewMixin, View):
    form_class = UserCreationForm
    success_url = reverse_lazy("dj-auth:create_done")
    template_name = "user/user_create.html"
    
    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()}
        )
    
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save(**self.get_save_kwargs(request))
            if bound_form.mail_sent:
                return redirect(self.success_url)
            else:
                errs = bound_form.non_field_errors()
                for err in errs:
                    error(request, err)
                return redirect('dj-auth:resend_activation')
        return TemplateResponse(
            request, 
            self.template_name,
            {'form': bound_form}
        )

class ActivateAccount(View):
    success_url = reverse_lazy("dj-auth:login")
    template_name = "user/user_activate.html"

    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (user is not None and token_generator.check_token(user, token)):
            user.is_active = True
            user.save()
            success(
                request,
                'User Activated! '
                'You may now login.')
            return redirect(self.success_url)
        else:
            return TemplateResponse(
                request,
                self.template_name
            )

class ResendActivationEmail(MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy("dj-auth:login")
    template_name = "user/resend_activation.html"

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()}
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(**self.get_save_kwargs(request))
            if (user is not None and not bound_form.mail_sent):
                errs = (bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                if errs:
                    bound_form.errors.pop("__all__")
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'form': bound_form})
        success(
            request,
            'Activation Email Sent!')
        return redirect(self.success_url)


@class_login_required
class ProfileDetail(ProfileGetObjectMixin, View):
    template_name = "user/profile_detail.html"

    def get(self, request):
        profile = self.get_object(request)
        return render(
            request,
            self.template_name,
            {'profile': profile}
        )


@class_login_required
class ProfileUpdate(ProfileGetObjectMixin, View):
    form_class = ProfileForm
    model = Profile
    template_name = "user/profile_form_update.html"
    success_url = reverse_lazy("dj-auth:profile")

    def get(self, request):
        profile = get_object_or_404(
            Profile,
            user = get_user(request))
        context = {
            'form': self.form_class(instance = profile),
            'profile': profile}
        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request):
        profile = get_object_or_404(
            Profile,
            user = get_user(request))
        bound_form = self.form_class(request.POST, request.FILES, instance = profile)
        if bound_form.is_valid():
            bound_form.save()
            return redirect(self.success_url)
        else:
            context = {
            'form': bound_form,
            'profile': profile}
            return render(
                request,
                self.template_name,
                context
            )


class PublicProfileDetail(View):

    def get(self, request, slug):
        profile = get_object_or_404(
            Profile,
            slug__iexact = slug)
        return render(
            request,
            "user/profile_detail.html",
            {'profile': profile},
        )