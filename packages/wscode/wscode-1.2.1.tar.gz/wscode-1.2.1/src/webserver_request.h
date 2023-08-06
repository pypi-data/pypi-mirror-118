
#ifndef __REQUEST_H__
#define __REQUEST_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <Python.h>
#include <webserver_fcgiapp.h>
#include <webserver_string.h>
#include <webserver_urlcode.h>
#include <webserver_conf.h>
#include <webserver_upload.h>

typedef struct {
    PyObject *this;
    FCGX_Request fcgi;
    PyObject *worker_function;
    PyObject *worker_args;
    char *buffer;
    int size;
} request_t;

request_t *request_init(int sock, PyObject *worker_function);
PyObject *request_param(PyObject *self, PyObject *args);
PyObject *request_execution(PyObject *self, PyObject *args);
PyObject *request_query_string_dict(PyObject *self, PyObject *args);
PyObject *request_http_cookie_dict(PyObject *self, PyObject *args);
PyObject *request_content_length(PyObject *self, PyObject *args);
PyObject *request_content_body(PyObject *self, PyObject *args);
PyObject *request_upload(PyObject *self, PyObject *args);

#endif


