
#include <webserver_string.h>

// empty
int webserver_str_empty(webserver_str_t s)
{
	return (!s.str || !s.len) ? ADX_ERROR : ADX_OK;
}

// null
webserver_str_t webserver_str_null(void)
{
	webserver_str_t s = {NULL, 0, 0};
	return s;
}

// ADX_STR
webserver_str_t ADX_STR(const char *str)
{
	if (!str) return webserver_str_null();
	return ADX_STR2((void *)str, strlen(str));
}

webserver_str_t ADX_STR2(void *str, size_t len)
{
	webserver_str_t s = {str, len, 0};
	return s;
}

// value string
webserver_str_t webserver_str_format(char *str, const char *format, ...)
{
	va_list ap;
	va_start(ap, format);
	webserver_str_t s = {str, 0, 0};
	s.len = vsprintf(str, format, ap);
	va_end(ap);
	return s;
}

// strdup
webserver_str_t webserver_strdup(webserver_pool_t *pool, void *str, size_t len)
{
	webserver_str_t s = webserver_str_null();
	if (!pool || !str || !len)
		return s;

	s.str = webserver_alloc(pool, len + 1);
	if (!s.str)
		return s;

	s.len = len;
	s.str[len] = 0;
	s.memory_size = len + 1;
	memcpy(s.str, str, len);
	return s;
}

// strdup
webserver_str_t webserver_strdup_r(webserver_pool_t *pool, const char *str)
{
	if (!pool || !str)
		return webserver_str_null();

	return webserver_strdup(pool, (void *)str, strlen(str));
}

// atoi
int webserver_str_atoi(webserver_str_t s)
{
	if (webserver_str_empty(s))
		return 0;

	return webserver_atoi(s.str);
}

// atof
double webserver_str_atof(webserver_str_t s)
{
	if (webserver_str_empty(s))
		return 0;

	return webserver_atof(s.str);
}

// atol
long webserver_str_atol(webserver_str_t s)
{
	if (webserver_str_empty(s))
		return 0;

	return webserver_atol(s.str);
}

// atoll
long long webserver_str_atoll(webserver_str_t s)
{
	if (webserver_str_empty(s))
		return 0;

	return webserver_atoll(s.str);
}

// from number
webserver_str_t webserver_str_from_number(webserver_pool_t *pool, long long n)
{
	char str[128];
	int len = sprintf(str, "%lld", n);
	return webserver_strdup(pool, str, len);
}

// from double
webserver_str_t webserver_str_from_double(webserver_pool_t *pool, double n)
{
	char str[128];
	int len = sprintf(str, "%0.2f", n);
	return webserver_strdup(pool, str, len);
}

// 不分大小写strstr
char *webserver_strstr(webserver_str_t s1, webserver_str_t s2)
{
	if (webserver_str_empty(s1))
		return NULL;

	if (webserver_str_empty(s2))
		return NULL;

	size_t i;
	for (i = 0; i < s1.len; i++) {
		if(strncasecmp(&s1.str[i], s2.str, s2.len) == 0)
			return &s1.str[i];
	}

	return NULL;
}

// 转换大写
webserver_str_t webserver_str_upper(webserver_str_t s)
{
	size_t i;
	for(i = 0; i < s.len; i++) {
		s.str[i] = toupper(s.str[i]);
	}

	return s;
}

// 转换小写
webserver_str_t webserver_str_lower(webserver_str_t s)
{
	size_t i;
	for(i = 0; i < s.len; i++) {
		s.str[i] = tolower(s.str[i]);
	}

	return s;
}

// strcat
int webserver_strcat(webserver_str_t *s1,  webserver_str_t *s2)
{
	if (!s1 || !s2)
		return ADX_ERROR;

	if (webserver_str_empty(*s2))
		return ADX_OK;

	if (s1->len + s2->len >= s1->memory_size)
		return ADX_ERROR;

	memcpy(&s1->str[s1->len], s2->str, s2->len);
	s1->len += s2->len;
	s1->str[s1->len] = 0;
	return ADX_OK;
}

