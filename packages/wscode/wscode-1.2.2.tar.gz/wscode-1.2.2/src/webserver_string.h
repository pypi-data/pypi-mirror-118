
#ifndef __ADX_STRING_H__
#define __ADX_STRING_H__

#include <webserver_type.h>
#include <webserver_alloc.h>
#include <webserver_time.h>

#define IS_NULL(o)     (o?o:"")
#define webserver_atoi(o)    atoi(IS_NULL(o))
#define webserver_atof(o)    atof(IS_NULL(o))
#define webserver_atol(o)    atol(IS_NULL(o))
#define webserver_atoll(o)   atoll(IS_NULL(o))

typedef struct {
	char *str;
	size_t len, memory_size;
} webserver_str_t;

typedef struct {
	webserver_str_t s1, s2;
	webserver_str_t *in, *out, *buffer;
} webserver_replace_t;

// empty
int webserver_str_empty(webserver_str_t str);

// null
webserver_str_t webserver_str_null(void);

// ADX_STR
webserver_str_t ADX_STR(const char *str);
webserver_str_t ADX_STR2(void *str, size_t len);
webserver_str_t webserver_str_format(char *str, const char *format, ...);

// strdup
webserver_str_t webserver_strdup(webserver_pool_t *pool, void *buf, size_t len);
webserver_str_t webserver_strdup_r(webserver_pool_t *pool, const char *buf);

// 类型转换
int webserver_str_atoi(webserver_str_t s);
double webserver_str_atof(webserver_str_t s);
long webserver_str_atol(webserver_str_t s);
long long webserver_str_atoll(webserver_str_t s);
webserver_str_t webserver_str_from_number(webserver_pool_t *pool, long long n);
webserver_str_t webserver_str_from_double(webserver_pool_t *pool, double n);

// 不分大小写strstr
char *webserver_strstr(webserver_str_t s1, webserver_str_t s2);

// 转换 大写/小写
webserver_str_t webserver_str_upper(webserver_str_t str); // 全部转大写
webserver_str_t webserver_str_lower(webserver_str_t str); // 全部转小写

// strcat
int webserver_strcat(webserver_str_t *s1,  webserver_str_t *s2);
int webserver_strcat_r(webserver_str_t *s1, const char *str, size_t len);

// 宏替换
int webserver_replace_init(webserver_replace_t *replace, webserver_str_t *buffer, webserver_str_t *message);
int webserver_replace_string(webserver_replace_t *replace, webserver_str_t src, webserver_str_t dest);
int webserver_replace_number(webserver_replace_t *replace, webserver_str_t src, int n);
int webserver_replace_double(webserver_replace_t *replace, webserver_str_t src, double n);

// 过滤字符
char *webserver_str_filter(char *src, char ch);
char *webserver_strtok(const char *src, char *dest, char **save_ptr, int ch);

void dict_set_string(PyObject *root, const char *key, char *val);

#endif

