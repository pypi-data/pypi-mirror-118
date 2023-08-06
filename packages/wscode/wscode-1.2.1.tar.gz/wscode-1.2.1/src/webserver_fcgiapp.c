
#include "webserver_fcgiapp.h"

static char *StringCopy(char *str)
{
	int strLen = strlen(str);
	char *newString = (char *)malloc(strLen + 1);
	memcpy(newString, str, strLen);
	newString[strLen] = '\000';
	return newString;
}

int FCGX_GetChar(FCGX_Stream *stream)
{
	if (stream->isClosed || ! stream->isReader)
		return EOF;

	if (stream->rdNext != stream->stop)
		return *stream->rdNext++;

	stream->fillBuffProc(stream);
	if (stream->isClosed)
		return EOF;

	if (stream->rdNext != stream->stop)
		return *stream->rdNext++;

	return EOF;
}

int FCGX_GetStr(char *str, int n, FCGX_Stream *stream)
{
	int m, bytesMoved = 0;
	if (stream->isClosed || ! stream->isReader || n <= 0) {
		return 0;
	}

	if(n <= (stream->stop - stream->rdNext)) {
		memcpy(str, stream->rdNext, n);
		stream->rdNext += n;
		return n;
	}

	for (;;) {

		if(stream->rdNext != stream->stop) {
			m = min(n - bytesMoved, stream->stop - stream->rdNext);
			memcpy(str, stream->rdNext, m);
			bytesMoved += m;
			stream->rdNext += m;
			if(bytesMoved == n)
				return bytesMoved;
			str += m;
		}

		if(stream->isClosed || !stream->isReader)
			return bytesMoved;

		stream->fillBuffProc(stream);
		if (stream->isClosed)
			return bytesMoved;
	}
}

int FCGX_PutStr(const char *str, int n, FCGX_Stream *stream)
{
	int m, bytesMoved = 0;
	if(n <= (stream->stop - stream->wrNext)) {
		memcpy(stream->wrNext, str, n);
		stream->wrNext += n;
		return n;
	}

	for (;;) {
		if(stream->wrNext != stream->stop) {
			m = min(n - bytesMoved, stream->stop - stream->wrNext);
			memcpy(stream->wrNext, str, m);
			bytesMoved += m;
			stream->wrNext += m;
			if(bytesMoved == n)
				return bytesMoved;
			str += m;
		}
		if(stream->isClosed || stream->isReader)
			return -1;
		stream->emptyBuffProc(stream, FALSE);
	}
}

int FCGX_FClose(FCGX_Stream *stream)
{
	if (stream == NULL) return 0;

	if(!stream->wasFCloseCalled) {
		if(!stream->isReader) {
			stream->emptyBuffProc(stream, TRUE);
		}
		stream->wasFCloseCalled = TRUE;
		stream->isClosed = TRUE;
		if(stream->isReader) {
			stream->wrNext = stream->stop = stream->rdNext;
		} else {
			stream->rdNext = stream->stop = stream->wrNext;
		}
	}
	return (stream->FCGI_errno == 0) ? 0 : EOF;
}

static void SetError(FCGX_Stream *stream, int FCGI_errno)
{
	if(stream->FCGI_errno == 0) {
		stream->FCGI_errno = FCGI_errno;
	}

	stream->isClosed = TRUE;
}

int FCGX_GetError(FCGX_Stream *stream) {
	return stream->FCGI_errno;
}

typedef struct Params {
	FCGX_ParamArray vec;    /* vector of strings */
	int length;		    /* number of string vec can hold */
	char **cur;		    /* current item in vec; *cur == NULL */
} Params;
typedef Params *ParamsPtr;
static ParamsPtr NewParams(int length)
{
	ParamsPtr result;
	result = (Params *)malloc(sizeof(Params));
	result->vec = (char **)malloc(length * sizeof(char *));
	result->length = length;
	result->cur = result->vec;
	*result->cur = NULL;
	return result;
}

static void FreeParams(ParamsPtr *paramsPtrPtr)
{
	ParamsPtr paramsPtr = *paramsPtrPtr;
	char **p;
	if(paramsPtr == NULL) {
		return;
	}
	for (p = paramsPtr->vec; p < paramsPtr->cur; p++) {
		free(*p);
	}
	free(paramsPtr->vec);
	free(paramsPtr);
	*paramsPtrPtr = NULL;
}

