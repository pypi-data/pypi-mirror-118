
#include <stdio.h>
#include <string.h>
#include <webserver_list.h>

#define ARRAY_SIZE(x) (sizeof(x)/sizeof(x[0]))
#define unlikely(x)     __builtin_expect(!!(x), 0)

webserver_list_t *webserver_list_merge(void *priv,
		int (*cmp)(void *priv, webserver_list_t *a, webserver_list_t *b),
		webserver_list_t *a, webserver_list_t *b)
{
	webserver_list_t head, *tail = &head;

	while (a && b) {
		/* if equal, take 'a' -- important for sort stability */
		if ((*cmp)(priv, a, b) <= 0) {
			tail->next = a;
			a = a->next;
		} else {
			tail->next = b;
			b = b->next;
		}
		tail = tail->next;
	}
	tail->next = a?:b;
	return head.next;
}

void webserver_list_merge_and_restore_back_links(void *priv,
		int (*cmp)(void *priv, webserver_list_t *a, webserver_list_t *b),
		webserver_list_t *head, webserver_list_t *a, webserver_list_t *b)
{
	webserver_list_t *tail = head;

	while (a && b) {
		/* if equal, take 'a' -- important for sort stability */
		if ((*cmp)(priv, a, b) <= 0) {
			tail->next = a;
			a->prev = tail;
			a = a->next;
		} else {
			tail->next = b;
			b->prev = tail;
			b = b->next;
		}
		tail = tail->next;
	}
	tail->next = a ? : b;

	do {
		(*cmp)(priv, tail->next, tail->next);

		tail->next->prev = tail;
		tail = tail->next;
	} while (tail->next);

	tail->next = head;
	head->prev = tail;
}

/*
 * list_sort - sort a list
 */
void webserver_list_sort_r(void *priv, webserver_list_t *head, int size, webserver_list_t **part,
		int (*cmp)(void *priv, webserver_list_t *a, webserver_list_t *b))
{
	int lev;  /* index into part[] */
	int max_lev = 0;
	webserver_list_t *list;

	if (webserver_list_empty(head))
		return;

	memset(part, 0, sizeof(part) * size);
	head->prev->next = NULL;
	list = head->next;

	while (list) {
		webserver_list_t *cur = list;
		list = list->next;
		cur->next = NULL;

		for (lev = 0; part[lev]; lev++) {
			cur = webserver_list_merge(priv, cmp, part[lev], cur);
			part[lev] = NULL;
		}
		if (lev > max_lev) {

			if (unlikely(lev >= (int)ARRAY_SIZE(part)-1)) {

				lev--;
			}

			max_lev = lev;
		}

		part[lev] = cur;
	}

	for (lev = 0; lev < max_lev; lev++)
		if (part[lev])
			list = webserver_list_merge(priv, cmp, part[lev], list);

	webserver_list_merge_and_restore_back_links(priv, cmp, head, part[max_lev], list);
}

void webserver_list_sort(void *priv, webserver_list_t *head, int size,
		int (*cmp)(void *priv, webserver_list_t *a, webserver_list_t *b))
{
	webserver_list_t *part[size];
	webserver_list_sort_r(priv, head, size, part, cmp);
}

/*
 * webserver_queue
 */
webserver_list_t *webserver_queue(webserver_list_t *head)
{
	webserver_list_t *p = head->next;
	if (p != head) {

		webserver_list_del(p);
		return p;
	}

	return NULL;
}



