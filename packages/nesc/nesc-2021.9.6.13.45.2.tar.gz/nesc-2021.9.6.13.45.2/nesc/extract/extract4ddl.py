#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : nesc.
# @File         : extract4ddl
# @Time         : 2021/9/6 下午12:28
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def process_func(l):
    if '-' in l:
        字段说明 = re.split('-+', l)[1].strip()
        l = re.split('-+', l)[0].strip()
    else:
        字段说明 = None

    l = l.strip().strip(',').strip(' not null').strip().replace('\t', ' ')

    字段名 = l[0].split()[0]

    if '(' in l.split()[1]:
        数据类型 = l.split()[1].split('(')[0]
        数据长度 = l.split('(')[-1][:-1]
    else:
        数据类型 = l.split()[1]
        数据长度 = None

    return [字段名, 数据类型, 数据长度, 字段说明]


def extract_data(p, start_func=lambda x: x.startswith('create table'), end_func=lambda x: x.startswith('tablespace')):
    flag = False
    data_map = {}
    with open(p) as f:
        for r in tqdm(f):
            if flag:  # 左开右闭
                data_map.setdefault(table, []).append(r.strip())

            if start_func(r):
                table = r.strip().split()[-1]
                flag = True

            if end_func(r):
                flag = False
    return data_map


def main(ipath, opath=None):
    p = Path(ipath)
    if opath is None:
        opath = p.parent / f"{p.name}.tsv"
    d = extract_data(p)
    dd = {i: j[1:-2] for i, j in d.items()}

    df = pd.DataFrame(dd.items(), columns=['表名', '字段名'])
    df = df.explode('字段名', True)
    df[['字段名', '数据类型', '数据长度', '字段说明']] = df['字段名'].map(process_func).values.tolist()

    df.to_csv(opath, '\t', index=False)

    logger.info(bjson(dict(zip(df.nunique().index, df.nunique()))))

    return


if __name__ == '__main__':
    main('/Users/yuanjie/Desktop/notebook/0_TODO/mot_part.sql')
