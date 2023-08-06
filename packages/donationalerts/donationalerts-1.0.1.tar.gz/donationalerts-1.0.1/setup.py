from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='donationalerts',
    packages=['donationalerts'],  
    version='1.0.1',
    license='MIT',
    description='Handling your donation in real time',
    author='cxldxice', 
    author_email='cxldxfxtxre@gmail.com',
    url='https://github.com/cxldxice/donationalerts',
    long_description=long_description,
    long_description_content_type='text/markdown',

    keywords=['donation', 'handlers', 'alerts'],
    install_requires=[            # I get to this in a second
        'requests',
        'flask',
    ]
)
