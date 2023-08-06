from setuptools import setup, find_packages

name = 'django-connection-pool'
version = '1.2.0'

setup(
    name=name,
    version=version,
    packages=find_packages(),
    install_requires=[
        "Django>=3.0.0,<4.0.0",
        "sqlalchemy>=1.4.20",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    license='GNU General Public License v3.0',
    author='Lee',
    author_email='canyun@live.com',
    description='django connection pool',
)
