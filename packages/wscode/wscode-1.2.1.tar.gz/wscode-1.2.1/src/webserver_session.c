
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <webserver_uuid.h>
#include <webserver_session.h>

static int session_mode = SESSION_MODE_FILE;
static int session_timeout = 60 * 60 * 3;
static char *session_path = "/tmp";

#if 0
void session_check_timeout_file(char *path)
{
	FILE *fp = fopen(path, "r");
	if (!fp) return;

	char timeout[11];
	size_t size = fread(timeout, 1, 10, fp);
	timeout[size] = 0;
	fclose(fp);

	if (size != 10)
		return;

	time_t sys_time = time(NULL);
	time_t file_time = atoi(timeout);
	if (sys_time - file_time >= session_timeout)
		remove(path);
}

void session_check_file(char *path, char *name)
{
	// S_ISLNK(st_mode)是否是一个连接
	// S_ISREG(st_mode)是否是一个常规文件
	// S_ISDIR(st_mode)是否是一个目录
	// S_ISCHR(st_mode)是否是一个字符设备
	// S_ISBLK(st_mode)是否是一个块设备
	// S_ISFIFO(st_mode)是否 是一个FIFO文件
	// S_ISSOCK(st_mode)是否是一个SOCKET文件
	struct stat sb;
	if (stat(path, &sb)) return;
	if (!S_ISREG(sb.st_mode)) return;
	if (strncmp(name, "sess_", 5)) return;
	session_check_timeout_file(path);
}

int session_check_dir(void)
{
	char path[PATH_MAX];
	DIR *dir = opendir(session_path);
	if (!dir) return -1;

	for (;;) {
		struct dirent *file = readdir(dir);
		if (!file) break;

		if(strncmp(file->d_name, ".", 1) == 0)
			continue;

		sprintf(path, "%s/%s", session_path, file->d_name);
		session_check_file(path, file->d_name);
	}

	closedir(dir);
	return 0;
}
#endif


PyObject *session_create_file(PyObject *self, PyObject *args)
{
	char *buf = NULL;
	int len = 0;
	if (!PyArg_ParseTuple(args, "s#", &buf, &len))
		Py_RETURN_FALSE;

	if (len <= 0) Py_RETURN_FALSE;

	char sec[11];
	sprintf(sec, "%zd", time(NULL));

	char path[PATH_MAX];
	char session_id[40] = {0};
	sprintf(path, "%s/sess_%s", session_path, webserver_uuid(session_id));

	FILE *fp = fopen(path, "wb");
	if (!fp) Py_RETURN_FALSE;

	fwrite(sec, 10, 1, fp);
	fwrite(buf, len, 1, fp);
	fclose(fp);

	return Py_BuildValue("s", session_id);
}

PyObject *session_destroy_file(PyObject *self, PyObject *args)
{
	int len = 0;
	char *key = NULL;
	if (!PyArg_ParseTuple(args, "s#", &key, &len))
		Py_RETURN_FALSE;

	if (len <= 0) Py_RETURN_FALSE;

	char path[PATH_MAX];
	sprintf(path, "%s/sess_%s", session_path, key);

	remove(path);
	Py_RETURN_TRUE;
}

PyObject *session_find_file(PyObject *self, PyObject *args)
{
	int len = 0;
	char *key = NULL;
	if (!PyArg_ParseTuple(args, "s#", &key, &len))
		Py_RETURN_NONE;

	if (len <= 0) Py_RETURN_NONE;

	char path[PATH_MAX];
	sprintf(path, "%s/sess_%s", session_path, key);
	if(access(path, F_OK) != 0)
		Py_RETURN_NONE;

	FILE *fp = fopen(path, "r+");
	if (!fp) Py_RETURN_NONE;

	char buf[SESSION_SIZE];
	size_t size = fread(buf, 1, 10, fp);
	if (size != 10) {
		fclose(fp);
		Py_RETURN_NONE;
	}

	buf[size] = 0;
	time_t sys_time = time(NULL);
	time_t file_time = atoi(buf);
	if (sys_time - file_time >= session_timeout) {
		fclose(fp);
		remove(path);
		Py_RETURN_NONE;
	}

	fseek(fp, 0, SEEK_SET);
	sprintf(buf, "%zd", time(NULL));
	fwrite(buf, 1, 10, fp);

	fseek(fp, 10, SEEK_SET);
	size = fread(buf, 1, SESSION_SIZE, fp);
	fclose(fp);

	return Py_BuildValue("s#", buf, size);
}

/*******************************************/
/****** API ******/
/*******************************************/
int session_init()
{
	return 0;
}

PyObject *session_create(PyObject *self, PyObject *args)
{
	switch (session_mode) {
		case SESSION_MODE_FILE:
			return session_create_file(self, args);
	}

	Py_RETURN_NONE;
}

PyObject *session_destroy(PyObject *self, PyObject *args)
{
	switch (session_mode) {
		case SESSION_MODE_FILE:
			return session_destroy_file(self, args);
	}

	Py_RETURN_NONE;
}

PyObject *session_find(PyObject *self, PyObject *args)
{
	switch (session_mode) {
		case SESSION_MODE_FILE:
			return session_find_file(self, args);
	}

	Py_RETURN_NONE;
}

