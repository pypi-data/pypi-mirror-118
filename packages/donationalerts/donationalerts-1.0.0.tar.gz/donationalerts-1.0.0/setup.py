from distutils.core import setup


setup(
    name='donationalerts',
    packages=['donationalerts'],  
    version='1.0.0',
    license='MIT',
    description='Handling your donation in real time',
    author='cxldxice', 
    author_email='cxldxfxtxre@gmail.com',
    url='https://github.com/cxldxice/donationalerts',

    keywords=['donation', 'handlers', 'alerts'],
    install_requires=[            # I get to this in a second
        'requests',
        'flask',
    ]
)
