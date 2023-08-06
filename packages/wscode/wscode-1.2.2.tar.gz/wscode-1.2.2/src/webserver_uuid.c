
#include <webserver_uuid.h>

typedef struct {
	unsigned int	time_low;
	unsigned short	time_mid;
	unsigned short	time_hi_and_version;
	unsigned short	clock_seq;
	unsigned char	node[6];
} webserver_uuid_t;

int webserver_uuid_get_fd()
{
	int i, fd = -1;
	struct timeval	tv;
	gettimeofday(&tv, 0);

	fd = open("/dev/urandom", O_RDONLY);
	if (fd == -1)
		fd = open("/dev/random", O_RDONLY | O_NONBLOCK);

	if (fd >= 0) {
		i = fcntl(fd, F_GETFD);
		if (i >= 0)
			fcntl(fd, F_SETFD, i | FD_CLOEXEC);
	}

	srand((getpid() << 16) ^ getuid() ^ tv.tv_sec ^ tv.tv_usec);
	return fd;
}

void webserver_uuid_get_bytes(void *buf, size_t nbytes)
{
	size_t n = nbytes;
	int fd = webserver_uuid_get_fd();
	int lose_counter = 0;
	unsigned char *cp = (unsigned char *) buf;

	if (fd >= 0) {
		while (n > 0) {
			ssize_t x = read(fd, cp, n);
			if (x <= 0) {
				if (lose_counter++ > 16)
					break;
				continue;
			}
			n -= x;
			cp += x;
			lose_counter = 0;
		}

		close(fd);
	}
}

void webserver_uuid_unpack(unsigned char * in, webserver_uuid_t *uu)
{
	unsigned char	*ptr = in;
	unsigned int	tmp;

	tmp = *ptr++;
	tmp = (tmp << 8) | *ptr++;
	tmp = (tmp << 8) | *ptr++;
	tmp = (tmp << 8) | *ptr++;
	uu->time_low = tmp;

	tmp = *ptr++;
	tmp = (tmp << 8) | *ptr++;
	uu->time_mid = tmp;

	tmp = *ptr++;
	tmp = (tmp << 8) | *ptr++;
	uu->time_hi_and_version = tmp;

	tmp = *ptr++;
	tmp = (tmp << 8) | *ptr++;
	uu->clock_seq = tmp;

	memcpy(uu->node, ptr, 6);
}

void webserver_uuid_pack( webserver_uuid_t *uu, unsigned char * ptr)
{
	unsigned int	tmp;
	unsigned char	*out = ptr;

	tmp = uu->time_low;
	out[3] = (unsigned char) tmp;
	tmp >>= 8;
	out[2] = (unsigned char) tmp;
	tmp >>= 8;
	out[1] = (unsigned char) tmp;
	tmp >>= 8;
	out[0] = (unsigned char) tmp;

	tmp = uu->time_mid;
	out[5] = (unsigned char) tmp;
	tmp >>= 8;
	out[4] = (unsigned char) tmp;

	tmp = uu->time_hi_and_version;
	out[7] = (unsigned char) tmp;
	tmp >>= 8;
	out[6] = (unsigned char) tmp;

	tmp = uu->clock_seq;
	out[9] = (unsigned char) tmp;
	tmp >>= 8;
	out[8] = (unsigned char) tmp;

	memcpy(out+10, uu->node, 6);
}

void webserver_uuid_generate(unsigned char *out)
{
	unsigned char buf[128] = {0};
	webserver_uuid_t uu;
	webserver_uuid_get_bytes(buf, sizeof(buf));
	webserver_uuid_unpack(buf, &uu);

	uu.clock_seq = (uu.clock_seq & 0x3FFF) | 0x8000;
	uu.time_hi_and_version = (uu.time_hi_and_version & 0x0FFF)
		| 0x4000;
	webserver_uuid_pack(&uu, out);
}

void webserver_uuid_unparse(unsigned char * uu, char *out)
{
	webserver_uuid_t uuid;
	static char *fmt = "%08x-%04x-%04x-%02x%02x-%02x%02x%02x%02x%02x%02x";
	webserver_uuid_unpack(uu, &uuid);
	sprintf(out, fmt,
			uuid.time_low, uuid.time_mid, uuid.time_hi_and_version,
			uuid.clock_seq >> 8, uuid.clock_seq & 0xFF,
			uuid.node[0], uuid.node[1], uuid.node[2],
			uuid.node[3], uuid.node[4], uuid.node[5]);
}

char *webserver_uuid(char *out)
{
	unsigned char uuid[128];
	webserver_uuid_generate(uuid);
	webserver_uuid_unparse(uuid, out);
	return out;
}

