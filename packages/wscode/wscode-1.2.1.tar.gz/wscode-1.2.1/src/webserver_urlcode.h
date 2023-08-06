
#ifndef __ADX_URLCODE_H__
#define __ADX_URLCODE_H__

#include <stdio.h>
#include <ctype.h>

int url_encode(void *in, int len, char *out);
int url_decode(void *str, int len);

#endif