static void PutParam(ParamsPtr paramsPtr, char *nameValue)
{
	int size;

	*paramsPtr->cur++ = nameValue;
	size = paramsPtr->cur - paramsPtr->vec;
	if(size >= paramsPtr->length) {
		paramsPtr->length *= 2;
		paramsPtr->vec = (FCGX_ParamArray)realloc(paramsPtr->vec, paramsPtr->length * sizeof(char *));
		paramsPtr->cur = paramsPtr->vec + size;
	}
	*paramsPtr->cur = NULL;
}

char *FCGX_GetParam(const char *name, FCGX_ParamArray envp)
{
	int len;
	char **p;
	if (name == NULL || envp == NULL)
		return NULL;

	len = strlen(name);
	for (p = envp; *p; ++p) {
		if((strncmp(name, *p, len) == 0) && ((*p)[len] == '=')) {
			return *p+len+1;
		}
	}

	return NULL;
}

static int ReadParams(Params *paramsPtr, FCGX_Stream *stream)
{
	int nameLen, valueLen;
	unsigned char lenBuff[3];
	char *nameValue;

	while((nameLen = FCGX_GetChar(stream)) != EOF) {
		/*
		 * Read name length (one or four bytes) and value length
		 * (one or four bytes) from stream.
		 */
		if((nameLen & 0x80) != 0) {
			if(FCGX_GetStr((char *) &lenBuff[0], 3, stream) != 3) {
				SetError(stream, FCGX_PARAMS_ERROR);
				return -1;
			}
			nameLen = ((nameLen & 0x7f) << 24) + (lenBuff[0] << 16)
				+ (lenBuff[1] << 8) + lenBuff[2];
		}
		if((valueLen = FCGX_GetChar(stream)) == EOF) {
			SetError(stream, FCGX_PARAMS_ERROR);
			return -1;
		}
		if((valueLen & 0x80) != 0) {
			if(FCGX_GetStr((char *) &lenBuff[0], 3, stream) != 3) {
				SetError(stream, FCGX_PARAMS_ERROR);
				return -1;
			}
			valueLen = ((valueLen & 0x7f) << 24) + (lenBuff[0] << 16)
				+ (lenBuff[1] << 8) + lenBuff[2];
		}
		/*
		 * nameLen and valueLen are now valid; read the name and value
		 * from stream and construct a standard environment entry.
		 */
		nameValue = (char *)malloc(nameLen + valueLen + 2);
		if(FCGX_GetStr(nameValue, nameLen, stream) != nameLen) {
			SetError(stream, FCGX_PARAMS_ERROR);
			free(nameValue);
			return -1;
		}
		*(nameValue + nameLen) = '=';
		if(FCGX_GetStr(nameValue + nameLen + 1, valueLen, stream)
				!= valueLen) {
			SetError(stream, FCGX_PARAMS_ERROR);
			free(nameValue);
			return -1;
		}
		*(nameValue + nameLen + valueLen + 1) = '\0';
		PutParam(paramsPtr, nameValue);
	}

	return 0;
}

static FCGI_Header MakeHeader(
		int type,
		int requestId,
		int contentLength,
		int paddingLength)
{
	FCGI_Header header;
	header.version = FCGI_VERSION_1;
	header.type             = (unsigned char) type;
	header.requestIdB1      = (unsigned char) ((requestId     >> 8) & 0xff);
	header.requestIdB0      = (unsigned char) ((requestId         ) & 0xff);
	header.contentLengthB1  = (unsigned char) ((contentLength >> 8) & 0xff);
	header.contentLengthB0  = (unsigned char) ((contentLength     ) & 0xff);
	header.paddingLength    = (unsigned char) paddingLength;
	header.reserved         =  0;
	return header;
}

static FCGI_EndRequestBody MakeEndRequestBody(
		int appStatus,
		int protocolStatus)
{
	FCGI_EndRequestBody body;
	body.appStatusB3    = (unsigned char) ((appStatus >> 24) & 0xff);
	body.appStatusB2    = (unsigned char) ((appStatus >> 16) & 0xff);
	body.appStatusB1    = (unsigned char) ((appStatus >>  8) & 0xff);
	body.appStatusB0    = (unsigned char) ((appStatus      ) & 0xff);
	body.protocolStatus = (unsigned char) protocolStatus;
	memset(body.reserved, 0, sizeof(body.reserved));
	return body;
}

