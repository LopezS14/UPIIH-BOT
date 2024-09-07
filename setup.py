# setup.py
from setuptools import setup

setup(
    name='myapp',
    version='0.1',
    install_requires=[
        'streamlit==1.38.0',
        'numpy',
        'requests',
        'python-docx',
        'tensorflow',
        'nltk',
        'pydub',
        'playsound'
    ],
)
