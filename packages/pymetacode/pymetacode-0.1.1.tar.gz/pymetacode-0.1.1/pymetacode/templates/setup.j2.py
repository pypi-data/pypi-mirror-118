import os
import setuptools


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        content = f.read()
    return content


setuptools.setup(
    name='{{ package.name }}',
    version=read('VERSION').strip(),
    description='{{ package.description }}',
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",
    author='{{ package.author }}',
    author_email='{{ package.author_email }}',
    url='{{ package.urls.main }}',
    project_urls={
        "Documentation": '{{ package.urls.documentation }}',
        "Source": '{{ package.urls.source }}',
    },
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    license='BSD',
    keywords=[
        {%- if package.keywords %}{% for item in package.keywords %}
        "{{ item }}",
        {% endfor %}{% endif -%}
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        {%- if package.install_requires %}{% for item in package.install_requires %}
        "{{ item }}",
        {% endfor %}{% endif -%}
    ],
    extras_require={
        'dev': ['prospector'],
        'docs': ['sphinx', 'sphinx-rtd-theme'],
    },
    python_requires='>=3.7',
)
