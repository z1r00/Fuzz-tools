# Fuzz-tools

## z1-crashes-classification-tool

### 描述

这是一个基于asan的fuzz crashes分类工具（2023-03-31）
会去除重复的样本，写这个tool的原因是其他的检测工具没有装上

用法如下，用mjs来演示

```bash
$ python3 main.py /home/ubuntu/asan_fuzz_mjs/mjs/build/mjs /home/ubuntu/mjs_fuzz/out/crashes out.txt
```

`/home/ubuntu/asan_fuzz_mjs/mjs/build/mjs` 这是目标文件（编译的时候加上-fsanitize=address）

`/home/ubuntu/mjs_fuzz/out/crashes` 这是fuzz之后的crashes存放目录

`out.txt` 这是结果保存的位置，这里演示的是保存在out.txt中

目前只写了argv[1]/argv[2]/argv[3]

### 界面

![](https://github.com/z1r00/Fuzz-tools/blob/main/img/1.png)

### Todo

- 适用于输入流

- 支持更多的参数
