from setuptools import setup

import setuptools
from setuptools import setup

setup(
    name='epic_mpl',
    version='0.1',
    url='https://github.com/samthiele/epic',
    license='MIT',
    author='Sam Thiele',
    author_email='sam.thiele01@gmail.com',
    description='Simple image point-picking with matplotlib.',
    long_description='Simply pick points using matplotlib.',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering"
        ],
    keywords='image point picking matplotlib',
    python_requires='>=3.6',
    install_requires=['numpy','matplotlib','easygui'],
    project_urls={  # Optional
            'Source': 'https://github.com/samthiele/epic',
        },
)