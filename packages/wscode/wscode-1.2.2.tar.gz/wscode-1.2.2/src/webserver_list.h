
#ifndef __ADX_LIST_H__
#define	__ADX_LIST_H__

#ifdef __cplusplus
extern "C" { 
#endif

	typedef struct webserver_list_t webserver_list_t;
	struct webserver_list_t {

		webserver_list_t *next;
		webserver_list_t *prev;
	};

	static inline void webserver_list_init(webserver_list_t *head)
	{
		head->next = head;
		head->prev = head;
	}

	static inline void _webserver_list_add(webserver_list_t *node, webserver_list_t *prev, webserver_list_t *next)
	{
		next->prev = node;
		node->next = next;
		node->prev = prev;
		prev->next = node;
	}

	static inline void webserver_list_add(webserver_list_t *head, webserver_list_t *node)
	{
		_webserver_list_add(node, head->prev, head);
	}

	static inline void webserver_list_add_tail(webserver_list_t *head, webserver_list_t *node)
	{
		_webserver_list_add(node, head, head->next);
	}

	static inline void _webserver_list_del(webserver_list_t *prev, webserver_list_t *next)
	{
		next->prev = prev;
		prev->next = next;
	}

	static inline void webserver_list_del(webserver_list_t *node)
	{
		_webserver_list_del(node->prev, node->next);
	}

	static inline int webserver_list_empty(webserver_list_t *head)
	{
		webserver_list_t *next = head->next;
		return (next == head) && (next == head->prev);
	}

	void webserver_list_sort(void *priv, webserver_list_t *head, int size,
			int (*cmp)(void *priv, webserver_list_t *a, webserver_list_t *b));

	void webserver_list_sort_r(void *priv, webserver_list_t *head, int size, webserver_list_t **part,
			int (*cmp)(void *priv, webserver_list_t *a, webserver_list_t *b));

	webserver_list_t *webserver_queue(webserver_list_t *head);

#define webserver_list_for_each(pos, head) for (pos = (head)->next; pos != (head); pos = pos->next)
#define webserver_list_for_tail(pos, head) for (pos = (head)->prev; pos != (head); pos = pos->prev)
#define webserver_list_offsetof(type,member) (size_t)(&((type *)0)->member)
#define webserver_list_entry(ptr, type, member) ({const typeof(((type *)0)->member) * __mptr = (ptr);(type *)((char *)__mptr - webserver_list_offsetof(type, member));})

#ifdef __cplusplus
}
#endif

#endif


