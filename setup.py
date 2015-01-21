from distutils.core import setup

setup(
    name='django-multiqueryset',
    version='0.9',
    author='Tiago Queiroz',
    author_email='contato@tiago.eti.br',
    packages=['django_multiqueryset'],
    url='http://github.com/belimawr/django-multiqueryset.git',
    license='LGPLv2.1',
    description=' class to wrapper Django QuerySets and lists together providing slice and access to specific elements',
    long_description=open('README.rst').read(),
    install_requires=[],
)
