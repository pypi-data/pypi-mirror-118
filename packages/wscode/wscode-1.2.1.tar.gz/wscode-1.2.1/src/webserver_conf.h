
#ifndef __ADX_CONF_H__
#define __ADX_CONF_H__

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <webserver_rbtree.h>
#include <webserver_alloc.h>
#include <webserver_string.h>
#include <Python.h>

#define ASCIILINESZ 2048

typedef struct {
	webserver_rbtree_node tree;
	char *section;
	char *key;
	char *val;
} webserver_conf_node_t;

typedef struct {
	webserver_rbtree_head head;
	webserver_pool_t *pool;
} webserver_conf_t;

int webserver_conf_init(void);
int webserver_conf_parse(const char *path);
void webserver_conf_free(void);

char *get_conf_string(const char *section, const char *key);
int get_conf_number(const char *section, const char *key);
int get_conf_bool(const char *section, const char *key);
PyObject *get_conf(PyObject *self, PyObject *args);

#endif


