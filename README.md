# Fuzz-tools

## z1-crashes-classification-tool

### 描述

这是一个基于asan+afl的fuzz crashes分类工具（2023-03-31）
会去除重复的样本，写这个tool的原因是其他的检测工具没有装上

用法如下

```bash
usage: main.py [-h] -p P -c C [-m M] [-o O] [-v]

Description of your program

optional arguments:
  -h, --help     show this help message and exit
  -p P           application
  -c C           crashes folder
  -m M           command
  -o O           save result
  -v, --version  show program's version number and exit
```

-p 是程序

-c 是crash保存的目录

-m 是程序执行crash的参数，如果没有则不填

-o 是保存结果，可以不填

用mjs来演示

```bash
$ python3 main.py -p /home/ubuntu/asan_fuzz_mjs/mjs/build/mjs -c /home/ubuntu/mjs_fuzz/fuzz_out/crashes
```

`/home/ubuntu/asan_fuzz_mjs/mjs/build/mjs` 这是目标文件（编译的时候加上-fsanitize=address）

`/home/ubuntu/mjs_fuzz/out/crashes` 这是fuzz之后的crashes存放目录


### 界面

![](https://github.com/z1r00/Fuzz-tools/blob/main/img/1.png)

### Todo

- 适用于输入流

- 支持更多的参数
