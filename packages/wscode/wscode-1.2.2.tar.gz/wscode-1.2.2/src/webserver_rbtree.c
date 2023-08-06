
#include <webserver_rbtree.h>

void webserver_rbtree_set_parent(webserver_rbtree_node *rb, webserver_rbtree_node *p)
{
	rb->rb_parent_color = (rb->rb_parent_color & 3) | (unsigned long)p;
}

void webserver_rbtree_set_color(webserver_rbtree_node *rb, int color)
{
	rb->rb_parent_color = (rb->rb_parent_color & ~1) | color;
}

void webserver_rbtree_link_node(webserver_rbtree_node *node, webserver_rbtree_node *parent, webserver_rbtree_node **rb_link)
{

	node->rb_parent_color = (unsigned long )parent;
	node->rb_left = node->rb_right = NULL;
	*rb_link = node;
}

void webserver_rbtree_rotate_left(webserver_rbtree_node *node, webserver_rbtree_head *head)
{
	webserver_rbtree_node *right = node->rb_right;
	webserver_rbtree_node *parent = rb_parent(node);

	if ((node->rb_right = right->rb_left))
		webserver_rbtree_set_parent(right->rb_left, node);

	right->rb_left = node;
	webserver_rbtree_set_parent(right, parent);

	if (parent) {

		if (node == parent->rb_left)
			parent->rb_left = right;
		else
			parent->rb_right = right;

	} else {

		head->rb_node = right;
	}

	webserver_rbtree_set_parent(node, right);
}

void webserver_rbtree_rotate_right(webserver_rbtree_node *node, webserver_rbtree_head *head)
{
	webserver_rbtree_node *left = node->rb_left;
	webserver_rbtree_node *parent = rb_parent(node);

	if ((node->rb_left = left->rb_right))
		webserver_rbtree_set_parent(left->rb_right, node);

	left->rb_right = node;
	webserver_rbtree_set_parent(left, parent);

	if (parent) {

		if (node == parent->rb_right)
			parent->rb_right = left;
		else
			parent->rb_left = left;

	} else {

		head->rb_node = left;
	}

	webserver_rbtree_set_parent(node, left);
}

void webserver_rbtree_insert_color(webserver_rbtree_node *node, webserver_rbtree_head *head)
{

	webserver_rbtree_node *parent, *gparent;

	while ((parent = rb_parent(node)) && rb_is_red(parent)) {

		gparent = rb_parent(parent);

		if (parent == gparent->rb_left) {

			register webserver_rbtree_node *uncle = gparent->rb_right;
			if (uncle && rb_is_red(uncle)) {

				rb_set_black(uncle);
				rb_set_black(parent);
				rb_set_red(gparent);
				node = gparent;
				continue;
			}

			if (parent->rb_right == node) {

				register webserver_rbtree_node *tmp;
				webserver_rbtree_rotate_left(parent, head);
				tmp = parent;
				parent = node;
				node = tmp;
			}

			rb_set_black(parent);
			rb_set_red(gparent);
			webserver_rbtree_rotate_right(gparent, head);

		} else {

			register webserver_rbtree_node *uncle = gparent->rb_left;
			if (uncle && rb_is_red(uncle)) {

				rb_set_black(uncle);
				rb_set_black(parent);
				rb_set_red(gparent);
				node = gparent;
				continue;
			}

			if (parent->rb_left == node) {

				register webserver_rbtree_node *tmp;
				webserver_rbtree_rotate_right(parent, head);
				tmp = parent;
				parent = node;
				node = tmp;
			}

			rb_set_black(parent);
			rb_set_red(gparent);
			webserver_rbtree_rotate_left(gparent, head);
		}
	}

	rb_set_black(head->rb_node);
}

