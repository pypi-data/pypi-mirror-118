from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='oneaccount',
    version='1.0.0',
    description='One account python library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Oila Studio',
    author_email='manager@oneaccount.app',
    license='MIT',
    classifiers=classifiers,
    keywords='privacy, authentication, login, secure, signup',
    packages=find_packages(),
    install_requires=["requests==2.26.0"]
)