static FCGI_UnknownTypeBody MakeUnknownTypeBody(
		int type)
{
	FCGI_UnknownTypeBody body;
	body.type = (unsigned char) type;
	memset(body.reserved, 0, sizeof(body.reserved));
	return body;
}

static int AlignInt8(unsigned n) {
	return (n + 7) & (UINT_MAX - 7);
}

static unsigned char *AlignPtr8(unsigned char *p) {
	unsigned long u = (unsigned long) p;
	u = ((u + 7) & (ULONG_MAX - 7)) - u;
	return p + u;
}

static void WriteCloseRecords(struct FCGX_Stream *stream)
{
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)stream->data;
	/*
	 * Enter rawWrite mode so final records won't be encapsulated as
	 * stream data.
	 */
	data->rawWrite = TRUE;
	/*
	 * Generate EOF for stream content if needed.
	 */
	if(!(data->type == FCGI_STDERR
				&& stream->wrNext == data->buff
				&& !data->isAnythingWritten)) {
		FCGI_Header header;
		header = MakeHeader(data->type, data->request->requestId, 0, 0);
		FCGX_PutStr((char *) &header, sizeof(header), stream);
	};
	/*
	 * Generate FCGI_END_REQUEST record if needed.
	 */
	if(data->request->nWriters == 1) {
		FCGI_EndRequestRecord endRequestRecord;
		endRequestRecord.header = MakeHeader(FCGI_END_REQUEST,
				data->request->requestId,
				sizeof(endRequestRecord.body), 0);
		endRequestRecord.body = MakeEndRequestBody(
				data->request->appStatus, FCGI_REQUEST_COMPLETE);
		FCGX_PutStr((char *) &endRequestRecord,
				sizeof(endRequestRecord), stream);
	}
	data->request->nWriters--;
}

static int write_it_all(int fd, char *buf, int len)
{
	int wrote = 0;
	while (len) {
		wrote = write(fd, buf, len);
		if (wrote < 0)
			return wrote;
		len -= wrote;
		buf += wrote;
	}
	return len;
}

static void EmptyBuffProc(struct FCGX_Stream *stream, int doClose)
{
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)stream->data;
	int cLen, eLen;
	/*
	 * If the buffer contains stream data, fill in the header.
	 * Pad the record to a multiple of 8 bytes in length.  Padding
	 * can't overflow the buffer because the buffer is a multiple
	 * of 8 bytes in length.  If the buffer contains no stream
	 * data, reclaim the space reserved for the header.
	 */
	if(!data->rawWrite) {
		cLen = stream->wrNext - data->buff - sizeof(FCGI_Header);
		if(cLen > 0) {
			eLen = AlignInt8(cLen);
			/*
			 * Giving the padding a well-defined value keeps Purify happy.
			 */
			memset(stream->wrNext, 0, eLen - cLen);
			stream->wrNext += eLen - cLen;
			*((FCGI_Header *) data->buff)
				= MakeHeader(data->type,
						data->request->requestId, cLen, eLen - cLen);
		} else {
			stream->wrNext = data->buff;
		}
	}
	if(doClose) {
		WriteCloseRecords(stream);
	};
	if (stream->wrNext != data->buff) {
		data->isAnythingWritten = TRUE;
		if (write_it_all(data->request->fd, (char *)data->buff, stream->wrNext - data->buff) < 0) {
			SetError(stream, OS_Errno);
			return;
		}
		stream->wrNext = data->buff;
	}
	/*
	 * The buffer is empty.
	 */
	if(!data->rawWrite) {
		stream->wrNext += sizeof(FCGI_Header);
	}
}

