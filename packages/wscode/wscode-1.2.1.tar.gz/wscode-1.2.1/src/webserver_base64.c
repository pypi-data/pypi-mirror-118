
#include <webserver_base64.h>

static const char base[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="; 
char *base64_encode(const char *src, char *dest)
{ 
	int i = 0;
	int tmp = 0;
	int temp = 0;
	int prepare = 0; 
	char changed[4]; 
	int src_len = strlen(src); 

	while (tmp < src_len) {

		temp = 0; 
		prepare = 0; 
		memset(changed, '\0', 4); 
		while (temp < 3) {
			if (tmp >= src_len) break;
			prepare = ((prepare << 8) | (src[tmp] & 0xFF)); 
			tmp++;
			temp++; 
		}

		prepare = (prepare<<((3-temp)*8)); 
		for (i = 0; i < 4 ;i++ ) {

			if (temp < i) 
				changed[i] = 0x40; 
			else 
				changed[i] = (prepare>>((3-i)*6)) & 0x3F; 

			int ch = changed[i];
			*dest++ = base[ch];
		} 
	} 

	*dest = '\0'; 
	return dest;
} 

/* 转换算子 */ 
static char base64_find_pos(char ch)
{ 
	char *ptr = (char*)strrchr(base, ch);//the last position (the only) in base[] 
	return (ptr - base); 
} 

/* Base64 解码 */ 
char *base64_decode(const char *src, char *dest)
{ 
	int i = 0; 
	int tmp = 0; 
	int temp = 0;
	int prepare = 0; 
	int equal_count = 0; 
	int src_len = strlen(src);

	if (*(src + src_len - 1) == '=') 
		equal_count += 1; 

	if (*(src + src_len - 2) == '=') 
		equal_count += 1; 

	if (*(src + src_len - 3) == '=') 
		equal_count += 1; 

	while (tmp < (src_len - equal_count)) {

		temp = 0; 
		prepare = 0; 
		while (temp < 4) {
			if (tmp >= (src_len - equal_count)) break; 
			prepare = (prepare << 6) | (base64_find_pos(src[tmp]));
			temp++;
			tmp++;
		}

		prepare = prepare << ((4-temp) * 6); 
		for (i = 0; i < 3; i++) {

			if (i == temp) break;
			*dest++ = (char)((prepare>>((2-i)*8)) & 0xFF);
		} 
	} 

	*dest = '\0'; 
	return dest; 
}


