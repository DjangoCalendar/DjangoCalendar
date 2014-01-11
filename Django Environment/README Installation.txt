1. Download Python from http://www.python.org/download/releases/2.7.3/
2. Install it.
3. Set PYTHONPATH = C:\Python27;C:\Python27\Lib\site-packages
4. Now you have installed Python on your computer.
5. Now Django Framework.
6. Download Django From https://www.djangoproject.com/download/1.5/tarball/
7. Unzip it and go to directory in it where is file setup.py
8. From command line (as Administrator) run command: py setup.py install
9. To verify that Django can be seen by Python, type python from your shell. Then at the Python prompt, try to import Django:
>>> import django
>>> print(django.get_version())
1.6
10. And now you have to setup a project.