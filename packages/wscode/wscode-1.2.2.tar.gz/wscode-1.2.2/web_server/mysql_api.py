# -*- coding: utf-8 -*-

import pymysql
import datetime


class mysql_error:
    def __init__(self):
        self.code = 0
        self.mess = ""

    def assembly(self, name, code=None, e=None):

        if e:
            self.code = code if code else -1
            self.mess = "mysql error %s : %s" % (name, e)
        else:
            self.code = code
            self.mess = "mysql error %s : [%s]" % (name, code)


class mysql_bash:
    def __init__(self, host, user, passwd, db):
        self.error = mysql_error()
        self.conn = self.conn(host, user, passwd, db)

    def conn(self, host, user, passwd, db):
        try:
            return pymysql.connect(
                host=host,
                user=user,
                passwd=passwd,
                db=db,
                charset="utf8")
        except Exception as e:
            self.error.assembly("conn", e.args[0])

    def select_value_parse(self, value):
        if type(value) == bytes:
            value = str(value)
        elif type(value) == datetime.datetime:
            value = value.strftime("%Y-%m-%d %H:%M:%S")

        return value

    def select(self, cur, sql, args=None, not_field_name=False):
        if not self.execute(cur, sql, args):
            return []

        r = []
        if not_field_name:
            for row in cur.fetchall():
                for value in row:
                    value = self.select_value_parse(value)
                    r.append(value)
        else:
            field_names = self.select_field_parse(cur)
            for row in cur.fetchall():
                node = {}
                for field, value in zip(field_names, row):
                    value = self.select_value_parse(value)
                    node[field] = value
                r.append(node)

        return r

    def select_field_parse(self, cur):
        names = []
        for name in cur.description:
            self.select_field_repeat(names, name[0])
        return names

    def select_field_repeat(self, names, key):
        index = 0
        __key = key
        while True:
            try:
                names.index(__key)
                index = index + 1
                __key = key + ("(%s)" % index)
            except:
                names.append(__key)
                return

    def execute(self, cur, sql, args):
        try:
            if not args:
                cur.execute(sql)
            else:
                cur.executemany(sql, [args])

        except Exception as e:
            if type(self.error.code) is not int:
                self.error.assembly("execute", 1010)
            else:
                self.error.assembly("execute", e.args[0], e)
            return False

        return True

    def cursor(self):
        try:
            return self.conn.cursor()
        except Exception as e:
            self.error.assembly("cursor", e.args[0])
            return None

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            self.error.assembly("commit", e.args[0])

    def rollback(self):
        try:
            self.conn.rollback()
        except Exception as e:
            self.error.assembly("rollback", e.args[0])

    def ping(self):
        try:
            return self.conn.ping()
        except Exception as e:
            self.error.assembly("ping", e.args[0])
            return False

    """
    def close(self):
        try:
            if self.conn.open:
                self.conn.close()
        except Exception as e:
            self.error.assembly("close", e.args[0])
    """


__WHERE_CODE__ = {
    "[=]": "=",
    "[>]": ">",
    "[>=]": ">=",
    "[<]": "<",
    "[<=]": "<=",
    "[<>]": "<>",
    "[!=]": "!=",
    "[~]": "LIKE",
    "[@]": "FUN",
}