static int ProcessManagementRecord(int type, FCGX_Stream *stream)
{
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)stream->data;
	ParamsPtr paramsPtr = NewParams(3);
	char **pPtr;
	char response[64]; /* 64 = 8 + 3*(1+1+14+1)* + padding */
	char *responseP = &response[FCGI_HEADER_LEN];
	char *name, value = '\0';
	int len, paddedLen;
	if(type == FCGI_GET_VALUES) {
		ReadParams(paramsPtr, stream);
		if((FCGX_GetError(stream) != 0) || (data->contentLen != 0)) {
			FreeParams(&paramsPtr);
			return FCGX_PROTOCOL_ERROR;
		}
		for (pPtr = paramsPtr->vec; pPtr < paramsPtr->cur; pPtr++) {
			name = *pPtr;
			*(strchr(name, '=')) = '\0';
			if(strcmp(name, FCGI_MAX_CONNS) == 0) {
				value = '1';
			} else if(strcmp(name, FCGI_MAX_REQS) == 0) {
				value = '1';
			} else if(strcmp(name, FCGI_MPXS_CONNS) == 0) {
				value = '0';
			} else {
				name = NULL;
			}
			if(name != NULL) {
				len = strlen(name);
				sprintf(responseP, "%c%c%s%c", len, 1, name, value);
				responseP += len + 3;
			}
		}
		len = responseP - &response[FCGI_HEADER_LEN];
		paddedLen = AlignInt8(len);
		*((FCGI_Header *) response)
			= MakeHeader(FCGI_GET_VALUES_RESULT, FCGI_NULL_REQUEST_ID,
					len, paddedLen - len);
		FreeParams(&paramsPtr);
	} else {
		paddedLen = len = sizeof(FCGI_UnknownTypeBody);
		((FCGI_UnknownTypeRecord *) response)->header
			= MakeHeader(FCGI_UNKNOWN_TYPE, FCGI_NULL_REQUEST_ID,
					len, 0);
		((FCGI_UnknownTypeRecord *) response)->body
			= MakeUnknownTypeBody(type);
	}
	if (write_it_all(data->request->fd, response, FCGI_HEADER_LEN + paddedLen) < 0) {
		SetError(stream, OS_Errno);
		return -1;
	}

	return MGMT_RECORD;
}

static int ProcessBeginRecord(int requestId, FCGX_Stream *stream)
{
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)stream->data;
	FCGI_BeginRequestBody body;
	if(requestId == 0 || data->contentLen != sizeof(body)) {
		return FCGX_PROTOCOL_ERROR;
	}
	if(data->request->isBeginProcessed) {
		/*
		 * The Web server is multiplexing the connection.  This library
		 * doesn't know how to handle multiplexing, so respond with
		 * FCGI_END_REQUEST{protocolStatus = FCGI_CANT_MPX_CONN}
		 */
		FCGI_EndRequestRecord endRequestRecord;
		endRequestRecord.header = MakeHeader(FCGI_END_REQUEST,
				requestId, sizeof(endRequestRecord.body), 0);
		endRequestRecord.body
			= MakeEndRequestBody(0, FCGI_CANT_MPX_CONN);
		if (write_it_all(data->request->fd, (char *)&endRequestRecord, sizeof(endRequestRecord)) < 0) {
			SetError(stream, OS_Errno);
			return -1;
		}

		return SKIP;
	}
	/*
	 * Accept this new request.  Read the record body.
	 */
	data->request->requestId = requestId;
	if(FCGX_GetStr((char *) &body, sizeof(body), stream)
			!= sizeof(body)) {
		return FCGX_PROTOCOL_ERROR;
	}
	data->request->keepConnection = (body.flags & FCGI_KEEP_CONN);
	data->request->role = (body.roleB1 << 8) + body.roleB0;
	data->request->isBeginProcessed = TRUE;
	return BEGIN_RECORD;
}

static int ProcessHeader(FCGI_Header header, FCGX_Stream *stream)
{
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)stream->data;
	int requestId;
	if(header.version != FCGI_VERSION_1) {
		return FCGX_UNSUPPORTED_VERSION;
	}
	requestId =        (header.requestIdB1 << 8)
		+ header.requestIdB0;
	data->contentLen = (header.contentLengthB1 << 8)
		+ header.contentLengthB0;
	data->paddingLen = header.paddingLength;
	if(header.type == FCGI_BEGIN_REQUEST) {
		return ProcessBeginRecord(requestId, stream);
	}
	if(requestId  == FCGI_NULL_REQUEST_ID) {
		return ProcessManagementRecord(header.type, stream);
	}
	if(requestId != data->request->requestId) {
		return SKIP;
	}
	if(header.type != data->type) {
		return FCGX_PROTOCOL_ERROR;
	}
	return STREAM_RECORD;
}

