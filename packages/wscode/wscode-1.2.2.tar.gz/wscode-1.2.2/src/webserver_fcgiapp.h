
#ifndef _FCGIAPP_H
#define _FCGIAPP_H

#include <stdarg.h>
#include <sys/time.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/tcp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/un.h>
#include <signal.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#ifndef FALSE
#define FALSE (0)
#endif

#ifndef TRUE
#define TRUE  (1)
#endif

#ifndef min
#define min(a,b) ((a) < (b) ? (a) : (b))
#endif

#ifndef max
#define max(a,b) ((a) > (b) ? (a) : (b))
#endif

#define OS_Errno errno
#define FCGX_UNSUPPORTED_VERSION -2
#define FCGX_PROTOCOL_ERROR -3
#define FCGX_PARAMS_ERROR -4
#define FCGI_MAX_LENGTH 0xffff
#define FCGI_HEADER_LEN  8
#define FCGI_VERSION_1           1
#define FCGI_BEGIN_REQUEST       1
#define FCGI_END_REQUEST         3
#define FCGI_PARAMS              4
#define FCGI_STDIN               5
#define FCGI_STDOUT              6
#define FCGI_STDERR              7
#define FCGI_GET_VALUES          9
#define FCGI_GET_VALUES_RESULT  10
#define FCGI_UNKNOWN_TYPE       11
#define FCGI_NULL_REQUEST_ID     0
#define FCGI_KEEP_CONN  1
#define FCGI_RESPONDER  1
#define FCGI_AUTHORIZER 2
#define FCGI_FILTER     3
#define FCGI_REQUEST_COMPLETE 0
#define FCGI_CANT_MPX_CONN    1
#define FCGI_MAX_CONNS  "FCGI_MAX_CONNS"
#define FCGI_MAX_REQS   "FCGI_MAX_REQS"
#define FCGI_MPXS_CONNS "FCGI_MPXS_CONNS"
#define FCGI_FAIL_ACCEPT_ON_INTR	1

#define STREAM_RECORD 0
#define SKIP          1
#define BEGIN_RECORD  2
#define MGMT_RECORD   3

typedef struct {
	unsigned char version;
	unsigned char type;
	unsigned char requestIdB1;
	unsigned char requestIdB0;
	unsigned char contentLengthB1;
	unsigned char contentLengthB0;
	unsigned char paddingLength;
	unsigned char reserved;
} FCGI_Header;

typedef struct {
	unsigned char roleB1;
	unsigned char roleB0;
	unsigned char flags;
	unsigned char reserved[5];
} FCGI_BeginRequestBody;

typedef struct {
	unsigned char appStatusB3;
	unsigned char appStatusB2;
	unsigned char appStatusB1;
	unsigned char appStatusB0;
	unsigned char protocolStatus;
	unsigned char reserved[3];
} FCGI_EndRequestBody;

typedef struct {
	FCGI_Header header;
	FCGI_EndRequestBody body;
} FCGI_EndRequestRecord;

typedef struct {
	unsigned char type;
	unsigned char reserved[7];
} FCGI_UnknownTypeBody;

typedef struct {
	FCGI_Header header;
	FCGI_UnknownTypeBody body;
} FCGI_UnknownTypeRecord;

typedef struct FCGX_Stream {
	unsigned char *rdNext;    /* reader: first valid byte
				   * writer: equals stop */
	unsigned char *wrNext;    /* writer: first free byte
				   * reader: equals stop */
	unsigned char *stop;      /* reader: last valid byte + 1
				   * writer: last free byte + 1 */
	int isReader;
	int isClosed;
	int wasFCloseCalled;
	int FCGI_errno;                /* error status */
	void (*fillBuffProc) (struct FCGX_Stream *stream);
	void (*emptyBuffProc) (struct FCGX_Stream *stream, int doClose);
	void *data;
} FCGX_Stream;

typedef char **FCGX_ParamArray;
typedef struct FCGX_Request {
	int requestId;            /* valid if isBeginProcessed */
	int role;
	FCGX_Stream *in;
	FCGX_Stream *out;
	FCGX_Stream *err;
	char **envp;

	int fd;
	struct Params *paramsPtr;
	int isBeginProcessed;     /* FCGI_BEGIN_REQUEST seen */
	int keepConnection;       /* don't close fd at end of request */
	int appStatus;
	int nWriters;             /* number of open writers (0..2) */
	int flags;
	int listen_sock;
	int detached;
} FCGX_Request;

typedef struct FCGX_Stream_Data {
	unsigned char *buff;      /* buffer after alignment */
	int bufflen;              /* number of bytes buff can store */
	unsigned char *mBuff;     /* buffer as returned by malloc */
	unsigned char *buffStop;  /* reader: last valid byte + 1 of entire buffer.
				   * stop generally differs from buffStop for
				   * readers because of record structure.
				   * writer: buff + bufflen */
	int type;                 /* reader: FCGI_PARAMS or FCGI_STDIN
				   * writer: FCGI_STDOUT or FCGI_STDERR */
	int eorStop;              /* reader: stop stream at end-of-record */
	int skip;                 /* reader: don't deliver content bytes */
	int contentLen;           /* reader: bytes of unread content */
	int paddingLen;           /* reader: bytes of unread padding */
	int isAnythingWritten;    /* writer: data has been written to fd */
	int rawWrite;             /* writer: write data without stream headers */
	FCGX_Request *request; /* request data not specific to one stream */
} FCGX_Stream_Data;

void FCGX_Init(void);
int FCGX_OpenSocket(const char *path, int backlog);
int FCGX_InitRequest(FCGX_Request *request, int sock, int flags);
int FCGX_Accept_r(FCGX_Request *request);
void FCGX_Finish_r(FCGX_Request *request);
void FCGX_Free(FCGX_Request * request, int close);
char *FCGX_GetParam(const char *name, FCGX_ParamArray envp);
int FCGX_GetChar(FCGX_Stream *stream);
int FCGX_GetStr(char *str, int n, FCGX_Stream *stream);
int FCGX_PutStr(const char *str, int n, FCGX_Stream *stream);
int FCGX_FClose(FCGX_Stream *stream);
int FCGX_GetError(FCGX_Stream *stream);
void FCGX_FreeStream(FCGX_Stream **stream);

int OS_Close(int fd, int shutdown);
int OS_Accept(int listen_sock, int fail_on_intr);

#endif	/* _FCGIAPP_H */

