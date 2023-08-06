
#ifndef __SESSION_H__
#define __SESSION_H__

#include <Python.h>

#define SESSION_MODE_FILE        0
#define SESSION_MODE_REDIS       1
#define SESSION_MODE_MEMORY      2
#define SESSION_SIZE             4096

PyObject *session_create(PyObject *self, PyObject *args);
PyObject *session_destroy(PyObject *self, PyObject *args);
PyObject *session_find(PyObject *self, PyObject *args);

#endif


