# pandas 3.1基础速查表

适用第五周3.1—3.2，示例df为已读取的表；输入data下CSV，导出到outputs。先核查字段与单位。

| 目的 | 写法 | 易错点 |
|---|---|---|
| 读取CSV | `pd.read_csv('data/salesdata.csv', encoding='utf-8')` | 默认逗号、有表头 |
| 预览 | `df.head(3)` / `df.tail(3)` | 文件行序不等于时间顺序 |
| 结构 | `df.shape` / `df.columns` / `df.dtypes` | shape是属性，无括号 |
| 概览 | `df.info()` | 自行打印，返回None |
| 一列 / 一列表 | `df['销售量/个']` / `df[['销售量/个']]` | Series与DataFrame |
| 按标签 | `df.loc[2:6, ['销售量/个']]` | 有序唯一标签下含右端 |
| 按位置 | `df.iloc[2:7, [3]]` | 0起算，不含7 |
| 条件筛选 | `df.loc[df['商品ID'] == 10000019]` | 检查比较类型，多个条件用括号及&/\| |
| 创建副本 | `practice = df.copy()` | 不污染基线 |
| 单步赋值 | `practice.loc[条件, '列名'] = 新值` | 不用链式赋值 |
| 增列 | `practice['标记'] = 1` | 常数赋给全部行 |
| 删除列 | `practice = practice.drop(columns='标记')` | 3.1弃用drop的inplace参数 |
| 删除行标签 | `practice = practice.drop(index=[1,2,3])` | 标签未自动重排 |
| 均值 / 中位数 | `df['销售价格/元'].mean()` / `.median()` | 默认跳过缺失；写清对象、单位 |
| 描述统计 | `df['销售价格/元'].describe()` | std为样本标准差；50%为中位数 |
| 类别频数 | `df['商品类别'].value_counts(dropna=False)` | 条数不是销量 |
| 有效数 / 缺失数 | `s.count()` / `s.isna().sum()` | len(s)包含缺失行 |
| NumPy转换 | `df.to_numpy()` | 推荐替代.values，标签会丢失 |
| 写CSV | `df.to_csv('outputs/练习.csv', index=False, encoding='utf-8-sig')` | 先创建outputs；回读检查 |
| 提取月份 | `pd.to_datetime(s, format='%Y/%m/%d %H:%M').dt.month` | 格式必须与输入一致 |

pandas 3的字符串列通常是str，旧环境可能是object；用isna识别缺失。类别类型仍可用，但并非所有文本都必须改category。read_table、read_csv、loc/iloc、mean、describe均保留；不能将教学写法调整统称为API被移除。

工业数据禁止混合不同单位直接平均、求和、排名；缺失不等于零。本周只统计同产品有效月份，不计算年度增长率。

## 扩展内容速查（2026-10-25，选讲）

完整说明和课堂位置见[扩展目录](09_扩展内容说明与选讲建议.md)。df、s及条件只是通用变量名；以下是写法骨架。

| 目的 | 写法 | 口径与提醒 |
|---|---|---|
| 局部预览 | `pd.read_csv(..., usecols=['列名'], nrows=5)` | 前几行不是随机样本 |
| 文本编号 | `pd.read_csv(..., dtype={'编号': 'string'})` | 比较值也用字符串，保留前导零 |
| 缺失标记 | `pd.read_csv(..., na_values=['未报'])` | 默认还识别其他常见缺失标记 |
| 指定工作表 | `pd.read_excel(..., sheet_name='表名')` | sheet_name=None返回字典 |
| 读取日期 | `pd.read_csv(..., parse_dates=['日期'], date_format='%Y-%m-%d')` | pandas2.0起；必须检查dtype |
| 单格访问 | `df.at[行标签, '列名']` / `df.iat[行位置, 列位置]` | 仅单格，多行列用loc/iloc |
| 多值筛选 | `s.isin(['甲', '乙'])` | 组合条件用括号与&、\|、~ |
| 区间筛选 | `s.between(50, 100, inclusive='both')` | 包含两端 |
| 新行号 | `df.reset_index(drop=True)` | 不排序，不恢复删除行 |
| 改列名 | `df.rename(columns={'旧列': '新列'})` | 接收返回表，保留单位 |
| 定制统计 | `s.agg(['count', 'mean', 'median', 'min', 'max'])` | 显式限定数值业务指标 |
| 记录占比 | `s.value_counts(normalize=True, dropna=False)` | 分母含缺失，不是销量占比 |
| 数值转换 | `pd.to_numeric(s, errors='coerce')` | 转换失败变缺失，保留原文核查 |
| 缺失合计 | `s.sum(min_count=1)` | 全缺失仍给缺失；不证明时期完整 |
| 按值排序 | `df.sort_values('日期')` | 日期先转正确类型 |
| 空结果 | `df.empty` | 有行但全缺失的表不一定为空 |

扩展不自动计入必做。原学生ZIP保留既有版本，未包含本次新增速查段；若需要发放本次扩展，教师另发此更新文件或课堂Notebook，学生题目仍独立留空。
