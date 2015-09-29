import io, os.path, re, sys

from setuptools import setup

# environment markers require a recent setuptools and/or pip version
if sys.version_info >= (3, 3) or 'bdist_wheel' in sys.argv:
    install_requires = []
elif sys.version_info >= (3, 0):
    install_requires = ['ipaddress>=1.0.7']
else:
    install_requires = ['ipaddress>=1.0.6']

with io.open(os.path.join(os.path.dirname(__file__), 'urilib', '__init__.py'),
             encoding='utf8') as f:
    metadata = dict(re.findall(r"__([a-z]+)__ = '([^']+)", f.read()))

setup(
    name='urilib',
    version=metadata['version'],
    author='Thomas Kemmer, IGARASHI Masanao',
    author_email='tkemmer@computer.org, syoux2@gmail.com',
    url='https://github.com/masayuko/urilib/',
    license='MIT',
    description='Encode like brower does, Unicode-aware, scheme-agnostic replacement for urlparse',
    long_description=open('README.rst').read(),
    keywords='uri url urlparse urlsplit urljoin urldefrag',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['urilib'],
    install_requires=install_requires,
    extras_require={
        ':python_version == "2.7"': ['ipaddress>=1.0.6'],
        ':python_version == "3.2"': ['ipaddress>=1.0.7']
    },
    test_suite='tests'
)
