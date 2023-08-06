
#include <webserver_urlcode.h>

static unsigned char hexchars[] = "0123456789ABCDEF";
int url_encode(void *in, int len, char *out)
{
	if (!in || !len || !out)
		return 0;

	unsigned char c;
	const char *from = in;
	const char *end = from + len;
	unsigned char *s = (unsigned char *)out;

	while (from < end) {

		c = *from++;
		if (c == ' ') {
			*s++ = '+';

		} else if ((c < '0' && c != '-' && c != '.')
				|| (c < 'A' && c > '9')
				|| (c > 'Z' && c < 'a' && c != '_')
				|| (c > 'z')) {

			s[0] = '%';
			s[1] = hexchars[c >> 4];
			s[2] = hexchars[c & 15];
			s += 3;

		} else {
			*s++ = c;
		}		     
	}

	*s = 0;
	return ((char *)s - out);
}

int url_decode(void *str, int len)
{
	if (!str || !len)
		return 0;

	int value;
	unsigned char c;
	char *from = str;
	char *end = from + len;
	char *in = str;
	char *out = str;

	for ( ;from < end; from++) {

		if (*in == '+') {
			*out = ' ';

		} else if (*in == '%'
				&& (end - from) > 2
				&& isxdigit((int) *(in + 1))
				&& isxdigit((int) *(in + 2))) {

			c = ((unsigned char *)(in + 1))[0];
			if (isupper(c))
				c = tolower(c);

			value = (c >= '0' && c <= '9' ? c - '0' : c - 'a' + 10) * 16;
			c = ((unsigned char *)(in + 1))[1];

			if (isupper(c))
				c = tolower(c);

			value += c >= '0' && c <= '9' ? c - '0' : c - 'a' + 10;
			*out = (char)value ;
			in += 2;

			from++;
			from++;

		} else {
			*out = *in;
		}

		++in;
		++out;
	}

	*out = 0;
	return ( out - (char *)str);
}




