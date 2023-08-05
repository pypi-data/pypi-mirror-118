from distutils.core import setup

setup(
    name='pytest_ver',
    packages=['pytest_ver'],
    version='0.0.1',
    license='MIT',
    description='Pytest module with Verification Report',
    author='JA',
    author_email='cppgent0@gmail.com',
    url='https://github.com/cppgent0/pytest-ver',
    download_url='https://github.com/cppgent0/pytest-ver/archive/refs/tags/v_0_0_1.tar.gz',
    keywords=['verification', 'pytest'],
    install_requires=[
        'reportlab',
        'pytest',
        'pytest-cov',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Acceptance',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
