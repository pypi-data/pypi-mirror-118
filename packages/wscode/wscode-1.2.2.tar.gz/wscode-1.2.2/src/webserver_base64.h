
#ifndef __ADX_BASE64_H__
#define __ADX_BASE64_H__

#include <webserver_type.h>
#include <webserver_alloc.h>

char *base64_encode(const char *src, char *dest);
char *base64_decode(const char *src, char *dest);

#endif



