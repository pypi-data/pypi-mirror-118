from django.contrib import admin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

csrf_protect_m = method_decorator(csrf_protect)


class PreferencesAdmin(admin.ModelAdmin):

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        Display single preferences object
        """
        model = self.model
        obj = model.singleton.get()
        return redirect(
            reverse(
                'admin:%s_%s_change' % (
                    model._meta.app_label, model._meta.model_name
                ),
                args=(obj.id,)
            )
        )
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """
        Disable additional save buttons
        """
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def has_add_permission(self, request):
        return False
