
#ifndef __ADX_UUID_H__
#define __ADX_UUID_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <ctype.h>
#include <fcntl.h>

#ifdef __cplusplus
extern "C" {
#endif

	void webserver_uuid_generate(unsigned char * out);
	void webserver_uuid_unparse(unsigned char * uu, char *out);
	char *webserver_uuid(char *out);

#ifdef __cplusplus
}
#endif

#endif






