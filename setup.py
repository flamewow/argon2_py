#!/usr/bin/env python
from setuptools import setup, Extension

import sys
import platform

includes = []
library_dirs = []
extra_sources = []
CFLAGS = []


if sys.platform.startswith('linux'):
    define_macros = [('HAVE_CLOCK_GETTIME', '1'),
                     ('HAVE_LIBRT', '1'),
                     ('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_STRUCT_SYSINFO', '1'),
                     ('HAVE_STRUCT_SYSINFO_MEM_UNIT', '1'),
                     ('HAVE_STRUCT_SYSINFO_TOTALRAM', '1'),
                     ('HAVE_SYSINFO', '1'),
                     ('HAVE_SYS_SYSINFO_H', '1'),
                     ('_FILE_OFFSET_BITS', '64')]
    libraries = []
    CFLAGS.append('-O2')
elif sys.platform.startswith('win32'):
    define_macros = [('inline', '__inline')]
    library_dirs = ['c:\OpenSSL-Win32\lib']
    libraries = ['libeay32', 'advapi32']
    includes = ['c:\OpenSSL-Win32\include', 'argon2-windows-stubs/include']
    extra_sources = ['argon2-windows-stubs/gettimeofday.c']
elif sys.platform.startswith('darwin') and platform.mac_ver()[0] < '10.6':
    define_macros = [('HAVE_SYSCTL_HW_USERMEM', '1')]
    libraries = ['c_argon2']
else:
    define_macros = [('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_SYSCTL_HW_USERMEM', '1')]
    libraries = ['c_argon2']

_argon2_module = Extension('_argon2',
                    sources = ['./src/argon2_py.c',
                               './phc-winner-argon2/src/argon2.c',
                               './phc-winner-argon2/src/core.c',
                               './phc-winner-argon2/src/encoding.c',
                               './phc-winner-argon2/src/ref.c',
                               './phc-winner-argon2/src/thread.c',
                               './phc-winner-argon2/src/blake2/blake2b.c',],
                    include_dirs = ['./phc-winner-argon2',
                                    './phc-winner-argon2/src',
                                    './phc-winner-argon2/src/blake2',] + includes,
                    define_macros = [('HAVE_CONFIG_H', None)] + define_macros,
                    extra_compile_args = CFLAGS,
                    library_dirs = library_dirs,
                    libraries = libraries
                           )

setup(name='argon2',
      version='0.1.9',
      description='Bindings for the argon2 password hasher',
      author='Moroz Ilya',
      author_email='flamewowilia@gmail.com',
      url='https://github.com/flamewow/argon2_py',
      py_modules=['argon2'],
      ext_modules=[_argon2_module],
      packages=[ 'phc-winner-argon2', ],

      classifiers=(
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
        ),
      license="CC0",
     )