static void FillBuffProc(FCGX_Stream *stream)
{
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)stream->data;
	FCGI_Header header;
	int headerLen = 0;
	int sizeof_header = sizeof(header);
	int status, count;

	for (;;) {
		/*
		 * If data->buff is empty, do a read.
		 */
		if(stream->rdNext == data->buffStop) {
			count = read(data->request->fd, (char *)data->buff,
					data->bufflen);
			if(count <= 0) {
				SetError(stream, (count == 0 ? FCGX_PROTOCOL_ERROR : OS_Errno));
				return;
			}
			stream->rdNext = data->buff;
			data->buffStop = data->buff + count;
		}
		/*
		 * Now data->buff is not empty.  If the current record contains
		 * more content bytes, deliver all that are present in data->buff.
		 */
		if(data->contentLen > 0) {
			count = min(data->contentLen, data->buffStop - stream->rdNext);
			data->contentLen -= count;
			if(!data->skip) {
				stream->wrNext = stream->stop = stream->rdNext + count;
				return;
			} else {
				stream->rdNext += count;
				if(data->contentLen > 0) {
					continue;
				} else {
					data->skip = FALSE;
				}
			}
		}
		/*
		 * If the current record (whose content has been fully consumed by
		 * the client) was padded, skip over the padding bytes.
		 */
		if(data->paddingLen > 0) {
			count = min(data->paddingLen, data->buffStop - stream->rdNext);
			data->paddingLen -= count;
			stream->rdNext += count;
			if(data->paddingLen > 0) {
				continue;
			}
		}
		/*
		 * All done with the current record, including the padding.
		 * If we're in a recursive call from ProcessHeader, deliver EOF.
		 */
		if(data->eorStop) {
			stream->stop = stream->rdNext;
			stream->isClosed = TRUE;
			return;
		}
		/*
		 * Fill header with bytes from the input buffer.
		 */
		count = min(sizeof_header - headerLen,
				data->buffStop - stream->rdNext);

		memcpy(((char *)(&header)) + headerLen, stream->rdNext, count);
		headerLen += count;
		stream->rdNext += count;

		if(headerLen < sizeof_header) {
			continue;
		}

		/*
		 * Interpret header.  eorStop prevents ProcessHeader from reading
		 * past the end-of-record when using stream to read content.
		 */
		headerLen = 0;
		data->eorStop = TRUE;
		stream->stop = stream->rdNext;
		status = ProcessHeader(header, stream);
		data->eorStop = FALSE;
		stream->isClosed = FALSE;
		switch(status) {
			case STREAM_RECORD:
				/*
				 * If this stream record header marked the end of stream
				 * data deliver EOF to the stream client, otherwise loop
				 * and deliver data.
				 *
				 * XXX: If this is final stream and
				 * stream->rdNext != data->buffStop, buffered
				 * data is next request (server pipelining)?
				 */
				if(data->contentLen == 0) {
					stream->wrNext = stream->stop = stream->rdNext;
					stream->isClosed = TRUE;
					return;
				}
				break;
			case SKIP:
				data->skip = TRUE;
				break;
			case BEGIN_RECORD:
				/*
				 * If this header marked the beginning of a new
				 * request, return role information to caller.
				 */
				return;
				break;
			case MGMT_RECORD:
				break;
			default:
				SetError(stream, status);
				return;
		}
	}
}

static FCGX_Stream *NewStream(FCGX_Request *request, int bufflen, int isReader, int streamType)
{
	/*
	 * XXX: It would be a lot cleaner to have a NewStream that only
	 * knows about the type FCGX_Stream, with all other
	 * necessary data passed in.  It appears that not just
	 * data and the two procs are needed for initializing stream,
	 * but also data->buff and data->buffStop.  This has implications
	 * for procs that want to swap buffers, too.
	 */
	FCGX_Stream *stream = (FCGX_Stream *)malloc(sizeof(FCGX_Stream));
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)malloc(sizeof(FCGX_Stream_Data));
	data->request = request;
	bufflen = AlignInt8(min(max(bufflen, 32), FCGI_MAX_LENGTH + 1));
	data->bufflen = bufflen;
	data->mBuff = (unsigned char *)malloc(bufflen);
	data->buff = AlignPtr8(data->mBuff);
	if(data->buff != data->mBuff) {
		data->bufflen -= 8;
	}
	if(isReader) {
		data->buffStop = data->buff;
	} else {
		data->buffStop = data->buff + data->bufflen;
	}
	data->type = streamType;
	data->eorStop = FALSE;
	data->skip = FALSE;
	data->contentLen = 0;
	data->paddingLen = 0;
	data->isAnythingWritten = FALSE;
	data->rawWrite = FALSE;

	stream->data = data;
	stream->isReader = isReader;
	stream->isClosed = FALSE;
	stream->wasFCloseCalled = FALSE;
	stream->FCGI_errno = 0;
	if(isReader) {
		stream->fillBuffProc = FillBuffProc;
		stream->emptyBuffProc = NULL;
		stream->rdNext = data->buff;
		stream->stop = stream->rdNext;
		stream->wrNext = stream->stop;
	} else {
		stream->fillBuffProc = NULL;
		stream->emptyBuffProc = EmptyBuffProc;
		stream->wrNext = data->buff + sizeof(FCGI_Header);
		stream->stop = data->buffStop;
		stream->rdNext = stream->stop;
	}
	return stream;
}

