A lightweight wysiwyg editor for Django
=======================================

Screenshot
----------

.. image:: https://raw.githubusercontent.com/douglasmiranda/django-wysiwyg-redactor/master/screenshots/redactor.jpg

What's that
-----------------

*django-wysiwyg-redactor* is a text editor application for Django, using `Redactor WYSIWYG editor <https://imperavi.com/redactor/>`_

Dependency
----------

- `Pillow or PIL` # for image upload

Getting started
---------------

- Install *django-wysiwyg-redactor*:

``pip install django-wysiwyg-redactor``

- Add `'redactor'` to INSTALLED_APPS.

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'redactor',
        # ...
    )

- Add `url(r'^redactor/', include('redactor.urls'))`, to urls.py

.. code-block:: python

    urlpatterns = [
        # ...
        url(r'^redactor/', include('redactor.urls')),
        # ...
    ]


- Add default config in settings.py

.. code-block:: python

    REDACTOR_OPTIONS = {'lang': 'en'}
    REDACTOR_UPLOAD = 'uploads/'

More `redactor settings <http://imperavi.com/redactor/docs/settings/>`_.

Using in model
--------------

.. code-block:: python

    from django.db import models
    from redactor.fields import RedactorField

    class Entry(models.Model):
        title = models.CharField(max_length=250, verbose_name=u'Title')
        short_text = RedactorField(verbose_name=u'Text')

or use custom parameters:

.. code-block:: python

    short_text = RedactorField(
        verbose_name=u'Text',
        redactor_options={'lang': 'en', 'focus': True},
        upload_to='tmp/',
        allow_file_upload=True,
        allow_image_upload=True
    )

Using only in Django Admin
--------------------------

.. code-block:: python

    from django import forms
    from redactor.widgets import RedactorEditor
    from blog.models import Entry

    class EntryAdminForm(forms.ModelForm):
        class Meta:
            model = Entry
            widgets = {
               'short_text': RedactorEditor(),
            }

    class EntryAdmin(admin.ModelAdmin):
        form = EntryAdminForm

`RedactorEditor` takes the same parameters as `RedactorField`.

Using Plugins
-------------
`Download <http://imperavi.com/redactor/plugins/>`_ the plugin you want or `create a custom plugin <http://imperavi.com/redactor/docs/how-to-create-plugin/>`_.

Then:

.. code-block:: python

    from django.db import models
    from redactor.fields import RedactorField

    class Entry(models.Model):
        title = models.CharField(max_length=250, verbose_name=u'Title')
        short_text = RedactorField(
            verbose_name=u'Text',
            # for example, if you downloaded the 'table' plugin:
            redactor_options={'plugins': ['table']}
        )

OR (on settings.py):

.. code-block:: python

    REDACTOR_OPTIONS = {'lang': 'en', 'plugins': ['table']}

Important: if you set a plugin called "table", you must create/paste the "table.js" on **YOUR_STATIC_FILES_FOLDER/redactor/plugins/table.js**

Upload Handlers
---------------
SimpleUploader - The Standard Uploader. Will upload your file to REDACTOR_UPLOAD.

UUIDUploader - This handler will replace the original file name for an UUID.

DateDirectoryUploader - This handler saves the file in a directory based on the current server date.

Usage:

For example, if I want to use the DateDirectoryUploader handler, I will put this on settings.py:

.. code-block:: python

    REDACTOR_UPLOAD_HANDLER = 'redactor.handlers.DateDirectoryUploader'

Upload permissions
------------------
By default django-wysiwyg-redactor uses `staff_member_required` decorator from
`django.contrib.admin.views.decorators` package to control access to dispatch
method.

To use custom authentication decorator, set `REDACTOR_AUTH_DECORATOR` to
anything else, eg. if every authenticated user should have permissions to
upload files/images/etc.:

.. code-block:: python

    REDACTOR_AUTH_DECORATOR = 'django.contrib.auth.decorators.login_required'

File Storages
-------------
*django-wysiwyg-redactor* defaults to using the default media storage for your Django application.

This can be overridden to use a different storage backend with this settings.py variable:

.. code-block::

    REDACTOR_FILE_STORAGE = 'my_site.file_storages.StorageClass'

Information on writing a custom storage backend is `here in the Django documentation <https://docs.djangoproject.com/en/1.7/howto/custom-file-storage/>`_.

Other third-party libraries exist to provide storage backends for cloud object storages (e.g. `django-cumulus <https://github.com/django-cumulus/django-cumulus/>`_ for Rackspace/OpenStack or `django-storages <http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html>`_ for Amazon S3). For example, following should be enough to store all your files and images to Amazon S3, even if the rest of the application uses different storage.

.. code-block:: python

    REDACTOR_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = '...'
    AWS_SECRET_ACCESS_KEY = '...'
    AWS_STORAGE_BUCKET_NAME = '...'


NOTE: Soon we will have a better documentation.

Contributing
------------

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request =]

Made by robots, or what?
------------------------
Awesome people, you should see the `AUTHORS <https://github.com/douglasmiranda/django-wysiwyg-redactor/blob/master/AUTHORS>`_ file.

About the licensing
-------------------
You may want to see the `LICENSE <https://github.com/douglasmiranda/django-wysiwyg-redactor/blob/master/LICENSE>`_ file.
