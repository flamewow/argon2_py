#!/usr/bin/env python

"""Installer for Argon2 Python bindings"""

import sys
import platform

from setuptools import setup, Extension

INCLUDES = []
LIBRARY_DIRS = []
CFLAGS = []


if sys.platform.startswith('linux'):
    DEFINE_MACROS = [('HAVE_CLOCK_GETTIME', '1'),
                     ('HAVE_LIBRT', '1'),
                     ('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_STRUCT_SYSINFO', '1'),
                     ('HAVE_STRUCT_SYSINFO_MEM_UNIT', '1'),
                     ('HAVE_STRUCT_SYSINFO_TOTALRAM', '1'),
                     ('HAVE_SYSINFO', '1'),
                     ('HAVE_SYS_SYSINFO_H', '1'),
                     ('_FILE_OFFSET_BITS', '64')]
    LIBRARIES = []
    CFLAGS.append('-O2')
elif sys.platform.startswith('win32'):
    DEFINE_MACROS = [('inline', '__inline')]
    LIBRARY_DIRS = [r'c:\OpenSSL-Win32\lib']
    LIBRARIES = ['libeay32', 'advapi32']
    INCLUDES = [r'c:\OpenSSL-Win32\include', 'argon2-windows-stubs/include']
elif sys.platform.startswith('darwin') and platform.mac_ver()[0] < '10.6':
    DEFINE_MACROS = [('HAVE_SYSCTL_HW_USERMEM', '1')]
    LIBRARIES = []

else:
    DEFINE_MACROS = [('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_SYSCTL_HW_USERMEM', '1')]
    LIBRARIES = ['c_argon2']

ARGON2_MODULE = Extension(
    '_argon2',
    sources=[
        './src/argon2_py.c',
        './phc-winner-argon2/src/argon2.c',
        './phc-winner-argon2/src/core.c',
        './phc-winner-argon2/src/encoding.c',
        './phc-winner-argon2/src/ref.c',
        './phc-winner-argon2/src/thread.c',
        './phc-winner-argon2/src/blake2/blake2b.c',
    ],
    include_dirs=[
        './phc-winner-argon2',
        './phc-winner-argon2/src',
        './phc-winner-argon2/src/blake2',
    ] + INCLUDES,
    define_macros=[('HAVE_CONFIG_H', None)] + DEFINE_MACROS,
    extra_compile_args=CFLAGS,
    library_dirs=LIBRARY_DIRS,
    libraries=LIBRARIES)

setup(
    name='argon2',
    version='0.1.10',
    description='Bindings for the argon2 password hasher',
    author='Moroz Ilya',
    author_email='flamewowilia@gmail.com',
    url='https://github.com/flamewow/argon2_py',
    py_modules=['argon2'],
    ext_modules=[ARGON2_MODULE],
    packages=['phc-winner-argon2'],

    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
    ),
    license="CC0",

    test_suite='tests',
)
