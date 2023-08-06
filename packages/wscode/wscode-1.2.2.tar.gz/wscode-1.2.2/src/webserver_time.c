
#include <webserver_time.h>

/*
 * tm_year   年: 加上1900
 * tm_mon    月: 取值区间为[0,11]
 * tm_mday   日: 取值区间为[1,31]
 * tm_hour   时: 取值区间为[0,23]
 * tm_min    分: 取值区间为[0,59]
 * tm_sec    秒: 取值区间为[0,59]
 * tm_wday   周: 取值区间为[0,6] 0星期天，1星期一
 * tm_yday   从每年的1月1日开始的天数: 取值区间为[0,365]，其中0代表1月1日
 */

char *strptime(const char *buf,const char *format, struct tm *tm);
time_t time_format(char *format, char *str)
{
	if (!format || !str)
		return 0;

	struct tm tm = {0};
	strptime(str, format, &tm);
	return mktime(&tm);
}

time_t time_format_str(char *str)
{
	char *format = "%Y-%m-%d %H:%M:%S";
	return time_format(format, str);
}

char *get_time_str(int type, const char *split, char *buf)
{
	struct tm tm;
	time_t t = time(NULL);
	localtime_r(&t, &tm);

	int size = 0;
	if (type & 1) { // 年
		size += sprintf(&buf[size], "%04d", tm.tm_year + 1900);
	}

	if (type & 2) { // 月
		if (split && size) size += sprintf(&buf[size], "%s", split);
		size += sprintf(&buf[size], "%02d", tm.tm_mon + 1);
	}

	if (type & 4) { // 日
		if (split && size) size += sprintf(&buf[size], "%s", split);
		size += sprintf(&buf[size], "%02d", tm.tm_mday);
	}

	if (type & 8) { // 时
		if (split && size) size += sprintf(&buf[size], "%s", split);
		size += sprintf(&buf[size], "%02d", tm.tm_hour);
	}

	if (type & 16) { // 分
		if (split && size) size += sprintf(&buf[size], "%s", split);
		size += sprintf(&buf[size], "%02d", tm.tm_min);
	}

	if (type & 32) { // 秒
		if (split && size) size += sprintf(&buf[size], "%s", split);
		size += sprintf(&buf[size], "%02d", tm.tm_sec);
	}

	return buf;
}


void time_display(time_t t)
{
	struct tm *tm = localtime(&t);
	fprintf(stdout, "[%04d-%02d-%02d][%02d:%02d:%02d][%d]\n",
			tm->tm_year + 1900,
			tm->tm_mon + 1,
			tm->tm_mday,
			tm->tm_hour,
			tm->tm_min,
			tm->tm_sec,
			tm->tm_wday);
}

/***************/
/*   获取时间   */
/***************/

// 获取年
int get_time_year(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return (tm.tm_year + 1900);
}

// 获取月 取值区间为[0,11]
int get_time_month(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return tm.tm_mon;
}

// 获取周 取值区间为[0,6]
int get_time_week(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return tm.tm_wday;
}

// 获取自然周 取值区间为[0,52]
int get_time_week_natural(time_t t)
{
	char buf[128];
	struct tm tm = {0};
	localtime_r(&t, &tm);
	strftime(buf, 128, "%W", &tm); // 取值区间为[0,52]
	return atoi(buf);
}

// 获取日 取值区间为[1,31]
int get_time_day(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return tm.tm_mday;
}

// 获取小时 取值区间为[0,23]
int get_time_hour(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return tm.tm_hour;
}

// 获取当前30分钟 取值区间为[0,47]
int get_time_30min(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return (tm.tm_hour * 2 + (tm.tm_min < 30 ? 0 : 1));
}

// 获取当前10分钟 取值区间为[0,5]
int get_time_10min(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return (tm.tm_min / 10);
}

// 获取分钟 取值区间为[0,59]
int get_time_min(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);
	return tm.tm_min;
}

/***************/
/*   剩余秒数   */
/***************/
// 剩余秒数 到达本月结束
int get_time_end_sec_month(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);

	tm.tm_mon++;
	tm.tm_mday = 1;
	tm.tm_hour = 23;
	tm.tm_min = 59;
	tm.tm_sec = 59;

	int end_sec = mktime(&tm) - TIME_DAY_SEC;
	return (end_sec - t);
}

// 剩余秒数 到达本周结束
int get_time_end_sec_week(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);

	tm.tm_mday += (7 - tm.tm_wday);
	tm.tm_hour = 23;
	tm.tm_min = 59;
	tm.tm_sec = 59;

	int end_sec = mktime(&tm);
	return (end_sec - t);
}

// 剩余秒数 到达本日结束
int get_time_end_sec_today(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);

	tm.tm_hour = 23;
	tm.tm_min = 59;
	tm.tm_sec = 59;

	int end_sec = mktime(&tm);
	return (end_sec - t);
}

// 剩余秒数 到达本小时结束
int get_time_end_sec_hour(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);

	tm.tm_min = 59;
	tm.tm_sec = 59;

	int end_sec = mktime(&tm);
	return (end_sec - t);

	return ((60 - tm.tm_min) * 60) - tm.tm_sec;
}

// 剩余秒数 到达30分钟结束
int get_time_end_sec_30min(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);

	if (tm.tm_min >= 30) tm.tm_min = 59;
	else tm.tm_min = 29;

	tm.tm_sec = 59;
	int end_sec = mktime(&tm);
	return (end_sec - t);
}

// 剩余秒数 到达10分钟结束
int get_time_end_sec_10min(time_t t)
{
	struct tm tm = {0};
	localtime_r(&t, &tm);

	int min = tm.tm_min / 10;
	switch (min) {
		case 0 : tm.tm_min = 9;
			 break;
		case 1 : tm.tm_min = 19;
			 break;
		case 2 : tm.tm_min = 29;
			 break;
		case 3 : tm.tm_min = 39;
			 break;
		case 4 : tm.tm_min = 49;
			 break;
		case 5 : tm.tm_min = 59;
			 break;
	}

	tm.tm_sec = 59;
	int end_sec = mktime(&tm);
	return (end_sec - t);

	// int min = tm.tm_min % 10; // 取个位数
	// return (600 - (min * 60 + tm.tm_sec));
}


/// 毫秒
int milli_second(void)
{
	struct timeval tv;
	gettimeofday(&tv,NULL);
	return tv.tv_sec * 1000 + tv.tv_usec / 1000;  //毫秒
}

/// 微秒
size_t micro_second(void)
{
	struct timeval tv;
	gettimeofday(&tv,NULL);
	return tv.tv_sec * 1000000 + tv.tv_usec;  //微秒
}


