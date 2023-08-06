
#ifndef __ADX_ALLOC_H__
#define __ADX_ALLOC_H__

#include <webserver_type.h>
#include <webserver_list.h>

#define ADX_ALLOC_MANAGER       1
#define ADX_ALLOC_MANAGER_NOT   0

typedef void *webserver_alloc_call(void *, size_t size);
typedef void *webserver_realloc_call(void *, void *, size_t size);
typedef void webserver_free_call(void *, void *);

typedef struct {
	webserver_list_t next;
	void *block;
	size_t size;

} webserver_pool_block_t;

typedef struct {
	webserver_list_t head;

} webserver_pool_manager;

typedef struct {
	void *__pool;
	webserver_alloc_call *__alloc;
	webserver_realloc_call *__realloc;
	webserver_free_call *__free;
	webserver_pool_manager *manager;
	size_t size;

} webserver_pool_t;

void *webserver_alloc(webserver_pool_t *pool, size_t size);
void webserver_pool_free(webserver_pool_t *pool);
webserver_pool_t *webserver_malloc_pool(void);
webserver_pool_t *webserver_pool_create(int manager_mode,
		void *__pool,
		webserver_alloc_call *__alloc,
		webserver_realloc_call *__realloc,
		webserver_free_call *__free);

#endif





