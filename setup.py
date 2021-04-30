# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'rabbitmq_admin/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


install_requires = [
    'requests>=2.7.0',
    'six>=1.8.0'
]
tests_require = [
    'coverage>=4.0',
    'flake8>=2.2.0',
    'pika>=0.10.0',
    'mock>=1.0.1',
    'nose>=1.3.0']
docs_require = [
    'Sphinx>=1.2.2',
    'sphinx_rtd_theme']

extras_require = {
    'test': tests_require,
    'packaging': ['wheel'],
    'docs': docs_require,
}

everything = set(install_requires)
for deps in extras_require.values():
    everything.update(deps)
extras_require['all'] = list(everything)

setup(
    name='rabbitmq-admin',
    version=get_version(),
    description='A python interface for the RabbitMQ Admin HTTP API',
    long_description=open('README.rst').read(),
    url='https://github.com/ambitioninc/rabbitmq-admin',
    author='Micah Hausler',
    author_email='opensource@ambition.com',
    keywords='RabbitMQ, AMQP, admin',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    zip_safe=False,
)
