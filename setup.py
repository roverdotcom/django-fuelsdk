from setuptools import setup
from setuptools import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings

        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                },
            },
            INSTALLED_APPS=['django_fuelsdk']
        )

        from django.core.management import call_command
        call_command('test', 'django_fuelsdk')


setup(
    name='django-fuelsdk',
    version='0.2',
    description='Django wrapper for the ExactTarget FuelSDK.',
    long_description=open('README.md').read(),
    author='Johannas Heller',
    author_email='johann@rover.com',
    license='MIT',
    url='https://github.com/roverdotcom/django-fuelsdk',
    packages=['django_fuelsdk'],
    keywords=['fuelsdk', 'email', 'django'],
    classifiers=[
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    install_requires=[
        'FuelSDK',
    ],
    cmdclass={'test': TestCommand}
)
