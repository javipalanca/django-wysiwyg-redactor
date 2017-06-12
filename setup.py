import os
from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-wysiwyg-redactor',
    version='0.5.1',
    description='django-wysiwyg-redactor is a lightweight responsive wysiwyg editor for Django',
    long_description=readme,
    author="Douglas Miranda",
    author_email='douglasmirandasilva@gmail.com',
    url='https://github.com/douglasmiranda/django-wysiwyg-redactor',
    license='MIT',
    packages=['redactor'],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',        
    ],
    keywords='django,admin,wysiwyg,editor,redactor,redactorjs',
)
