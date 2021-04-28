# About
*本脚本是在 https://github.com/sseaky/XShell2MobaXterm 的基础上修改的。*

*在升级到xshell 7后发现不能导出原脚本的文件，所以更新了一下。*

***脚本写好才发现，原来导出的.xts文件解压出来就可以使用Seaky的脚本了，做了个无用功...***

***就当一个补充吧....***

MobaXterm的配置文件中，连接字串用%分割，很多意义不明，不同协议也有区别，所以只测试了写本脚本时涉及的ssh、telnet、ftp三种类型的常用参数。



## 版本

MobaXterm:	v21.1 Build 4628

XShell:	7 (Build 0065)

Python:	3.9

OS:	Windows 10



## 使用

python XShell2MobaXterm.py <XShell_Sessions_file_1> <XShell_Sessions_file_2> ...

理论上后面可以接无限个文件。

之所以不采用之前的文件夹读取的方式是因为会读取不必要文件，并且文件目录会混乱。

## 描述

将Xshell导出的.tsv格式文件转为MobaXterm可以导入的.mxtsessions格式文件。

目前Xshell 7 版本可以导出三种文件，[.csv、.xts、.tsv]，其中，.xts文件为压缩包文件，里面是.xsh文件，.csv顾名思义，而.tsv文件就是文本文件。

三者相比较.xts最复杂，信息最多，另外两个信息量相同，.csv文件最方便处理，而且我们导出需要的信息基本都有，所以选择了.csv文件作为源处理文件。

导入后所有会话的密码都需要手动重新输入。