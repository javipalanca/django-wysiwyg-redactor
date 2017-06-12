from django.db.models import TextField
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from redactor.widgets import RedactorEditor


class RedactorField(TextField):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('redactor_options', {})
        upload_to = kwargs.pop('upload_to', '')
        allow_file_upload = kwargs.pop('allow_file_upload', True)
        allow_image_upload = kwargs.pop('allow_image_upload', True)
        self.widget = RedactorEditor(
            redactor_options=options,
            upload_to=upload_to,
            allow_file_upload=allow_file_upload,
            allow_image_upload=allow_image_upload
        )
        super(RedactorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)

        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = self.widget
        return super(RedactorField, self).formfield(**defaults)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^redactor\.fields\.RedactorField"])
