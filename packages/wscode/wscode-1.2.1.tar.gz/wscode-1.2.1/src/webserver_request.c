
#include "webserver_request.h"

request_t *request_init(int sock, PyObject *worker_function)
{
    int body_size = get_conf_number("core", "body_size");
    if (body_size <= 0) body_size = 1024 * 1024 * 5;

    char *buffer = malloc(body_size);
    if (!buffer) return NULL;

    request_t *r = malloc(sizeof(request_t));
    if (!r) return NULL;

    r->this = PyLong_FromVoidPtr(r);
    PyObject *worker_args = PyTuple_New(1);
    PyTuple_SetItem(worker_args, 0, r->this);

    r->this->ob_refcnt = 3;
    worker_args->ob_refcnt = 3;

    FCGX_InitRequest(&r->fcgi, sock, 0);
    r->worker_function = worker_function;
    r->worker_args = worker_args;
    r->buffer = buffer;
    r->size = body_size;
    return r;
}

extern char **environ;
void environ_print(char **env)
{
    char **p;
    for (p = env; *p; p++) {
        fprintf(stdout, "[%s]\n", *p);
    }
}

PyObject *request_param(PyObject *self, PyObject *args)
{
    char *key = NULL;
    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "Os", &request, &key))
        Py_RETURN_NONE;

    if (!key || !request)
        Py_RETURN_NONE;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) Py_RETURN_NONE;

    char *value = FCGX_GetParam(key, r->fcgi.envp);
    if (!value) Py_RETURN_NONE;

    return Py_BuildValue("s", value);
}

PyObject *request_execution(PyObject *self, PyObject *args)
{
    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "O", &request))
        Py_RETURN_NONE;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) Py_RETURN_NONE;

    char *s, *value = FCGX_GetParam("DOCUMENT_URI", r->fcgi.envp);
    if (!value || strlen(value) >= 2000)
        Py_RETURN_NONE;

    strcpy(r->buffer, "controller");
    strcpy(&r->buffer[10], value);
    for (s = r->buffer; *s; s++) {
        if (*s == '/')*s = '.';
    }

    return Py_BuildValue("s", r->buffer);
}

PyObject *request_query_string_dict(PyObject *self, PyObject *args)
{
    PyObject *root = PyDict_New();
    if (!root) Py_RETURN_NONE;

    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "O", &request))
        return root;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) return root;

    char *value = FCGX_GetParam("QUERY_STRING", r->fcgi.envp);
    if (!value) return root;
    strcpy(r->buffer, value);

    char *save = NULL;
    char *str = strtok_r(r->buffer, "&", &save);
    while (str) {
        char *val = strchr(str, '=');
        if (val) {
            *val++ = 0;
            dict_set_string(root, str, val);
        }

        str = strtok_r(NULL, "&", &save);
    }

    return root;
}

PyObject *request_http_cookie_dict(PyObject *self, PyObject *args)
{
    PyObject *root = PyDict_New();
    if (!root) Py_RETURN_NONE;

    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "O", &request))
        return root;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) return root;

    char *value = FCGX_GetParam("HTTP_COOKIE", r->fcgi.envp);
    if (!value) return root;

    strcpy(r->buffer, value);
    webserver_str_filter(r->buffer, '\r');
    webserver_str_filter(r->buffer, '\n');
    webserver_str_filter(r->buffer, '\t');
    webserver_str_filter(r->buffer, ' ');

    char *save = NULL;
    char *str = strtok_r(r->buffer, ";", &save);
    while (str) {
        char *val = strchr(str, '=');
        if (val) {
            *val++ = 0;
            dict_set_string(root, str, val);
        }

        str = strtok_r(NULL, ";", &save);
    }

    return root;
}

PyObject *request_content_length(PyObject *self, PyObject *args)
{
    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "O", &request))
        Py_RETURN_NONE;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) Py_RETURN_NONE;

    char *value = FCGX_GetParam("CONTENT_LENGTH", r->fcgi.envp);
    if (!value) Py_RETURN_NONE;

    return Py_BuildValue("i", strlen(value));
}

PyObject *request_content_body(PyObject *self, PyObject *args)
{
    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "O", &request))
        Py_RETURN_NONE;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) Py_RETURN_NONE;

    int size = FCGX_GetStr(r->buffer, r->size, r->fcgi.in);
    if (size <= 0 || size >= r->size)
        Py_RETURN_NONE;

    r->buffer[size] = 0;
    return Py_BuildValue("s#", r->buffer, size);
}

PyObject *request_upload(PyObject *self, PyObject *args)
{
    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "O", &request))
        Py_RETURN_NONE;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) Py_RETURN_NONE;

    char *CONTENT_TYPE = FCGX_GetParam("CONTENT_TYPE", r->fcgi.envp);
    if (!CONTENT_TYPE) Py_RETURN_NONE;

    int size = FCGX_GetStr(r->buffer, r->size, r->fcgi.in);
    if (size <= 0 || size >= r->size)
        Py_RETURN_NONE;

    upload_t upload;
    upload.content_type = CONTENT_TYPE;
    upload.content_body = r->buffer;
    upload.length = size;
    return upload_parse(&upload);
}

