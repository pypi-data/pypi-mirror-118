
#ifndef __ADX_LOG_H__
#define __ADX_LOG_H__

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdarg.h>
#include <pthread.h>
#include <errno.h>
#include <time.h>
#include <Python.h>
#include <webserver_alloc.h>

#ifdef __cplusplus
extern "C" {
#endif

#define LOGERROR		1
#define LOGWARNING		2
#define LOGINFO			3
#define LOGDEBUG		4

	typedef struct {
		FILE *fp;
		const char *path;
		webserver_pool_t *pool;
		pthread_mutexattr_t mattr;
		pthread_mutex_t mutex;

	} webserver_log_t;

	int webserver_log_init(void);
	void webserver_log_free(void);

void webserver_log(const char *format, ...);
PyObject *__webserver_log(PyObject *self, PyObject *args);

#ifdef __cplusplus
}
#endif

#endif


