"""
Python bindings for the argon2 password hashing algorithm

Argon2 is the winner of the Password Hashing Competition
(https://password-hashing.net), and this is a Python wrapper for
it. The source of Argon2 is available at
https://github.com/P-H-C/phc-winner-argon2
"""

import imp
import sys
from ctypes import (
    c_char_p,
    c_int,
    c_size_t,
    c_uint32,
    cdll,
    create_string_buffer,
)


IS_PY2 = sys.version_info < (3, 0, 0, 'final', 0)

ARGON2_LIB = cdll.LoadLibrary(imp.find_module('_argon2')[1])

C_ARGON2_HASH = ARGON2_LIB.argon2_hash
C_ARGON2_HASH.argtypes = [
    c_uint32,  # uint32_t       N
    c_uint32,  # uint32_t       r
    c_uint32,  # uint32_t       p

    c_char_p,  # const uint8_t *passwd
    c_size_t,  # size_t         passwdlen

    c_char_p,  # const uint8_t *salt
    c_size_t,  # size_t         saltlen

    c_char_p,  # uint8_t       *buf
    c_size_t,  # size_t         buflen

    c_char_p,  # uint8_t       *encoded
    c_size_t,  # size_t         encodedlen

    c_uint32,  # uint32_t       Argon_type
]
C_ARGON2_HASH.restype = c_int


class Argon2Type(object):  # pylint: disable=too-few-public-methods
    """Enumerated Argon2 types"""
    Argon2_d = 0
    Argon2_i = 1

argon2_d = Argon2Type.Argon2_d  # pylint: disable=invalid-name
argon2_i = Argon2Type.Argon2_i  # pylint: disable=invalid-name


class Argon2Exception(Exception):
    """The argon2_hash call failed"""
    errors = (
        "ARGON2_OK", "ARGON2_OUTPUT_PTR_NULL", "ARGON2_OUTPUT_TOO_SHORT", "ARGON2_OUTPUT_TOO_LONG",
        "ARGON2_PWD_TOO_SHORT", "ARGON2_PWD_TOO_LONG", "ARGON2_SALT_TOO_SHORT",
        "ARGON2_SALT_TOO_LONG", "ARGON2_AD_TOO_SHORT", "ARGON2_AD_TOO_LONG",
        "ARGON2_SECRET_TOO_SHORT", "ARGON2_SECRET_TOO_LONG",
        "ARGON2_TIME_TOO_SMALL", "ARGON2_TIME_TOO_LARGE", "ARGON2_MEMORY_TOO_LITTLE",
        "ARGON2_MEMORY_TOO_MUCH", "ARGON2_LANES_TOO_FEW", "ARGON2_LANES_TOO_MANY",
        "ARGON2_PWD_PTR_MISMATCH", "ARGON2_SALT_PTR_MISMATCH", "ARGON2_SECRET_PTR_MISMATCH",
        "ARGON2_AD_PTR_MISMATCH", "ARGON2_MEMORY_ALLOCATION_ERROR", "ARGON2_FREE_MEMORY_CBK_NULL",
        "ARGON2_ALLOCATE_MEMORY_CBK_NULL", "ARGON2_INCORRECT_PARAMETER", "ARGON2_INCORRECT_TYPE",
        "ARGON2_OUT_PTR_MISMATCH", "ARGON2_THREADS_TOO_FEW", "ARGON2_THREADS_TOO_MANY",
        "ARGON2_MISSING_ARGS", "ARGON2_ENCODING_FAIL", "ARGON2_DECODING_FAIL"
    )


def _ensure_bytes(data):
    if IS_PY2 and isinstance(data, unicode):
        raise TypeError('can not encrypt/decrypt unicode objects')

    if not IS_PY2 and isinstance(data, str):
        return bytes(data, 'utf-8')

    return data


def argon2_hash(  # pylint: disable=too-many-arguments,invalid-name
        password, salt, t=16, m=8, p=1, buflen=128, argon_type=Argon2Type.Argon2_i):
    """
    This is argon2 hashing function.

    t - time cost, which defines the amount of computation realized and
        therefore the execution time, given in number of iterations
    m - memory cost, which defines the memory usage, given in kibibytes
    p - parallelism degree, which defines the number of parallel threads
    """
    outbuf = create_string_buffer(buflen)
    password = _ensure_bytes(password)
    salt = _ensure_bytes(salt)

    result = C_ARGON2_HASH(t, m, p,
                           password, len(password),
                           salt, len(salt),
                           outbuf, buflen,
                           None, 0,
                           argon_type)

    if result:
        raise Argon2Exception(Argon2Exception.errors[result])

    return outbuf.raw


if __name__ == "__main__":
    print(argon2_hash("password", "some salt"))  # pylint: disable=superfluous-parens
