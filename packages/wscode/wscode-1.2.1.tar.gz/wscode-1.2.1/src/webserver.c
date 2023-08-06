
#include <webserver_type.h>
#include <webserver_conf.h>
#include <webserver_logs.h>
#include <webserver_request.h>
#include <webserver_response.h>
#include <webserver_session.h>
#include <webserver_controller.h>

static void Extension_signal(int code)
{
	switch(code) {
		case SIGINT :
		case SIGTERM :
		case SIGKILL :
			exit(0);
	}
}

void Extension_worker_loop(int sock, PyObject *worker_function)
{
	request_t *r = request_init(sock, worker_function);
	if (!r) exit(-1);

	for (;;) {
		if (FCGX_Accept_r(&r->fcgi) == 0) {
			PyObject_Call(r->worker_function, r->worker_args, NULL);
			// PyObject_CallObject(r->worker_function, r->worker_args);
			FCGX_Finish_r(&r->fcgi);
		}
	}
}

PyObject *Extension_run(PyObject *self, PyObject *args)
{
	PyObject *worker_function = NULL;
	if (!PyArg_ParseTuple(args, "O", &worker_function))
		Py_RETURN_FALSE;

	if (!PyFunction_Check(worker_function))
		Py_RETURN_FALSE;

	if (webserver_conf_init())
		Py_RETURN_FALSE;

	if (webserver_log_init())
		Py_RETURN_FALSE;

	if (controller_init())
		Py_RETURN_FALSE;

	signal(SIGHUP, SIG_IGN);
	signal(SIGPIPE, SIG_IGN);
	signal(SIGINT, Extension_signal);
	signal(SIGTERM, Extension_signal);
	signal(SIGKILL, Extension_signal);

	char *listen = get_conf_string("core", "listen");
	int port = get_conf_number("core", "port");
	int daemonize = get_conf_bool("core", "daemonize");
	int worker_count = get_conf_number("core", "worker_count");

	if (!listen) listen = "0.0.0.0";
	if (!port) port = 9001;
	if (!worker_count) worker_count = 8;

	int listen_sock = FCGX_OpenSocket(listen, port);
	if (listen_sock <= 0)
		exit(-1);

	fprintf(stdout, "start...\n");
    fprintf(stdout, "python version=%d.%d.%d\n", PY_MAJOR_VERSION, PY_MINOR_VERSION, PY_MICRO_VERSION);
    if (!daemonize) {
		Extension_worker_loop(listen_sock, worker_function);
	}

	pid_t i, worker_pid[worker_count];
	for (i = 0; i < worker_count; i++) {
		worker_pid[i] = fork();
		if (worker_pid[i] == 0) {
			Extension_worker_loop(listen_sock, worker_function);
		}
	}

	for (;;) {
		for (i = 0; i < worker_count; i++) {
			if (waitpid(worker_pid[i], NULL, WNOHANG) == -1) {
				worker_pid[i] = fork();
				if (worker_pid[i] == 0) {
					Extension_worker_loop(listen_sock, worker_function);
				}
			}
		}

		sleep(1);
	}
}

PyMethodDef Extension_methods[] = {
	{"run", Extension_run, METH_VARARGS, NULL},
	{"get_conf", get_conf, METH_VARARGS, NULL},

	{"request_param", request_param, METH_VARARGS, NULL},
	{"request_execution", request_execution, METH_VARARGS, NULL},
	{"request_query_string_dict", request_query_string_dict, METH_VARARGS, NULL},
	{"request_http_cookie_dict", request_http_cookie_dict, METH_VARARGS, NULL},
	{"request_content_length", request_content_length, METH_VARARGS, NULL},
	{"request_content_body", request_content_body, METH_VARARGS, NULL},
	{"request_upload", request_upload, METH_VARARGS, NULL},
	{"response", web_server_response, METH_VARARGS, NULL},

	{"session_create", session_create, METH_VARARGS, NULL},
	{"session_destroy", session_destroy, METH_VARARGS, NULL},
	{"session_find", session_find, METH_VARARGS, NULL},

	{"get_controller", get_controller, METH_VARARGS, NULL},
	{"controller_check_pass", controller_check_pass, METH_VARARGS, NULL},

	{"log", __webserver_log, METH_VARARGS, NULL},
	{NULL, NULL, 0, NULL}
};

#ifdef IS_PY3
static struct PyModuleDef Extension_module = {
	PyModuleDef_HEAD_INIT,
	"Extension",
	NULL,
	-1,
	Extension_methods
};

void PyInit_Extension(){
	PyModule_Create(&Extension_module);
}
#else
PyMODINIT_FUNC initExtension(void)
{
	Py_InitModule("Extension", Extension_methods);
}
#endif

