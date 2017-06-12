import json
from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.views.generic import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_str

from redactor.forms import ImageForm
from redactor.utils import import_class, is_module_image_installed

# deal with python3 basestring
try:
    unicode = unicode
except NameError:
    basestring = (str, bytes)
else:
    basestring = basestring


class RedactorUploadView(FormView):
    form_class = ImageForm
    http_method_names = ('post',)
    upload_to = getattr(settings, 'REDACTOR_UPLOAD', 'redactor/')
    upload_handler = getattr(settings, 'REDACTOR_UPLOAD_HANDLER',
                             'redactor.handlers.SimpleUploader')
    auth_decorator = getattr(settings, 'REDACTOR_AUTH_DECORATOR',
                             staff_member_required)
    if isinstance(auth_decorator, basestring):
        # Given decorator is string, probably because user can't import eg.
        # django.contrib.auth.decorators.login_required in settings level.
        # We are expected to import it on our own.
        auth_decorator = import_class(auth_decorator)

    @method_decorator(csrf_exempt)
    @method_decorator(auth_decorator)
    def dispatch(self, request, *args, **kwargs):
        if not is_module_image_installed():
            data = {
                'error': True,
                'message': _("ImproperlyConfigured: Neither Pillow nor PIL could be imported: No module named 'Image'")
            }
            return HttpResponse(json.dumps(data), status=400,
                                content_type='application/json')
        return super(RedactorUploadView, self).dispatch(request,
                                                        *args, **kwargs)

    def form_invalid(self, form):
        # TODO: Needs better error messages
        try:
            message = form.errors.values()[-1][-1]
        except:
            message = _('Invalid file.')
        data = {'error': True, 'message': message}
        return HttpResponse(json.dumps(data), status=400,
                            content_type='application/json')

    def form_valid(self, form):
        file_ = form.cleaned_data['file']
        handler_class = import_class(self.upload_handler)
        uploader = handler_class(file_,
                                 upload_to=self.kwargs.get('upload_to', None))
        uploader.save_file()
        file_name = force_str(uploader.get_filename())
        file_url = force_str(uploader.get_url())
        file_name_key = 'id' if self.form_class is ImageForm else 'name'
        data = {'url': file_url, file_name_key: file_name}
        return HttpResponse(json.dumps(data), content_type='application/json')
