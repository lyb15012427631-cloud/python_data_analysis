# 第三周NumPy速查表

| 业务目的 | 写法 | 提醒 |
|---|---|---|
| 导入 | `import numpy as np` | np是约定的别名 |
| 创建数值数组 | `np.array([100,120], dtype=float)` | 元素共享dtype |
| 连续整数 | `np.arange(2014,2024)` | 不含2024 |
| 看结构 | `a.shape / a.ndim / a.size / a.dtype` | 属性不加()；一维shape如(10,) |
| 取行列 | `a[0,1]`、`a[:,1]` | 从0计数，逗号分隔行列 |
| 切片 | `a[1:3]` | 不含位置3 |
| 改形状 | `a.reshape(3,2)` | 元素总数必须相等 |
| 并排两列 | `np.column_stack((years,yields))` | 输出二维数组；年份可能显示成浮点数 |
| 类型转换 | `text.astype(float)` | 中文“年”须先去除 |
| 按条件选取 | `years[yields > yields.mean()]` | 两数组长度和顺序一致 |
| 多条件 | `(years>=2014) & (years<=2023)` | 每个条件加括号，数组不用and |
| 汇总 | `np.sum(a)`、`np.mean(a)`、`np.std(a,ddof=0)` | 先明确统计范围、单位 |
| 极值和位置 | `np.max(a)`、`np.argmax(a)` | argmax返回位置，且只取首个并列位置 |
| 汇总行维度 | `a.sum(axis=0)` | 每列一个结果；只统计同口径值 |
| 汇总列维度 | `a.sum(axis=1)` | 每行一个结果 |
| 排序位置 | `np.argsort(a)` | 用同一位置索引同步重排年份与产量 |
| 相邻增长量 | `yields[1:]-yields[:-1]` | 先按年份升序 |
| 同比百分数 | `(yields[1:]-yields[:-1])/yields[:-1]*100` | 上年为基期，不能除以0 |
| 读取CSV | `np.loadtxt(path,delimiter=',',skiprows=1,usecols=(0,1),dtype=str,encoding='utf-8-sig')` | 本文件先读文本再转换 |

10个年份对应9个相邻年度间隔。原文件降序；只反转年份、不反转产量会错配。年份列不得参与产量均值与求和。
`*`对ndarray是逐元素乘法；`@`是矩阵乘法（拓展）。标准差描述离散程度，单位为万吨；不是增长率。
