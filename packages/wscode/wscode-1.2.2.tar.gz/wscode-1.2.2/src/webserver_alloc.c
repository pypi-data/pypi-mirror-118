
#include <webserver_alloc.h>

static void *__alloc(void *pool, size_t size) {return malloc(size);}
static void *__realloc(void *pool, void *p, size_t size) {return realloc(p, size);}
static void __free(void *pool, void *p) {free(p);}
webserver_pool_t *webserver_pool_create(int manager_mode,
		void *__pool,
		webserver_alloc_call *__alloc,
		webserver_realloc_call *__realloc,
		webserver_free_call *__free)
{
	if (!__alloc)
		return NULL;

	if (manager_mode) {
		if (!__free)
			return NULL;
	}

	webserver_pool_t *pool = __alloc(__pool, sizeof(webserver_pool_t));
	if (!pool) return NULL;

	pool->__pool = __pool;
	pool->__alloc = __alloc;
	pool->__realloc = __realloc;
	pool->__free = __free;
	pool->manager = NULL;
	pool->size = 0;

	if (manager_mode) {
		pool->manager = __alloc(__pool, sizeof(webserver_pool_manager));
		if (!pool->manager)
			return NULL;

		webserver_list_init(&pool->manager->head);
	}

	return pool;
}

webserver_pool_block_t *webserver_pool_block(webserver_pool_t *pool, void *p)
{
	if (!pool || !pool->manager || !p)
		return NULL;

	char *__p = (char *)p;
	char *node = __p - sizeof(webserver_pool_block_t);
	return (webserver_pool_block_t *)node;
}

void *webserver_alloc_manager(webserver_pool_t *pool, size_t size)
{
	if (!pool || size <= 0)
		return NULL;

	char *p = pool->__alloc(pool->__pool, sizeof(webserver_pool_block_t) + size);
	if (!p) return NULL;

	webserver_pool_block_t *node = (webserver_pool_block_t *)p;
	node->block = sizeof(webserver_pool_block_t) + p;
	node->size = size;
	pool->size += size;

	webserver_list_add(&pool->manager->head, &node->next);
	return node->block;
}

void *webserver_alloc(webserver_pool_t *pool, size_t size)
{
	if (pool->manager)
		return webserver_alloc_manager(pool, size);

	void *p = pool->__alloc(pool->__pool, size);
	if (!p) return NULL;

	pool->size += size;
	return p;
}

void *webserver_realloc(webserver_pool_t *pool, void *__p, size_t size)
{
	if (!pool || !pool->manager)
		return NULL;

	if (!pool->__realloc)
		return NULL;

	webserver_pool_block_t *node = webserver_pool_block(pool, __p);
	if (!node) return NULL;

	if (node->size >= size)
		return __p;

	webserver_list_del(&node->next);
	pool->size = pool->size - node->size;

	char *p = pool->__realloc(node, pool->__pool, sizeof(webserver_pool_block_t) + size);
	if (!p) return NULL;

	node = (webserver_pool_block_t *)p;
	node->block = sizeof(webserver_pool_block_t) + p;
	node->size = size;
	pool->size += size;

	webserver_list_add(&pool->manager->head, &node->next);
	return node->block;
}

void webserver_pool_free(webserver_pool_t *pool)
{
	if (!pool || !pool->manager || !pool->__free)
		return;

	webserver_list_t *p = NULL;
	webserver_list_t *head = &pool->manager->head;
	for (p = head->next; p != head; ) {
		webserver_pool_block_t *node = (webserver_pool_block_t *)p;
		p = p->next;

		pool->__free(pool->__pool, node);
	}

	pool->__free(pool->__pool, pool);
}

webserver_pool_t *webserver_malloc_pool(void)
{
	return webserver_pool_create(ADX_ALLOC_MANAGER,
			NULL,
			__alloc,
			__realloc,
			__free);
}

