
#include <webserver_conf.h>

static char *path = "app.conf";
static webserver_conf_t *webserver_conf_root = NULL;
int webserver_conf_init(void)
{
	if (webserver_conf_root)
		return ADX_ERROR;

	webserver_pool_t *pool = webserver_malloc_pool();
	if (!pool) return ADX_ERROR;

	webserver_conf_root = webserver_alloc(pool, sizeof(webserver_conf_t));
	if (!webserver_conf_root)
		return ADX_ERROR;

	webserver_conf_root->pool = pool;
	webserver_conf_root->head = RB_ROOT;
	if (webserver_conf_parse(path) != 0) {
		webserver_conf_free();
		return ADX_ERROR;
	}

	return ADX_OK;
}

void webserver_conf_free(void)
{
	if (webserver_conf_root)
		webserver_pool_free(webserver_conf_root->pool);
}

int webserver_conf_add(char *section, char *key, char *val)
{
	if (!section || !key || !val)
		return ADX_ERROR;

	int section_len = strlen(section);
	int key_len = strlen(key);
	int val_len = strlen(val);
	if (!section_len || !key_len || !val_len)
		return ADX_ERROR;

	webserver_conf_node_t *node = malloc(sizeof(webserver_conf_node_t));
	if (!node) return ADX_ERROR;

	node->section = webserver_alloc(webserver_conf_root->pool, section_len + 1);
	node->key = webserver_alloc(webserver_conf_root->pool, key_len + 1);
	node->val = webserver_alloc(webserver_conf_root->pool, val_len + 1);
	if (!node->section || !node->key || !node->val)
		return ADX_ERROR;

	strcpy(node->section, section);
	strcpy(node->key, key);
	strcpy(node->val, val);

	node->tree.str.str = node->key;
	node->tree.str.len = key_len;
	webserver_rbtree_string_add(&webserver_conf_root->head, &node->tree);
	return ADX_OK;
}

int webserver_conf_parse(const char *path)
{
	char line    [ASCIILINESZ] = {0};
	char section [ASCIILINESZ] = {0};
	char key     [ASCIILINESZ] = {0};
	char value   [ASCIILINESZ] = {0};

	FILE *fp = fopen(path, "r");
	if (!fp) return ADX_ERROR;

	while (fgets(line, 1024, fp)) {

		int len = strlen(line) - 1;
		if (len == 0 || len >= ASCIILINESZ) continue;
		if (line[0] == '#') continue;

		while ((len >= 0) && ((line[len]=='\n') || (isspace(line[len])))) {
			line[len] = 0 ;
			len-- ;
		}

		if (line[0]=='[' && line[len]==']') {
			sscanf(line, "[%[^]]", section);
		}

		if (section[0] &&
				(sscanf (line, "%[^=] = \"%[^\"]\"",	key, value) == 2
				 ||  sscanf (line, "%[^=] = '%[^\']'",	key, value) == 2
				 ||  sscanf (line, "%[^=] = %[^;#]",	key, value) == 2)) {
			if (webserver_conf_add(section, key, value)) {
				fclose(fp);
				return ADX_ERROR;
			}
		}
	}

	fclose(fp);
	return ADX_OK;
}

char *get_conf_string(const char *section, const char *key)
{
	if (!webserver_conf_root || !key)
		return NULL;

	webserver_conf_node_t *node = (webserver_conf_node_t *)
		webserver_rbtree_string_find(&webserver_conf_root->head, key, strlen(key));
	if (!node)
		return NULL;

	return node->val;
}

int get_conf_number(const char *section, const char *key)
{
	char *value = get_conf_string(section, key);
	return value ? webserver_atoi(value) : 0;
}

int get_conf_bool(const char *section, const char *key)
{
	char *value = get_conf_string(section, key);
	if (!value)
		return 0;

	if (strcmp(value, "True") == 0) {
		return 1;
	}

	if (strcmp(value, "true") == 0) {
		return 1;
	}

	if (strcmp(value, "yes") == 0) {
		return 1;
	}

	return 0;
}

PyObject *get_conf(PyObject *self, PyObject *args)
{
	char *section = NULL, *key = NULL;
	int section_len = 0, key_len = 0;
	if (!PyArg_ParseTuple(args, "s#s#",
				&section, &section_len,
				&key, &key_len)) {
		Py_RETURN_NONE;
	}

	if (section_len <= 0 || section_len <= 0) {
		Py_RETURN_NONE;
	}

	char *val = get_conf_string(section, key);
	if (!val) {
		Py_RETURN_NONE;
	}

	return Py_BuildValue("s", val);
}

