# pandas最新版兼容性审查与逐例对应

核对日期2026-10-24。官方发布记录最新稳定版为3.1.0（2026-10-22）；运行版本及警告检查见《验证记录.md》。原件未执行；逐例阅读3.1的13个、3.2的34个代码单元，原编号均保留对应。3.1原9—13按教师要求单列《选做内容.ipynb》，不纳入正课。

## 已正式弃用、推荐迁移与普通修正分开记录

| 原位置 | 分类 | 修订与依据 |
|---|---|---|
| 3.2原27—28，drop(..., inplace=True) | **pandas3.1正式弃用参数** | `edited = edited.drop(columns=...)` / `drop(index=...)`；drop方法本身仍支持。见[3.1弃用说明](https://pandas.pydata.org/pandas-docs/stable/whatsnew/v3.1.0.html#deprecations) |
| 3.2原2、23，.values | 仍支持，官方推荐替代 | `to_numpy()`；明确会丢标签，布尔数组必须对应同一行顺序。见[values文档](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html) |
| 3.2原22 | 原代码错误，不是新近移除 | 整数ID与字符串不匹配；改loc和整数比较。官方文档限制iloc使用布尔Series，本机整数索引存在可接受特例，详见下方实测记录。见[索引文档](https://pandas.pydata.org/docs/user_guide/indexing.html) |
| 3.2原8—10 | 教学可读性改进 | 连续[]读操作不等于链式赋值，原读取未被一概弃用；改iloc/head明确意图 |
| 3.2原24 | 原loc赋值本就正确，保留 | 另用copy隔离演示；补充不要链式赋值。见[迁移指南](https://pandas.pydata.org/docs/user_guide/migration.html) |
| 3.2原4 | pandas3行为变化 | 字符串默认推断str，不能把旧输出object当固定答案；无需强制改回object |
| 3.2原25 | 普通教学改进 | map(lambda x:x.month)仍支持，改显式to_datetime格式与dt.month。见[dt.month](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.month.html) |
| 3.2原29—34 | 仍支持与口径修正 | mean/describe/value_counts/category保留；使用未被删改的基线，区分记录频数和销量。见[describe](https://pandas.pydata.org/docs/reference/api/pandas.Series.describe.html) |
| 3.1原1—4 | 仍支持 | read_table/read_csv保留；错误分隔符和header=None标为对照，不冒充推荐参数 |
| 3.1原5 | 数据编码问题 | UTF-8文件不能随意改GBK；捕获UnicodeDecodeError，不吞其他错误 |
| 3.1原6、8 | 输出位置与额外索引问题 | 输出改本包outputs；to_csv/to_excel均index=False，回读检查 |
| 3.1原7—8 | 可选依赖 | openpyxl不存在时明确跳过Excel；CSV继续。见[read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html) |
| 3.1原9—13 | 教师调整与环境替代 | 独立选做，按教师最新要求改用MySQL；PyMySQL讲解基础操作，SQLAlchemy配合pandas读写。read_sql系列未被弃用，新版连接代码尚未实跑。见[read_sql](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) |

实测差异：本机pandas 3.1.0及现有3.0.5允许整数索引的布尔Series传入iloc，但字符串索引的布尔Series会报ValueError。官方索引指南仍说明iloc不支持布尔Series。因此不能笼统声称原22在所有当前环境必然报错；确定的问题是整数商品ID与字符串比较导致空结果。为表达清楚且减少环境差异，本课统一条件筛选用loc，iloc对照使用to_numpy()。这一差异不影响修订后的代码。

本次未在原示例中发现必须迁移的已移除pandas接口；发现drop的inplace参数正式弃用。不能扩大结论为“所有inplace均弃用”，也不能把.values称为已移除。未在原件中出现的append、ix等不列为本次发现。
安全检查：原3.1含写教材tmp及连接本机MySQL、replace表；均不原样执行。新正课写包内outputs；新选做面向MySQL专用教学库，建新演示表，不自动删表；to_sql使用fail而非replace。3.2仅内存操作。

## 逐例映射

编号指原Notebook从1开始的代码单元序号；新文件同编号标题定位，额外导入单元标“补充”。

| 原文件/编号 | 新位置与处理 |
|---|---|
| 3.1 / 1 | 01 Notebook“原示例 1”：read_table：明确分隔符 |
| 3.1 / 2 | 01 Notebook“原示例 2”：read_csv：本周首选 |
| 3.1 / 3 | 01 Notebook“原示例 3”：错误分隔符对照 |
| 3.1 / 4 | 01 Notebook“原示例 4”：header=None对照 |
| 3.1 / 5 | 01 Notebook“原示例 5”：编码错误演示 |
| 3.1 / 6 | 01 Notebook“原示例 6”：CSV导出与回读 |
| 3.1 / 7 | 01 Notebook“原示例 7”：读取Excel（依赖具备时演示） |
| 3.1 / 8 | 01 Notebook“原示例 8”：Excel导出与回读 |
| 3.1 / 9 | 选做内容/选做内容.ipynb 第1、2、11节，MySQL选做，不在正课 |
| 3.1 / 10 | 选做内容/选做内容.ipynb 第12节SHOW TABLES，MySQL选做，不在正课 |
| 3.1 / 11 | 选做内容/选做内容.ipynb 第5、6、12节查询，MySQL选做，不在正课 |
| 3.1 / 12 | 选做内容/选做内容.ipynb 第12节pandas读取，MySQL选做，不在正课 |
| 3.1 / 13 | 选做内容/选做内容.ipynb 第13节写表与回读，MySQL选做，不在正课 |
| 3.2 / 1 | 02 Notebook“原示例 1”：读取并看行标签 |
| 3.2 / 2 | 02 Notebook“原示例 2”：转为NumPy数组 |
| 3.2 / 3 | 02 Notebook“原示例 3”：列名 |
| 3.2 / 4 | 02 Notebook“原示例 4”：数据类型 |
| 3.2 / 5 | 02 Notebook“原示例 5”：size、ndim、shape |
| 3.2 / 6 | 02 Notebook“原示例 6”：转置（快速浏览） |
| 3.2 / 7 | 02 Notebook“原示例 7”：取单列 |
| 3.2 / 8 | 02 Notebook“原示例 8”：取一列前5个位置 |
| 3.2 / 9 | 02 Notebook“原示例 9”：取两列前5行 |
| 3.2 / 10 | 02 Notebook“原示例 10”：取位置1—5的行 |
| 3.2 / 11 | 02 Notebook“原示例 11”：head |
| 3.2 / 12 | 02 Notebook“原示例 12”：tail |
| 3.2 / 13 | 02 Notebook“原示例 13”：loc取命名列 |
| 3.2 / 14 | 02 Notebook“原示例 14”：iloc取位置3的列 |
| 3.2 / 15 | 02 Notebook“原示例 15”：loc取两列 |
| 3.2 / 16 | 02 Notebook“原示例 16”：iloc取位置1和3 |
| 3.2 / 17 | 02 Notebook“原示例 17”：loc取标签3 |
| 3.2 / 18 | 02 Notebook“原示例 18”：loc标签切片 |
| 3.2 / 19 | 02 Notebook“原示例 19”：iloc取位置3 |
| 3.2 / 20 | 02 Notebook“原示例 20”：iloc位置切片 |
| 3.2 / 21 | 02 Notebook“原示例 21”：按商品ID筛选 |
| 3.2 / 22 | 02 Notebook“原示例 22”：修正原布尔索引错误 |
| 3.2 / 23 | 02 Notebook“原示例 23”：iloc布尔数组（对照） |
| 3.2 / 24 | 02 Notebook“原示例 24”：在副本修改类别 |
| 3.2 / 25 | 02 Notebook“原示例 25”：增加月份 |
| 3.2 / 26 | 02 Notebook“原示例 26”：增加常数列 |
| 3.2 / 27 | 02 Notebook“原示例 27”：删除列 |
| 3.2 / 28 | 02 Notebook“原示例 28”：删除标签行 |
| 3.2 / 29 | 02 Notebook“原示例 29”：NumPy均值对照（可略） |
| 3.2 / 30 | 02 Notebook“原示例 30”：销售价格均值 |
| 3.2 / 31 | 02 Notebook“原示例 31”：描述性统计 |
| 3.2 / 32 | 02 Notebook“原示例 32”：类别频数 |
| 3.2 / 33 | 02 Notebook“原示例 33”：category类型（选讲） |
| 3.2 / 34 | 02 Notebook“原示例 34”：类别描述性统计（选讲） |
