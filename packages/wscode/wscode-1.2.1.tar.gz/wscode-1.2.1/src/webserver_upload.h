
#ifndef __REQUEST_UPLOAD_H__
#define __REQUEST_UPLOAD_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h>

#define UPLOAD_BUF_SIZE 1024
#if PY_MAJOR_VERSION >= 3
#ifndef IS_PY3K
#define IS_PY3K 1
#endif
#endif

typedef struct {
    PyObject *list;
    PyObject *cur_dict;
    const char *cur_field;
    size_t cur_field_len;
    PyObject *cur_data;
    char *content_type;
    char *content_body;
    size_t length;
} upload_t;

PyObject *upload_parse(upload_t *upload);
#endif


