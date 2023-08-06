#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import csv


class Chaos():
    def _null(self):
        return None

    def _num(self):
        return 123

    def _xss(self):
        return "<script>alert(1)</script>"

    def _empty(self):
        return ""

    def _sql(self):
        return " --"

    def _long(self):
        return "a" * 32

    def _symbol(self):
        return "!@#\\/"

    def ret_file(self, file, params, retlist):
        with open(file, 'w', encoding='utf-8', newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(params)
            csv_writer.writerows(retlist)

    @classmethod
    def chaos(cls, params, custom=None, type='product', file=None):
        """
        :param params:参数列表 ["name", "age","sex","like"]
        :param custom:自定义参数值 {"name": "zhangsan","like":"qiu"}
        :param type:
                    product 笛卡尔积　　（有放回抽样排列）
                    permutations 排列　　（不放回抽样排列）
                    combinations 组合,没有重复　　（不放回抽样组合）
                    combinations_with_replacement 组合,有重复　　（有放回抽样组合）
        :param file: 要生成用例的文件，如：ret.csv
        :return:
        """
        clist = []
        for i in dir(Chaos):
            if i[0] == "_" and i[1] != "_":
                clist.append(eval("Chaos()." + i + "()"))
        if custom is None:
            custom = dict()

        if type == "product":
            retlist = [list(i) for i in itertools.product(clist, repeat=len(params) - len(custom))]
        elif type == "permutations":
            retlist = [list(i) for i in itertools.permutations(clist, len(params) - len(custom))]
        elif type == "combinations":
            retlist = [list(i) for i in itertools.combinations(clist, len(params) - len(custom))]
        elif type == "combinations_with_replacement":
            retlist = [list(i) for i in itertools.combinations_with_replacement(clist, len(params) - len(custom))]
        else:
            raise Exception("type参数错误")

        for k, v in custom.items():
            for i in retlist:
                i.insert(params.index(k), v)
        if file:
            Chaos().ret_file('ret.csv', params, retlist)

        return params, retlist


if __name__ == '__main__':
    params = ["name", "age", "sex", "like"]
    custom = {"name": "zhangsan", "like": "qiu"}
    print(Chaos.chaos(params, custom, type="product", file='ret.csv'))
