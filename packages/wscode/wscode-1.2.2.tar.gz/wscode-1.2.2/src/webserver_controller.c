
#include "webserver_controller.h"

static webserver_rbtree_head controller_head = RB_ROOT;
static webserver_rbtree_head controller_check_pass_head = RB_ROOT;
static void controller_parse(char *path)
{
    char name[PATH_MAX];
    strcpy(name, path);

    char *s = NULL;
	for (s = name; *s; s++)
		if (*s == '/') *s = '.';

    PyObject *module = PyImport_ImportModule(name);
	if (!module) {
        PyErr_Print();
        Py_Exit(-1);
	}

    module->ob_refcnt++;
	PyObject *func = PyObject_GetAttrString(module, "run");
	if (!func) {
        PyErr_Print();
        Py_Exit(-1);
	}

    func->ob_refcnt++;
	controller_t *c = malloc(sizeof(controller_t));
	if (!c) {
        Py_Exit(-1);
	}

	size_t len  = strlen(name);
	c->execution = malloc(len);
	memcpy(c->execution, name, len);
	c->execution[len] = 0;

	c->tree.str.str = c->execution;
	c->tree.str.len = len;
    c->module = module;
    c->func = func;

	webserver_rbtree_string_add(&controller_head, &c->tree);
}

static void controller_parse_dir(char *path, char *name)
{
	char __path[PATH_MAX];
	int size = snprintf(__path, PATH_MAX, "%s/%s", path, name);
	if (size >= PATH_MAX) {
		return;
	}

    return controller_scanning(__path);
}

static void controller_parse_file(char *path, char *name)
{
	char __path[PATH_MAX];
	if (strstr(name, "__init__")) {
        return;
	}

	char *ext = strrchr(name,'.');
	if (!ext || strcmp(".py", ext)) {
		return;
	}

	*ext = 0;
	int size = snprintf(__path, PATH_MAX, "%s/%s", path, name);
	if (size >= PATH_MAX) {
		return;
	}

	return controller_parse(__path);
}

void controller_scanning(char *path)
{
	DIR *dir = opendir(path);
	if (!dir) return;

	for (;;) {
		struct dirent *d = readdir(dir);
		if (!d) break;

		if(strncmp(d->d_name, ".", 1) == 0) {
			continue;
		}

		if (d->d_type == DT_DIR) {
			controller_parse_dir(path, d->d_name);

		} else if (d->d_type == DT_REG) {
			controller_parse_file(path, d->d_name);
		}
	}

	closedir(dir);
}

int controller_init(void)
{
    static char path[] = "controller";
	controller_scanning(path);
    controller_check_pass_init();
    return 0;
}

PyObject *get_controller(PyObject *self, PyObject *args)
{
    int len = 0;
    char *key = NULL;
    if (!PyArg_ParseTuple(args, "s#", &key, &len)) {
        Py_RETURN_NONE;
    }

    if (!key || !len) {
        Py_RETURN_NONE;
    }

    webserver_rbtree_node *tree = webserver_rbtree_string_find(&controller_head, key, len);
    if (!tree) {
        Py_RETURN_NONE;
    }

    controller_t *c = (controller_t *)tree;
    c->module->ob_refcnt++;
    c->func->ob_refcnt++;
    return c->func;
}

void controller_check_pass_add(char *str);
void controller_check_pass_init(void)
{
    controller_check_pass_add("controller.login");
    char *buffer = get_conf_string("controller", "pass");
    if (!buffer) return;

    char *save = NULL;
    char *str = strtok_r(buffer, ",", &save);
    while (str) {

        controller_check_pass_add(str);
        str = strtok_r(NULL, ",", &save);
    }
}

void controller_check_pass_add(char *str)
{
    if (!str)
        return;

    size_t len = strlen(str);
    if (!len)
        return;;

    webserver_rbtree_node *tree = malloc(sizeof(webserver_rbtree_node));
    if (!tree)
        return;

    tree->str.str = str;
    tree->str.len = len;
    webserver_rbtree_string_add(&controller_check_pass_head, tree);
}

PyObject *controller_check_pass(PyObject *self, PyObject *args)
{
    int len = 0;
    char *key = NULL;
    if (!PyArg_ParseTuple(args, "s#", &key, &len)) {
        Py_RETURN_FALSE;
    }

    if (!key || !len) {
        Py_RETURN_FALSE;
    }

    if (webserver_rbtree_string_find(&controller_check_pass_head, key, len)) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}

