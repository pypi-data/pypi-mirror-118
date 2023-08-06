
#ifndef __controller_h__
#define __controller_h__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <webserver_rbtree.h>
#include <webserver_conf.h>
#include <Python.h>

typedef struct {
	webserver_rbtree_node tree;
	char *execution;
	PyObject *module;
	PyObject *func;

} controller_t;

int controller_init(void);
void controller_scanning(char *path);
PyObject *get_controller(PyObject *self, PyObject *args);

void controller_check_pass_init(void);
PyObject *controller_check_pass(PyObject *self, PyObject *args);

#endif

