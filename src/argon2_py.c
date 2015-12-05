/* Author : Moroz Ilya */

#include <Python.h>

static PyMethodDef _argon2_methods[] = {
    {NULL, NULL, 0, NULL},
};

#if PY_MAJOR_VERSION == 2

PyMODINIT_FUNC init_argon2(void) {
    Py_InitModule("_argon2", _argon2_methods);
}

#endif

#if PY_MAJOR_VERSION == 3

static struct PyModuleDef argon2_module = {
    PyModuleDef_HEAD_INIT,
    "_argon2",
    NULL,
    -1,
    _argon2_methods
};

PyMODINIT_FUNC PyInit__scrypt(void) {
    return PyModule_Create(&argon2_module);
}

#endif