void webserver_rbtree_delete_color(webserver_rbtree_node *node, webserver_rbtree_node *parent, webserver_rbtree_head *head)
{

	webserver_rbtree_node *other = NULL;

	while ((!node || rb_is_black(node)) && node != head->rb_node) {

		if (parent->rb_left == node) {

			other = parent->rb_right;

			if (rb_is_red(other)) {

				rb_set_black(other);
				rb_set_red(parent);
				webserver_rbtree_rotate_left(parent, head);
				other = parent->rb_right;
			}

			if ((!other->rb_left || rb_is_black(other->rb_left)) &&
					(!other->rb_right || rb_is_black(other->rb_right))) {

				rb_set_red(other);
				node = parent;
				parent = rb_parent(node);

			} else {

				if (!other->rb_right || rb_is_black(other->rb_right)) {

					rb_set_black(other->rb_left);
					rb_set_red(other);
					webserver_rbtree_rotate_right(other, head);
					other = parent->rb_right;
				}

				webserver_rbtree_set_color(other, rb_color(parent));
				rb_set_black(parent);
				rb_set_black(other->rb_right);
				webserver_rbtree_rotate_left(parent, head);
				node = head->rb_node;
				break;
			}

		} else {

			other = parent->rb_left;

			if (rb_is_red(other)) {

				rb_set_black(other);
				rb_set_red(parent);
				webserver_rbtree_rotate_right(parent, head);
				other = parent->rb_left;
			}

			if ((!other->rb_left || rb_is_black(other->rb_left)) &&
					(!other->rb_right || rb_is_black(other->rb_right))) {

				rb_set_red(other);
				node = parent;
				parent = rb_parent(node);

			} else {

				if (!other->rb_left || rb_is_black(other->rb_left)) {

					rb_set_black(other->rb_right);
					rb_set_red(other);
					webserver_rbtree_rotate_left(other, head);
					other = parent->rb_left;
				}

				webserver_rbtree_set_color(other, rb_color(parent));
				rb_set_black(parent);
				rb_set_black(other->rb_left);
				webserver_rbtree_rotate_right(parent, head);
				node = head->rb_node;
				break;
			}
		}
	}

	if (node)rb_set_black(node);
}

void webserver_rbtree_delete(webserver_rbtree_head *head, webserver_rbtree_node *node)
{

	int color;
	webserver_rbtree_node *child, *parent;

	if (!node->rb_left) {

		child = node->rb_right;

	} else if (!node->rb_right) {

		child = node->rb_left;

	} else {

		webserver_rbtree_node *old = node, *left;

		node = node->rb_right;
		while ((left = node->rb_left) != NULL)
			node = left;

		if (rb_parent(old)) {

			if (rb_parent(old)->rb_left == old)
				rb_parent(old)->rb_left = node;
			else
				rb_parent(old)->rb_right = node;

		} else {

			head->rb_node = node;
		}

		child = node->rb_right;
		parent = rb_parent(node);
		color = rb_color(node);

		if (parent == old) {

			parent = node;

		} else {

			if (child)webserver_rbtree_set_parent(child, parent);
			parent->rb_left = child;

			node->rb_right = old->rb_right;
			webserver_rbtree_set_parent(old->rb_right, node);
		}

		node->rb_parent_color = old->rb_parent_color;
		node->rb_left = old->rb_left;
		webserver_rbtree_set_parent(old->rb_left, node);

		if (color == 1)webserver_rbtree_delete_color(child, parent, head);
		return;
	}

	parent = rb_parent(node);
	color = rb_color(node);

	if (child)webserver_rbtree_set_parent(child, parent);

	if (parent) {

		if (parent->rb_left == node)
			parent->rb_left = child;
		else
			parent->rb_right = child;

	} else {

		head->rb_node = child;
	}

	if (color == 1)webserver_rbtree_delete_color(child, parent, head);
}

/* for print */
void _webserver_rbtree_print(webserver_rbtree_node *p)
{
	// webserver_rbtree_node *node = (webserver_rbtree_node *)p;
	// fprintf(stdout, "[tree][%d][%s]\n", node->number, node->string);
	if (p->rb_left) _webserver_rbtree_print(p->rb_left);
	if (p->rb_right)_webserver_rbtree_print(p->rb_right);
}

void webserver_rbtree_print(webserver_rbtree_head *head)
{
	if (!head->rb_node) return;
	_webserver_rbtree_print(head->rb_node);
}

