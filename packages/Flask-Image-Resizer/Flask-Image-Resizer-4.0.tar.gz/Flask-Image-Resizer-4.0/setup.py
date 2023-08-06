from setuptools import setup

setup(

    name='Flask-Image-Resizer',
    version='4.0',
    description='Dynamic image resizing for Flask.',
    url='http://github.com/rustamlilala/Flask-Image-Resizer',
        
    author='Lala Rustamli',
    author_email='rustamlilala@gmail.com',
    license='BSD-3',

    packages=['flask_image_resizer'],

    install_requires=[

        'Flask>=0.9',
        'itsdangerous', # For Flask v0.9

        # We need either PIL, or the newer Pillow. Since this may induce some
        # dependency madness, I have created a module that should flatten that
        # out. See: https://github.com/mikeboers/Flask-Images/pull/10 for more.
        'PillowCase',
        
        'six',

    ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    tests_require=[
        'nose>=1.0',
    ],
    test_suite='nose.collector',

    zip_safe=False,
)