class mysql_api(mysql_bash):
    def __init__(self, host, user, passwd, db):
        super().__init__(host, user, passwd, db)

    def get(self, table, columns=None, where=None, group=None, not_field_name=False):

        """
        :param table:      表名
        :param columns:    参考 columns_parse
        :param where:      参考 where_parse
        :param group:      参考 group_parse
        """

        r = self.get_list(table, columns, None, where, group, None, False, not_field_name)
        if not r:
            return {}
        return r[0]

    def get_list(self, table, columns=None, limit=None, where=None, group=None,
                 order=None, found_rows=False, not_field_name=False):

        """
        :param table:      表名
        :param columns:    参考 columns_parse
        :param limit:      参考 limit_parse
        :param where:      参考 where_parse
        :param group:      参考 group_parse
        :param order:      参考 order_parse
        :param found_rows: True 获取总条数
        """

        table = self.table_parse(table)
        if not table: return {}, 0

        columns = self.columns_parse(columns)
        where, args = self.where_parse(where)
        group = self.group_parse(group)
        order = self.order_parse(order)
        limit = self.limit_parse(limit)

        if found_rows:
            sql = "SELECT SQL_CALC_FOUND_ROWS %s %s %s %s %s %s" % (columns, table, where, group, order, limit)
        else:
            sql = "SELECT %s %s %s %s %s %s" % (columns, table, where, group, order, limit)

        cur = self.cursor()
        r = self.select(cur, sql, args, not_field_name)
        if found_rows:
            count = self.get_found_rows(found_rows, cur)
            cur.close()
            return r, count

        cur.close()
        return r

    def get_found_rows(self, found_rows, cur):
        if not found_rows:
            return 0

        self.execute(cur, "SELECT FOUND_ROWS()", None)
        count = cur.fetchall()
        if count: return count[0][0]
        return 0

    def table_parse(self, table):

        """
        :param from:         主表名称
        :param join:         连接的对象
        :param join.table:   连接的表名称
        :param join.type:    连接的类型: left,inner,right (默认 left)
        :param join.on:      连接的条件字段

        : STR
        table="t_media"

        table="t_place
            left join t_channel on t_place.channel_id = t_channel.channel_id
            left join t_media on t_place.media_id = t_media.media_id"

        : OBJ
        table={
            "from": "t_place",
            "join": [
                {
                    "table": "t_channel",
                    "on": "channel_id"
                },
                {
                    "type": "left",
                    "table": "t_media",
                    "on": ["t_place.media_id", "t_media.media_id"]
                }
            ]
        }

        table={
            "from": "t_channel",
            "join": {
                "table": "t_media",
                "on": "media_id"
            }
        }
        """

        if not table:
            return None

        if type(table) == str:
            return "FROM " + table

        if type(table) != dict:
            return None

        from_table = table.get("from")
        if not from_table:
            return None

        join_sql = ""
        join = table.get("join")
        if join:
            join_sql += self.table_join_parse(from_table, join)

        return "FROM " + from_table + join_sql

    def table_join_parse(self, from_table, join):

        if type(join) == dict:
            return self.table_join_obj_parse(from_table, join)

        if type(join) != list:
            return ""

        sql = ""
        for node in join:
            sql += self.table_join_obj_parse(from_table, node)

        return sql

    def table_join_obj_parse(self, from_table, join):

        t = join.get("table")
        on = join.get("on")
        if not t or not on:
            return ""

        join_type = join.get("type")
        if join_type:
            join_type = "%s JOIN" % (join_type)
        else:
            join_type = "LEFT JOIN"

        if type(on) == str:
            key1 = "%s.%s" % (from_table, on)
            key2 = "%s.%s" % (t, on)
            return " %s %s ON %s=%s" % (join_type, t, key1, key2)

        elif type(on) == list:
            return " %s %s ON %s=%s" % (join_type, t, on[0], on[1])

    """
    def table_as_parse(self, table_name):
        if not table_name:
            return "", ""

        # 移除多余空格
        table_name = table_name.strip()
        if " as " in table_name:
            t = table_name.split(" as ")
            return t[0].strip(), t[1].strip()
        return table_name, ""

    def table_join_value_parse(self, join):
        try:
            field1 = list(join.keys())[0]
            field2 = join[field1]
            return field1, field2
        except Exception as e:
            self.error.assembly("table_join_value_parse", e=e)
            return None, None
    """

    def columns_parse(self, columns):

        """
        columns="media_id,name"
        columns=["media_id","name"]
        """

        if type(columns) == str:
            return columns
        if type(columns) == list:
            return ",".join(str(column) for column in columns)
        return "*"

    def where_parse(self, where):

        """
        运算符:          [=], [>], [>=], [<], [<=], [<>], [!=]
        模糊匹配(LIKE):   [~]
        mysql函数:       [@]  例如: is not null/now()

        where={
            "aaa": "AAA",
            "bbb[=]": "BBB",
            "ccc[>]": "CCC",
            "ddd[>=]": "DDD",
            "eee[<]": "EEE",
            "fff[<=]": "FFF",
            "ggg[<>]": "GGG",
            "hhh[!=]": "HHH",
            "iii[~]": "III",
            "jjj[@]": "is not null",
        }
        """

        if type(where) == str:
            return where, None

        if not where or type(where) != dict:
            return "", None

        sql = []
        args = []
        for key in where:
            s = self.where_parse_judge(key, where.get(key), args)
            if s: sql.append(s)

        if not sql:
            return "", None

        r = "WHERE 1=1"
        for s in sql:
            r += " AND " + s
        return r, args

    def where_parse_judge(self, key, val, args):
        if not key or val == None:
            return None

        key, comp = self.where_parse_extract(key)
        if not key or not comp:
            return None

        if comp == "FUN":
            return key + " " + val

        elif comp == "LIKE":
            val = "%" + val + "%"

        args.append(val)
        return key + " " + comp + " %s"

    def where_parse_extract(self, key):

        if not "[" in key:
            return key, "="

        for comp in __WHERE_CODE__:
            if comp in key:
                key = key.replace(comp, "")
                return key, __WHERE_CODE__[comp]
        """
        try:
            import re
            p = re.compile("[\[](.*?)[\]]", re.S)
            comp = str(re.findall(p, key))
            key = key.replace(comp, "")
            comp = comp.replace("[", "").replace("]", "")
            return key, comp

        except Exception as e:
            self.error.assembly("where_parse_judge", e=e)
        """

        return None, None

    def group_parse(self, group):

        """
        group="media_id,name"
        group=["media_id","name"]
        """

        if not group:
            return ""

        if type(group) == str:
            return " GROUP BY " + group

        if type(group) == list:
            return " GROUP BY " + (",".join(str(s) for s in group))

        return ""

    def order_parse(self, order):

        """
        order="region_id desc,region_name"
        order=["region_id desc","region_name"]
        order={
            "region_id": "desc",
            "region_name": None
        }
        """

        if not order:
            return ""

        if type(order) == str:
            return " ORDER BY " + order

        if type(order) == list:
            return " ORDER BY " + (",".join(str(s) for s in order))

        if type(order) != dict:
            return ""

        __list = []
        for s in order:
            value = order.get(s)
            if value and value == "desc":
                __list.append("%s DESC" % (s))
            else:
                __list.append(s)

        return " ORDER BY " + (",".join(str(s) for s in __list))

    def limit_parse(self, limit):

        """
        limit=3
        limit=0,5
        limit={
            "page_index": 1,
            "page_count": 3,
        }
        """

        if not limit:
            return ""

        if type(limit) == int:
            return " LIMIT " + str(limit)

        if type(limit) == str:
            return " LIMIT " + limit

        if type(limit) != dict:
            return ""

        page_index = limit.get("page_index")
        page_count = limit.get("page_count")
        if not page_index or not page_count:
            return ""

        if type(page_index) != int or type(page_count) != int:
            self.error.assembly("limit_parse", e="page_index/page_count not int!")
            return ""

        if page_index:
            page_index = page_index - 1

        return " LIMIT %s,%s" % (page_index * page_count, page_count)

    def add(self, table, items, commit=True, ignore=False):

        """
        :param table:  表名
        :param items:  字段/值
        :param commit: True 自动提交
        :param ignore: True 自动忽略重复插入

        items={
                "aa": 100
                "bb[@]": "now()"
        }
        items=[
            {
                "aa": 100
                "bb[@]": "now()"
            },
            {
                "aa": 101
                "bb[@]": "now()"
            },
            {
                "aa": 102
                "bb[@]": "now()"
            }
        ]
        """

        if not table or not items:
            return False

        if type(items) == dict:
            return self.add_dict(table, items, commit, ignore)

        elif type(items) == list:
            return self.add_list(table, items, commit, ignore)

        return False

    def add_parse(self, table, items, ignore=True):
        args = []
        columns = values = comm = ""
        for key in items:
            val = items.get(key)
            if val is not None:
                if "[@]" in key:
                    columns += comm + key.replace("[@]", "")
                    values += comm + val

                else:
                    columns += comm + key
                    values += comm + "%s"
                    args.append(val)

                comm = ","

        if not columns:
            return None, []

        sql = "INSERT "
        if ignore:
            sql += "IGNORE "
        sql += "INTO %s (%s) VALUES (%s)" % (table, columns, values)
        return sql, args

    def add_dict(self, table, items, commit=True, ignore=True):
        sql, args = self.add_parse(table, items, ignore)
        if not sql:
            return False

        cur = self.cursor()
        if not self.execute(cur, sql, args):
            cur.close()
            return False

        if commit:
            self.commit()

        cur.close()
        return True

    def add_list(self, table, items, commit=True, ignore=True):
        cur = self.cursor()
        for item in items:
            sql, args = self.add_parse(table, item, ignore)
            if not sql:
                cur.close()
                return False

            if not self.execute(cur, sql, args):
                cur.close()
                return False

        if commit:
            self.commit()

        cur.close()
        return True

    def set(self, table, items, where=None, commit=True, auto_insert=False):

        """
        :param table:  表名
        :param items:  字段/值
        :param where:  参考 where_parse
        :param commit: True 自动提交

        items={
            "aa": 100
            "bb[@]": "now()"
        },
        where={
            "id":100
        }
        """

        if not table or not items:
            return False

        if type(items) != dict:
            return False

        sql, args = self.set_parse(table, items, where, auto_insert)
        if not sql:
            return False

        cur = self.cursor()
        if not self.execute(cur, sql, args):
            cur.close()
            return False

        if commit:
            self.commit()

        cur.close()
        return True

    def set_parse(self, table, items, where, auto_insert):
        if auto_insert:
            return self.set_parse_auto_insert(table, items)

        sql, args = self.set_parse_update(table, items)
        if not sql:
            return None, []

        where_sql, where_args = self.where_parse(where)
        return sql + where_sql, args + where_args

    def set_parse_update(self, table, items):
        args = []
        columns = comm = ""
        for key in items:
            val = items.get(key)
            if val != None:
                if "[@]" in key:
                    columns += comm + key.replace("[@]", "")
                    columns += " = " + val

                else:
                    columns += comm + key
                    columns += " = %s"
                    args.append(val)

                comm = ", "

        if not columns:
            return None, []

        sql = "UPDATE %s SET %s " % (table, columns)
        return sql, args

    def set_parse_auto_insert(self, table, items):
        args = []
        keys = values = updates = comm = ""
        for key in items:
            val = items.get(key)
            if val is not None:
                if "[@]" in key:
                    key = key.replace("[@]", "")
                    keys += comm + key
                    values += comm + val
                    updates += comm + "%s=%s" % (key, val)
                else:
                    keys += comm + key
                    values += comm + "%s"
                    updates += comm + key + "=%s"
                    args.append(val)
            comm = ","

        sql = "INSERT INTO %s (%s) VALUES (%s) " % (table, keys, values)
        sql += "ON DUPLICATE KEY UPDATE %s" % updates
        return sql, args + args

    def delete(self, table, where=None, commit=True):

        """
        :param table:  表名
        :param where:  参考 where_parse
        :param commit: True 自动提交

        where={
            "id":100
        }
        """

        if not table:
            return False

        where, args = self.where_parse(where)
        sql = "DELETE FROM %s %s " % (table, where)

        cur = self.cursor()
        if not self.execute(cur, sql, args):
            cur.close()
            return False

        if commit:
            self.commit()

        cur.close()
        return True

    def last_insert_id(self):
        cur = self.cursor()
        if not self.execute(cur, "SELECT LAST_INSERT_ID()", None):
            cur.close()
            return None

        r = cur.fetchall()
        cur.close()

        if r:
            return r[0][0]
        return None

