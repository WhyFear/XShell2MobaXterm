# -*- coding: utf-8 -*-
# @Author: Seaky
# @Modify: pakro
# @Date:   2021/4/27
# @Description: 将Xshell导出的.tsv格式文件转为MobaXterm可以导入的.mxtsessions格式文件。
# 目前Xshell 7 版本可以导出三种文件，[.csv、.xts、.tsv]，其中，.xts文件为压缩包文件，里面是.xsh文件，.csv顾名思义，而.tsv文件就是文本文件。
# 三者相比较.xts最复杂，信息最多，另外两个信息量相同，.csv文件最方便处理，而且我们导出需要的信息基本都有，所以选择了.csv文件作为源处理文件。

import csv
import sys
from copy import deepcopy

PATTERN1 = '{name}=#{icon}#{protocol}%{host}%{port}%{user}'
PATTERN2 = '#MobaFont%10%0%0%0%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0#0#{description} #-1'

CLASS = {
    'SSH': {
        'data':
            {'name': '', 'icon': 109, 'protocol': 0, 'host': '', 'port': 22, 'user': '', 'keyfile': '',
             'description': ''},
        'pattern':
            PATTERN1 + '%%-1%-1%%%22%%0%0%0%{keyfile}%%-1%0%0%0%%1080%%0%0%1' + PATTERN2
    },
    'TELNET': {
        'data':
            {'name': '', 'icon': 98, 'protocol': 1, 'host': '', 'port': 23, 'user': '', 'description': ''},
        'pattern':
            PATTERN1 + '%%2%%22%%%0%0%%1080%' + PATTERN2
    },
    'FTP': {
        'data':
            {'name': '', 'icon': 130, 'protocol': 6, 'host': '', 'port': 21, 'user': '', 'description': ''},
        'pattern':
            PATTERN1 + '%-1%%0%0%0%0%%21%%%0%0%-1%0%0%0%' + PATTERN2
    },
}


def convert(source_dir: list, output):
    with open(output, 'w', encoding="utf-8") as output_file:
        # 先写入四行数据，不作为目录。所有source文件按照文件名进行装入。
        output_file.write('[Bookmarks]\n')
        output_file.write(f'SubRep=\n')
        output_file.write('ImgNum=42\n')
        output_file.write('\n')  # 换行写入下一个目录
        i = 1
        for file_name in source_dir:
            if not file_name.endswith('.csv'):
                print(f"wrong file type! {file_name},skip this file...", )
                continue
            output_file.write(f'[Bookmarks_{i}]\n')
            output_file.write(f'SubRep={file_name.split(".")[0]}\n')  # 文件名作为MobaXterm的文件夹名
            output_file.write('ImgNum=41\n')

            with open(file_name, "r", encoding="utf-8") as config_file:
                reader = csv.reader(config_file)
                for line in reader:
                    name = line[0]
                    protocol = line[1]
                    host = line[2]
                    port = line[3]
                    user = line[4]
                    if protocol in ['SSH', 'FTP', 'TELNET']:
                        d = deepcopy(CLASS[protocol]['data'])
                        d.update({
                            'name': name,
                            'host': host,
                            'port': port,
                            'user': user,
                        })
                        output_file.write(CLASS[protocol]['pattern'].format(**d) + '\n')
                        i += 1
                    else:
                        print('unknown {}, {}'.format(protocol, file_name))
            output_file.write('\n')  # 换行写入下一个目录


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # 多个文件多个参数，理论上支持无限个。
        print('Usage: python XShell2MobaXterm.py <XShell_Sessions_file_1> <XShell_Sessions_file_2> ...')
    else:
        source_files = sys.argv[1:]
        output = 'Xshell2MobaXterm.mxtsessions'
        convert(source_files, output)
        print('Export {} to {} done.'.format(source_files, output))