/* string */
webserver_rbtree_node *webserver_rbtree_string_add(webserver_rbtree_head *head, webserver_rbtree_node *new_node)
{
	webserver_rbtree_node *parent = NULL;
	webserver_rbtree_node **p = &head->rb_node;
	webserver_rbtree_node *node = NULL;

	if (!new_node->str.str || !new_node->str.len)
		return NULL;

	while (*p) {

		parent = *p;
		node = parent;

		int retval = strncmp(node->str.str, new_node->str.str, new_node->str.len);
		if (retval < 0) {
			p = &(*p)->rb_left;

		} else if (retval > 0) {
			p = &(*p)->rb_right;

		} else {

			if (node->str.len == new_node->str.len)
				return NULL;

			if (node->str.len < new_node->str.len)
				p = &(*p)->rb_left;

			else
				p = &(*p)->rb_right;
		}
	}

	webserver_rbtree_link_node(new_node, parent, p);
	webserver_rbtree_insert_color(new_node, head);
	return node;
}

webserver_rbtree_node *webserver_rbtree_string_find(webserver_rbtree_head *head, const char *key, size_t len)
{
	webserver_rbtree_node *p = head->rb_node;
	webserver_rbtree_node *node = NULL;

	if (!key || !len)
		return NULL;

	while (p) {

		node = (webserver_rbtree_node *)p;
		int retval = strncmp(node->str.str, key, len);
		if (retval < 0) {
			p = p->rb_left;

		} else if (retval > 0) {
			p = p->rb_right;

		} else {

			if (node->str.len == len)
				return node;

			if (node->str.len < len)
				p = p->rb_left;

			else
				p = p->rb_right;
		}
	}

	return NULL;
}

/* number */
webserver_rbtree_node *webserver_rbtree_number_add(webserver_rbtree_head *head, webserver_rbtree_node *new_node)
{

	webserver_rbtree_node *parent = NULL;
	webserver_rbtree_node **p = &head->rb_node;
	webserver_rbtree_node *node = NULL;

	while (*p) {

		parent = *p;
		node = (webserver_rbtree_node *)parent;

		if (new_node->number < node->number) 
			p = &(*p)->rb_left;

		else if (new_node->number > node->number) 
			p = &(*p)->rb_right;

		else return NULL;
	}

	webserver_rbtree_link_node(new_node, parent, p);
	webserver_rbtree_insert_color(new_node, head);
	return node;
}

webserver_rbtree_node *webserver_rbtree_number_find(webserver_rbtree_head *head, long long key)
{

	webserver_rbtree_node *p = head->rb_node;
	webserver_rbtree_node *node = NULL;

	while (p) {

		node = (webserver_rbtree_node *)p;

		if (key < node->number)
			p = p->rb_left;

		else if (key > node->number)
			p = p->rb_right;

		else return node;
	}

	return NULL;
}

/* pointer */
webserver_rbtree_node *webserver_rbtree_pointer_add(webserver_rbtree_head *head, webserver_rbtree_node *new_node)
{

	webserver_rbtree_node *parent = NULL;
	webserver_rbtree_node **p = &head->rb_node;
	webserver_rbtree_node *node = NULL;

	while (*p) {

		parent = *p;
		node = (webserver_rbtree_node *)parent;

		if (new_node->pointer < node->pointer)
			p = &(*p)->rb_left;

		else if (new_node->pointer > node->pointer)
			p = &(*p)->rb_right;

		else return NULL;
	}

	webserver_rbtree_link_node(new_node, parent, p);
	webserver_rbtree_insert_color(new_node, head);
	return node;
}

webserver_rbtree_node *webserver_rbtree_pointer_find(webserver_rbtree_head *head, void *key)
{
	webserver_rbtree_node *p = head->rb_node;
	webserver_rbtree_node *node = NULL;

	while (p) {

		node = (webserver_rbtree_node *)p;

		if (key < node->pointer)
			p = p->rb_left;

		else if (key > node->pointer)
			p = p->rb_right;

		else return node;
	}

	return NULL;
}




