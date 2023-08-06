
#ifndef __ADX_TIME_H__
#define __ADX_TIME_H__

#include <webserver_type.h>
#include <webserver_alloc.h>
#include <webserver_string.h>

#define TIME_DAY_SEC 86400

#define GET_TIME_YEAR            get_time_year(time(NULL)) // 获取年
#define GET_TIME_MONTH           get_time_month(time(NULL)) // 获取月 取值区间为[0,11]
#define GET_TIME_WEEK            get_time_week(time(NULL)) // 获取周 取值区间为[0,6]
#define GET_TIME_WEEK_NATURAL    get_time_week_natural(time(NULL)) // 获取自然周 取值区间为[0,52]
#define GET_TIME_DAY             get_time_day(time(NULL)) // 获取日 取值区间为[1,31]
#define GET_TIME_HOUR            get_time_hour(time(NULL)) // 获取小时 取值区间为[0,23]
#define GET_TIME_30MIN           get_time_30min(time(NULL)) // 获取当前30分钟 取值区间为[0,47]
#define GET_TIME_10MIN           get_time_10min(time(NULL)) // 获取当前10分钟 取值区间为[0,5]
#define GET_TIME_MIN             get_time_min(time(NULL))// 获取分钟 取值区间为[0,59]

#define TIME_MONTH_END           get_time_end_sec_month(time(NULL))
#define TIME_WEEK_END            get_time_end_sec_week(time(NULL))
#define TIME_TODAY_END           get_time_end_sec_today(time(NULL))
#define TIME_HOUR_END            get_time_end_sec_hour(time(NULL))
#define TIME_30MIN_END           get_time_end_sec_30min(time(NULL))
#define TIME_10MIN_END           get_time_end_sec_10min(time(NULL))


time_t time_format(char *format, char *str);
time_t time_format_str(char *str);

/***************/
/*   获取时间   */
/***************/
int get_time_year(time_t t); // 获取年
int get_time_month(time_t t); // 获取月 取值区间为[0,11]
int get_time_week(time_t t); // 获取周 取值区间为[0,6]
int get_time_week_natural(time_t t); // 获取自然周 取值区间为[0,52]
int get_time_day(time_t t); // 获取日 取值区间为[1,31]
int get_time_hour(time_t t); // 获取小时 取值区间为[0,23]
int get_time_30min(time_t t); // 获取当前30分钟 取值区间为[0,47]
int get_time_10min(time_t t); // 获取当前10分钟 取值区间为[0,5]
int get_time_min(time_t t); // 获取分钟 取值区间为[0,59]

/***************/
/*   剩余秒数   */
/***************/
int get_time_end_sec_month(time_t t); // 剩余秒数 到达本月结束
int get_time_end_sec_week(time_t t); // 剩余秒数 到达本周结束
int get_time_end_sec_today(time_t t); // 剩余秒数 到达本日结束
int get_time_end_sec_hour(time_t t); // 剩余秒数 到达本小时结束
int get_time_end_sec_30min(time_t t); // 剩余秒数 到达30分钟结束
int get_time_end_sec_10min(time_t t); // 剩余秒数 到达10分钟结束

/// 毫秒
int milli_second(void);
/// 微秒
size_t micro_second(void);


#endif