void FCGX_FreeStream(FCGX_Stream **streamPtr)
{
	FCGX_Stream *stream = *streamPtr;
	FCGX_Stream_Data *data;
	if(stream == NULL) {
		return;
	}
	data = (FCGX_Stream_Data *)stream->data;
	data->request = NULL;
	free(data->mBuff);
	free(data);
	free(stream);
	*streamPtr = NULL;
}

static FCGX_Stream *SetReaderType(FCGX_Stream *stream, int streamType)
{
	FCGX_Stream_Data *data = (FCGX_Stream_Data *)stream->data;
	data->type = streamType;
	data->eorStop = FALSE;
	data->skip = FALSE;
	data->contentLen = 0;
	data->paddingLen = 0;
	stream->wrNext = stream->stop = stream->rdNext;
	stream->isClosed = FALSE;
	return stream;
}

static FCGX_Stream *NewReader(FCGX_Request *request, int bufflen, int streamType)
{
	return NewStream(request, bufflen, TRUE, streamType);
}

static FCGX_Stream *NewWriter(FCGX_Request *request, int bufflen, int streamType)
{
	return NewStream(request, bufflen, FALSE, streamType);
}

void FCGX_Finish_r(FCGX_Request *request)
{
	int close;

	if (request == NULL) {
		return;
	}

	close = !request->keepConnection;

	/* This should probably use a 'status' member instead of 'in' */
	if (request->in) {
		close |= FCGX_FClose(request->err);
		close |= FCGX_FClose(request->out);

		close |= FCGX_GetError(request->in);
	}

	FCGX_Free(request, close);
}

void FCGX_Free(FCGX_Request * request, int close)
{
	if (request == NULL)
		return;

	FCGX_FreeStream(&request->in);
	FCGX_FreeStream(&request->out);
	FCGX_FreeStream(&request->err);
	FreeParams(&request->paramsPtr);

	if (close) {
		OS_Close(request->fd, ! request->detached);
		request->fd = -1;
		request->detached = 0;
	}
}

void FCGX_Init(void)
{

}

int FCGX_OpenSocket(const char *ip, int port)
{
	int listenSock = socket(AF_INET, SOCK_STREAM, 0);
	if(listenSock >= 0) {
		int flag = 1;
		if(setsockopt(listenSock, SOL_SOCKET, SO_REUSEADDR,
					(char *) &flag, sizeof(flag)) < 0) {
			// fprintf(stderr, "Can't set SO_REUSEADDR.\n");
			exit(1001);
		}
	}

	if(listenSock < 0) {
		return -1;
	}

	struct  sockaddr_in	sa;
	memset((char *) &sa, 0, sizeof(sa));
	sa.sin_family = AF_INET;
	sa.sin_addr.s_addr = inet_addr(ip);
	sa.sin_port = htons(port);

	if(bind(listenSock, (struct sockaddr *) &sa, sizeof(sa)) < 0
			|| listen(listenSock, 4096) < 0) {
		perror("bind/listen");
		exit(errno);
	}

	return listenSock;
}

int FCGX_InitRequest(FCGX_Request *request, int sock, int flags)
{
	memset(request, 0, sizeof(FCGX_Request));

	/* @@@ Should check that sock is open and listening */
	request->listen_sock = sock;

	/* @@@ Should validate against "known" flags */
	request->flags = flags;

	request->fd = -1;

	return 0;
}