int webserver_strcat_r(webserver_str_t *s1, const char *str, size_t len)
{
	webserver_str_t s2 = {(char *)str, len, 0};
	return webserver_strcat(s1, &s2);
}

// 替换
static int __webserver_replace(
        webserver_str_t *out, webserver_str_t *in,
        webserver_str_t *src, webserver_str_t *dest)
{
	size_t i;
	if (!in || !out || !src || !dest)
		return ADX_ERROR;

	if (webserver_str_empty(*in))
		return ADX_ERROR;

	if (webserver_str_empty(*src))
		return ADX_ERROR;

	if (webserver_str_empty(*dest)) {
		dest->str = "";
		dest->len = 0;
	}

	for(i = 0, out->len = 0; i < in->len; ) {

		if (strncmp(&in->str[i], src->str, src->len) == 0) {

			i = i + src->len;
			if (webserver_strcat(out, dest))
				return ADX_ERROR;

		} else {

			if (webserver_strcat_r(out, &in->str[i++], 1))
				return ADX_ERROR;
		}
	}

	return ADX_OK;
}

void webserver_replace_set_message(webserver_replace_t *replace, webserver_str_t *message)
{
	replace->in->len = message->len;
	memcpy(replace->in->str, message->str, message->len);
}

int webserver_replace_init(webserver_replace_t *replace, webserver_str_t *buffer, webserver_str_t *message)
{
	if (webserver_str_empty(*message))
		return ADX_ERROR;

	if (buffer->memory_size <= 2)
		return ADX_ERROR;

	replace->in = &replace->s1;
	replace->in->str = buffer->str;
	replace->in->memory_size = buffer->memory_size / 2;
	replace->in->len = 0;

	replace->out = &replace->s2;
	replace->out->str = replace->in->str + replace->in->memory_size;
	replace->out->memory_size = replace->in->memory_size;
	replace->out->len = 0;

	replace->buffer = replace->out;
	webserver_replace_set_message(replace, message);
	return ADX_OK;
}

int webserver_replace_string(webserver_replace_t *replace, webserver_str_t src, webserver_str_t dest)
{

	if (__webserver_replace(replace->out, replace->in, &src, &dest))
		return ADX_ERROR;

	replace->buffer = replace->out;
	replace->out = replace->in;
	replace->in = replace->buffer;
	return ADX_OK;
}

int webserver_replace_number(webserver_replace_t *replace, webserver_str_t src, int n)
{
	char str[128];
	int len = sprintf(str, "%d", n);
	webserver_str_t dest = ADX_STR2(str, len);
	return webserver_replace_string(replace, src, dest);
}

int webserver_replace_double(webserver_replace_t *replace, webserver_str_t src, double n)
{
	char str[128];
	int len = sprintf(str, "%0.2f", n);
	webserver_str_t dest = ADX_STR2(str, len);
	return webserver_replace_string(replace, src, dest);
}

char *webserver_str_filter(char *src, char ch)
{
	if (!src || !(*src))
		return NULL;

	char *s, *dest = src;
	for (s = src; *s; s++) {
		if (*s != ch)
			*dest++ = *s;
	}

	*dest = 0;
	return src;
}

char *webserver_strtok(const char *src, char *dest, char **save_ptr, int ch)
{
	*dest = 0;
	if (save_ptr && *save_ptr)
		src = *save_ptr;

	char *p = dest;
	char *s = (char *)src;
	for (; s && *s; s++) {

		if (*s == ch) {

			*p = 0;
			*save_ptr = s + 1;
			return dest;
		}

		*p++ = *s;
	}

	if (src || *save_ptr) {

		*p = 0;
		*save_ptr = NULL;
		return dest;
	}

	return NULL;
}

void dict_set_string(PyObject *root, const char *key, char *val)
{
    if (!root || !key || !val)
        return;

    if (!(*key) || !(*val))
        return;

    PyObject *py_val = PyUnicode_FromString(val);
    // PyObject *py_val = PyString_FromString(val);
    if (!py_val)
        return;

    PyDict_SetItemString(root, key, py_val);
    Py_DECREF(py_val);
}

