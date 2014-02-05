from setuptools import setup, find_packages

setup(
    name='django-fuelsdk',
    version="0.1",
    description='Django wrapper for the ExactTarget FuelSDK.',
    long_description=open('README.md').read(),
    author='Johannas Heller',
    author_email='johann@rover.com',
    maintainer='Johannas Heller',
    maintainer_email='johann@rover.com',
    license='MIT',
    url='https://github.com/roverdotcom/django-fuelsdk',
    download_url='https://github.com/roverdotcom/django-fuelsdk/releases',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
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
    ]
)