int FCGX_Accept_r(FCGX_Request *request)
{
	/* Finish the current request, if any. */
	FCGX_Finish_r(request);

	for (;;) {
		/*
		 * If a connection isn't open, accept a new connection (blocking).
		 * If an OS error occurs in accepting the connection,
		 * return -1 to the caller, who should exit.
		 */
		if (request->fd < 0) {
			int fail_on_intr = request->flags & FCGI_FAIL_ACCEPT_ON_INTR;

			request->fd = OS_Accept(request->listen_sock, fail_on_intr);
			if (request->fd < 0) {
				return (errno > 0) ? (0 - errno) : -9999;
			}
		}
		/*
		 * A connection is open.  Read from the connection in order to
		 * get the request's role and environment.  If protocol or other
		 * errors occur, close the connection and try again.
		 */
		request->isBeginProcessed = FALSE;
		request->in = NewReader(request, 8192, 0);
		FillBuffProc(request->in);
		if(!request->isBeginProcessed) {
			goto TryAgain;
		}
		{
			char *roleStr;
			switch(request->role) {
				case FCGI_RESPONDER:
					roleStr = "FCGI_ROLE=RESPONDER";
					break;
				case FCGI_AUTHORIZER:
					roleStr = "FCGI_ROLE=AUTHORIZER";
					break;
				case FCGI_FILTER:
					roleStr = "FCGI_ROLE=FILTER";
					break;
				default:
					goto TryAgain;
			}
			request->paramsPtr = NewParams(30);
			PutParam(request->paramsPtr, StringCopy(roleStr));
		}
		SetReaderType(request->in, FCGI_PARAMS);
		if(ReadParams(request->paramsPtr, request->in) >= 0) {
			/*
			 * Finished reading the environment.  No errors occurred, so
			 * leave the connection-retry loop.
			 */
			break;
		}

		/*
		 * Close the connection and try again.
		 */
TryAgain:
		FCGX_Free(request, 1);

	} /* for (;;) */
	/*
	 * Build the remaining data structures representing the new
	 * request and return successfully to the caller.
	 */
	SetReaderType(request->in, FCGI_STDIN);
	request->out = NewWriter(request, 8192, FCGI_STDOUT);
	request->err = NewWriter(request, 512, FCGI_STDERR);
	request->nWriters = 2;
	request->envp = request->paramsPtr->vec;
	return 0;
}

int OS_Close(int fd, int shutdown_ok)
{
	if (fd == -1)
		return 0;

	// fprintf(stdout, "close=%d\n", fd);

	/*
	 * shutdown() the send side and then read() from client until EOF
	 * or a timeout expires.  This is done to minimize the potential
	 * that a TCP RST will be sent by our TCP stack in response to
	 * receipt of additional data from the client.  The RST would
	 * cause the client to discard potentially useful response data.
	 */

	if (shutdown_ok) {

		if (shutdown(fd, 1) == 0) {

			struct timeval tv;
			fd_set rfds;
			int rv;
			char trash[1024];

			FD_ZERO(&rfds);

			do {

				FD_SET(fd, &rfds);
				tv.tv_sec = 2;
				tv.tv_usec = 0;
				rv = select(fd + 1, &rfds, NULL, NULL, &tv);
			}
			while (rv > 0 && read(fd, trash, sizeof(trash)) > 0);
		}
	}

	return close(fd);
}

static int is_reasonable_accept_errno (const int error)
{
	switch (error) {
		case EPROTO:
		case ECONNABORTED:
		case ECONNRESET:
		case ETIMEDOUT:
		case EHOSTUNREACH:
		case ENETUNREACH:
			return 1;
		default:
			return 0;
	}
}

static int is_af_unix_keeper(const int fd)
{
	fd_set read_fds;
	FD_ZERO(&read_fds);
	FD_SET(fd, &read_fds);

	struct timeval tval = {2, 0};
	return select(fd + 1, &read_fds, NULL, NULL, &tval) >= 0 && FD_ISSET(fd, &read_fds);
}

int OS_Accept(int listen_sock, int fail_on_intr)
{
	int socket = -1;
	struct sockaddr_in sa;

	for (;;) {
		for (;;) {
			do {
				socklen_t len = sizeof(sa);
				socket = accept(listen_sock, (struct sockaddr *)&sa, &len);
				// fprintf(stdout, "socket=%d\n", socket);

			} while (socket < 0
					&& errno == EINTR
					&& ! fail_on_intr );

			if (socket < 0) {
				if (! is_reasonable_accept_errno(errno)) {
					return (-1);
				}
				errno = 0;

			} else {  /* socket >= 0 */

				int set = 1;
				setsockopt(socket, IPPROTO_TCP, TCP_NODELAY, (char *)&set, sizeof(set));
				break;

			}  /* socket >= 0 */
		}  /* for(;;) */

		if (is_af_unix_keeper(socket))
			break;

		close(socket);
	}  /* while(1) - lock */

	return (socket);
}


