import json
import datetime
import urllib
import urllib.request


# SQL -> JSON
# EXPLAIN PLAN FOR

headers = {"Content-Type": "application/json"}

class druid_error:
    def __init__(self):
        self.mess = ""

    def assembly(self, name, e=None):
        self.mess = "druid error %s : [%s]" % (name, e)
        core.logs.error(self.mess)

class druid_api:
    def __init__(self, url, table):
        self.url = url
        self.table = table

    def datasource_parse(self, o):
        if o: return o
        return self.table

    def one_more_day(self, s):
        try:
            t = datetime.datetime.strptime(s, "%Y-%m-%d")
            t = t + datetime.timedelta(days=1)
            return t.strftime("%Y-%m-%d")
        except:
            return None

    def today(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return ["%s/%s" % (today, tomorrow)]

    def intervals_parse(self, o):
        if type(o) == str:
            return o

        elif type(o) == list:
            return o

        elif type(o) == dict:
            start_time = o.get("start")
            end_time = self.one_more_day(o.get("end"))
            if start_time and end_time:
                return ["%s/%s" % (start_time, end_time)]

        return None

    def filter_parse(self, o):
        if type(o) == str:
            return o

        if type(o) == list:
            return o

        if type(o) == dict:
            return self.filter_dict_parse(o)

    def filter_dict_parse(self, o):
        fields = []
        for key in o:
            val = o.get(key)
            if type(val) == list:
                fields.append({
                    "type": "in",
                    "dimension": key,
                    "values": o.get(key)
                })
            else:
                fields.append({
                    "type": "selector",
                    "dimension": key,
                    "value": o.get(key)
                })

        if fields:
            return {
                "type": "and",
                "fields": fields
            }

        return None

    def limit_sort_parse(self, columns):
        key = columns.get("key")
        order = columns.get("order")
        if not key or not order:
            return []

        if order == "asc":
            direction = "ascending"
        elif order == "desc":
            direction = "descending"
        else:
            return []

        return [{
            "dimension": key,
            "direction": direction,
            "dimensionOrder": {
                "type": "numeric"
            }
        }]

    def limit_spec_parse(self, o):

        page_index = o.get("page_index")
        page_count = o.get("page_count")
        sort = o.get("sort")

        try: page_index = page_index - 1
        except Exception as e:
            return {}

        if sort:
            columns = self.limit_sort_parse(sort)
            if columns:
                return {
                    "type": "default",
                    "columns": columns,
                    "limit": page_count,
                    "offset": page_index * page_count
                }

        return {
            "type": "default",
            "limit": page_count,
            "offset": page_index * page_count
        }

    def group(self,
              datasource=None,
              granularity="all",
              intervals=None,
              dimensions=[],
              aggregations=[],
              post_aggregations=[],
              filter=None,
              limit_spec={},
              count=True):

        query = {
            "queryType": "groupBy",
            "dataSource": self.datasource_parse(datasource),
            "granularity": granularity,
            "intervals": self.intervals_parse(intervals),
            "dimensions": dimensions,
            "aggregations": aggregations,
            "postAggregations": post_aggregations,
            "filter": self.filter_parse(filter),
            "limitSpec": self.limit_spec_parse(limit_spec)
        }

        # print("query", json.dumps(query, ensure_ascii=False))
        res = self.post(query)
        if not res:
            if count : return [], 0
            else: return []

        if count:
            __count = self.count(query)
            if not __count:
                return [], 0
            return self.group_format(res), __count

        return self.group_format(res)

    def count(self, __query):

        query = {
            "queryType": __query.get("queryType"),
            "dataSource": __query.get("dataSource"),
            "granularity": __query.get("granularity"),
            "intervals": __query.get("intervals"),
            "dimensions": __query.get("dimensions"),
            "filter": __query.get("filter"),
        }

        count = {
            "queryType": "timeseries",
            "dataSource": {
                "type": "query",
                "query": query
            },
            "granularity": "all",
            "intervals": ["0000/3000"],
            "aggregations": [{
                "type": "count",
                "name": "count"
                }
            ]
        }

        res = self.post(count)
        if not res:
            return 0
        try:
            return res[0].get("result").get("count")
        except Exception as e:
            return 0

    def post(self, query):

        try:
            querystr = json.dumps(query, ensure_ascii=False)
            req = urllib.request.Request(self.url, headers=headers, data=bytes(querystr, "utf8"))
            res = urllib.request.urlopen(req)
            data = res.read()
            data = json.loads(data)
            res.close()
            return data

        except Exception as e:
            return None

    def group_format(self, data):
        try:
            return [x.get('event') for x in data]
        except Exception as e:
            return []

