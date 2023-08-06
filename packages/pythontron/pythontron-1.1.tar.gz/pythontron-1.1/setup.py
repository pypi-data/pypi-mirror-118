from setuptools import setup

pytron_info = """
Pythontron.

Copyright © Makar Kuznetsov 2021. All rights reserved

License – GNU GPL.

See more information on Github.
"""

setup(
    name='pythontron',
    version='1.1',
    description='Python library for creating perceptrons.',
    long_description=pytron_info,
    url='http://github.com/HonestHacker123/pythontron',
    install_requires=['numpy'],
    packages=['pythontron'],
    author="Makar Kuznetsov",
    author_email='makar10kuznetsov@mail.ru',
    zip_safe=False
)
