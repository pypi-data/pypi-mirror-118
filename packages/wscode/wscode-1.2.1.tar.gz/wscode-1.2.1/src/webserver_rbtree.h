
#ifndef	__ADX_RBTREE_H__
#define	__ADX_RBTREE_H__


#include <stdio.h>
#include <string.h>

#ifdef __cplusplus
"C" { 
#endif

	typedef struct {
		char *str;
		size_t len;
	} webserver_rbtree_str;

	typedef struct webserver_rbtree_node webserver_rbtree_node;
	struct webserver_rbtree_node {

		unsigned long  rb_parent_color;
		webserver_rbtree_node *rb_right;
		webserver_rbtree_node *rb_left;
		union {
			webserver_rbtree_str str;
			long long number;
			void *pointer;
		};

	};

	typedef struct {
		webserver_rbtree_node *rb_node;

	} webserver_rbtree_head;

	void webserver_rbtree_insert_color(webserver_rbtree_node *node, webserver_rbtree_head *head);
	void webserver_rbtree_link_node(webserver_rbtree_node * node, webserver_rbtree_node *parent, webserver_rbtree_node **rb_link);
	void webserver_rbtree_delete(webserver_rbtree_head *head, webserver_rbtree_node *node);

	webserver_rbtree_node *webserver_rbtree_string_add(webserver_rbtree_head *head, webserver_rbtree_node *new_node);
	webserver_rbtree_node *webserver_rbtree_string_find(webserver_rbtree_head *head, const char *key, size_t len);

	webserver_rbtree_node *webserver_rbtree_number_add(webserver_rbtree_head *head, webserver_rbtree_node *new_node);
	webserver_rbtree_node *webserver_rbtree_number_find(webserver_rbtree_head *head, long long key);

	webserver_rbtree_node *webserver_rbtree_pointer_add(webserver_rbtree_head *head, webserver_rbtree_node *new_node);
	webserver_rbtree_node *webserver_rbtree_pointer_find(webserver_rbtree_head *head, void *key);


#define RB_ROOT	(webserver_rbtree_head) {0}
#define rb_is_red(r) (!rb_color(r))
#define rb_is_black(r) rb_color(r)
#define rb_set_red(r) do { (r)->rb_parent_color &= ~1; } while (0)
#define rb_set_black(r) do { (r)->rb_parent_color |= 1; } while (0)
#define rb_parent(r) ((webserver_rbtree_node *)((r)->rb_parent_color & ~3))
#define rb_color(r) ((r)->rb_parent_color & 1)
#define rb_offsetof(type,member) (size_t)(&((type *)0)->member)
#define rb_entry(ptr, type, member) ({const typeof(((type *)0)->member) * __mptr = (ptr);(type *)((char *)__mptr - rb_offsetof(type, member));})

#ifdef __cplusplus
}
#endif

#endif



