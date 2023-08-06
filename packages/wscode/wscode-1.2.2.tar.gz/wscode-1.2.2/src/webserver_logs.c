
#include <webserver_logs.h>

static char *path = "web_server.log";
static webserver_log_t *log_object = NULL;
int webserver_log_init(void)
{
	webserver_pool_t *pool = webserver_malloc_pool();
	if (!pool) return -1;

	log_object = webserver_alloc(pool, sizeof(webserver_log_t));
	if (!log_object) return -1;

	FILE *fp = fopen(path, "a+");
	if (!fp) return -1;

	log_object->fp = fp;
	log_object->path = path;
	log_object->pool = pool;
	pthread_mutexattr_init(&log_object->mattr);
	pthread_mutexattr_setpshared(&log_object->mattr, PTHREAD_PROCESS_SHARED);
	pthread_mutex_init(&log_object->mutex, &log_object->mattr);
	return 0;
}

void webserver_log_free(void)
{
	if (log_object)
		webserver_pool_free(log_object->pool);
}

void webserver_log(const char *format, ...)
{

	va_list ap;
	va_start(ap, format);

	struct tm tm;
	time_t system_time = time(NULL);
	localtime_r(&system_time, &tm);

	pthread_mutex_lock(&log_object->mutex); // lock

	fprintf(log_object->fp, "[%04d-%02d-%02d %02d:%02d:%02d]",
			tm.tm_year + 1900,
			tm.tm_mon + 1,
			tm.tm_mday,
			tm.tm_hour,
			tm.tm_min,
			tm.tm_sec);
	vfprintf(log_object->fp, format, ap);
	fwrite("\n", 1, 1, log_object->fp);
	fflush(log_object->fp);

	pthread_mutex_unlock(&log_object->mutex); // unlock
}

void webserver_log_from_buffer(const char *buffer, int len)
{
	struct tm tm;
	time_t system_time = time(NULL);
	localtime_r(&system_time, &tm);

	// fprintf(stdout, "%.*s\n", len, buffer);
	pthread_mutex_lock(&log_object->mutex); // lock

	fprintf(log_object->fp, "[%04d-%02d-%02d %02d:%02d:%02d]",
			tm.tm_year + 1900,
			tm.tm_mon + 1,
			tm.tm_mday,
			tm.tm_hour,
			tm.tm_min,
			tm.tm_sec);
	fwrite(buffer, 1, len, log_object->fp);
	fwrite("\n", 1, 1, log_object->fp);
	fflush(log_object->fp);

	pthread_mutex_unlock(&log_object->mutex); // unlock
}

PyObject *__webserver_log(PyObject *self, PyObject *args)
{
	int size = 0;
	char *msg = NULL;
	if (!PyArg_ParseTuple(args, "s#", &msg, &size)) {
		Py_RETURN_NONE;
	}

	if (!msg || !size) {
		Py_RETURN_NONE;
	}

	webserver_log_from_buffer(msg, size);
	Py_RETURN_NONE;
}

