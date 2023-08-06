
#include "webserver_response.h"

PyObject *web_server_response(PyObject *self, PyObject *args)
{
    char *buff = NULL;
    PyObject *request = NULL;
    if (!PyArg_ParseTuple(args, "Os", &request, &buff))
        Py_RETURN_FALSE;

    request_t *r = PyLong_AsVoidPtr(request);
    if (!r) Py_RETURN_FALSE;

    int len = (int)strlen(buff);
    if (FCGX_PutStr(buff, len, r->fcgi.out) == -1)
          Py_RETURN_FALSE;

    FCGX_Finish_r(&r->fcgi);
    Py_RETURN_TRUE;
}

