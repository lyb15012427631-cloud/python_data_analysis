# %% [markdown]
# # 任务3.2 分析工业产品产量数据的基本情况｜新版 pandas 课堂版
#
# 第五周第2—4课时。目标：理解标签和位置，完成筛选、在副本增删改、解释基础统计，再迁移到单一工业产品。
# 原34个代码单元逐一对应。输入为data/salesdata.csv，末尾读取data/工业产品产量数据.csv；本Notebook不导出文件。依赖Python、pandas、NumPy（仅原示例29）。
# 从上往下运行；与3.1独立，不依赖上一份Notebook变量。统计始终使用完整salesdata基线；修改和删除只作用于edited，避免演示顺序改变统计对象。验证状态见《验证记录.md》。

# %% [markdown]
# ## 本次新增：扩展内容导航（2026-10-25）
#
# 原教学单元按原顺序完整保留；下列扩展就地插入对应示例后，均可按学情跳过。160分钟原教学安排不变，建议每节只选1—2项，其余课后查阅。学生必做题与教师答案保持原样。
#
# - **3.2-A** 保留二维结构：双括号与单行列表（建议选讲）
# - **3.2-B** 换成文字行标签，真正看清loc与iloc（建议选讲）
# - **3.2-C** 只取一个值：at与iat（课后选做）
# - **3.2-D** 组合筛选：&、|、~、isin与between（建议选讲）
# - **3.2-E** 布尔条件会按标签对齐（课后选做）
# - **3.2-F** 筛选后修改与Copy-on-Write（建议选讲）
# - **3.2-G** 向量化增列与Series标签对齐（建议选讲）
# - **3.2-H** 重设行号与改列名：reset_index、rename（建议选讲）
# - **3.2-I** 定制统计：agg、quantile与round（建议选讲）
# - **3.2-J** 简单平均与销量加权平均（课后选做）
# - **3.2-K** 频数、占比与不同值：normalize、unique、nunique（建议选讲）
# - **3.2-L** 文本转数值：to_numeric与异常记录核查（课后选做）
# - **3.2-M** 缺失、0与合计：sum(min_count=...)（建议选讲）
# - **3.2-N** 排序后再看首尾，以及空筛选检查（课后选做）
#
# 输入、依赖、运行顺序沿用本文件原说明；新增例子不新增落盘输出。验证状态与官方资料见[扩展说明](../说明文档/09_扩展内容说明与选讲建议.md)。

# %%
from pathlib import Path
import pandas as pd
from IPython.display import display

# 自动定位公共数据目录：可从本周根目录或代码所在子目录运行。
# 脚本以自身位置为起点，Notebook以当前工作目录为起点。
BASE = Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
if not (BASE / 'data' / 'salesdata.csv').is_file():
    BASE = BASE.parent
DATA = BASE / 'data'
OUTPUT = BASE / 'outputs'
if not (DATA / 'salesdata.csv').is_file():
    raise FileNotFoundError('请在第五周根目录或上课文件、练习文件、选做内容目录中运行。')
OUTPUT.mkdir(exist_ok=True)
print('pandas 版本：', pd.__version__)

# %% [markdown]
# ## 原示例 1｜读取并看行标签
#
# 每次重新读取源副本，保持1351行基线；默认RangeIndex不是商品ID。

# %%
salesdata = pd.read_csv(DATA / 'salesdata.csv', encoding='utf-8')
print(salesdata.index)

# %% [markdown]
# ## 原示例 2｜转为NumPy数组
#
# 原.values仍支持，官方推荐to_numpy()；转换后丢失行列标签，混合数据可能成为object数组。只显示前3行。

# %%
print(salesdata.to_numpy()[:3])

# %% [markdown]
# ## 原示例 3｜列名
#
# 列名包含单位，选列时须逐字匹配。

# %%
print(salesdata.columns)

# %% [markdown]
# ## 原示例 4｜数据类型
#
# pandas 3默认字符串通常显示str，旧版本常见object；不应把显示变化当作读错。商品ID本文件推断为整数，因此条件比较用整数。

# %%
print(salesdata.dtypes)

# %% [markdown]
# ## 原示例 5｜size、ndim、shape
#
# size是单元格数，不是记录数；二维表ndim为2。

# %%
print('元素数：', salesdata.size, '维度：', salesdata.ndim, '形状：', salesdata.shape)

# %% [markdown]
# ## 原示例 6｜转置（快速浏览）
#
# 交换行列，原表不改变；业务表通常不需要转置后分析。

# %%
print('原形状：', salesdata.shape, '转置后：', salesdata.T.shape)

# %% [markdown]
# ## 原示例 7｜取单列
#
# 一层括号返回Series；对比前课双层括号。

# %%
quantity = salesdata['销售量/个']
print(type(quantity).__name__, quantity.shape)

# %% [markdown]
# ## 扩展内容 3.2-A｜保留二维结构：双括号与单行列表（建议选讲）
#
# 业务问题：为什么一列有时显示成Series，有时仍是一张表？
# - 单个列名返回Series，列名列表返回DataFrame；`loc[0]`与`loc[[0]]`也有类似区别。
# - 后续若要保留列名或继续按表处理，列表选择能保持二维结构，并不表示单括号写法过时。
# 先预测四个shape，特别留意`(5,)`与`(1, 5)`的差别。
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
print('单列Series：', salesdata['销售量/个'].shape)
print('单列表：', salesdata[['销售量/个']].shape)
print('单行Series：', salesdata.loc[0].shape)
print('单行表：', salesdata.loc[[0]].shape)

# %% [markdown]
# ## 原示例 8｜取一列前5个位置
#
# 用iloc明确位置，替代连续[]切片；原读取方式不等于正式弃用。

# %%
display(salesdata['销售价格/元'].iloc[:5])

# %% [markdown]
# ## 原示例 9｜取两列前5行
#
# head(5)直接表达预览目的。修正原文字重复列名。

# %%
display(salesdata[['销售量/个', '销售价格/元']].head(5))

# %% [markdown]
# ## 原示例 10｜取位置1—5的行
#
# iloc[1:6]取第2—6条记录，不是自然序号第1—5行。

# %%
display(salesdata.iloc[1:6])

# %% [markdown]
# ## 原示例 11｜head
#
# 默认前5行。

# %%
display(salesdata.head())

# %% [markdown]
# ## 原示例 12｜tail
#
# 默认后5行，不等于日期最新5条，文件尚未按日期排序。

# %%
display(salesdata.tail())

# %% [markdown]
# ## 原示例 13｜loc取命名列
#
# loc使用方括号，是索引器，不是loc()函数调用。

# %%
sales1 = salesdata.loc[:, '销售价格/元']
print(sales1.size)

# %% [markdown]
# ## 原示例 14｜iloc取位置3的列
#
# 从0计数，位置3是第4列“销售量/个”，原注释“第3列”不准确。

# %%
sales2 = salesdata.iloc[:, 3]
print(sales2.name, sales2.size)

# %% [markdown]
# ## 原示例 15｜loc取两列
#
# 返回二维表；size等于行数×2。

# %%
print(salesdata.loc[:, ['销售量/个', '销售价格/元']].size)

# %% [markdown]
# ## 原示例 16｜iloc取位置1和3
#
# 实际为第2和第4列，即商品类别和销售量。

# %%
quantity_sales2 = salesdata.iloc[:, [1, 3]]
print(quantity_sales2.columns.tolist(), quantity_sales2.size)

# %% [markdown]
# ## 原示例 17｜loc取标签3
#
# 一行多列会返回Series。

# %%
display(salesdata.loc[3, ['销售量/个', '销售价格/元']])

# %% [markdown]
# ## 原示例 18｜loc标签切片
#
# 当前索引有序且唯一，2:6包含标签6。

# %%
display(salesdata.loc[2:6, ['销售量/个', '销售价格/元']])

# %% [markdown]
# ## 原示例 19｜iloc取位置3
#
# 当前默认行标签恰等于位置，不能由此认为loc和iloc通用。

# %%
display(salesdata.iloc[3, [1, 3]])

# %% [markdown]
# ## 原示例 20｜iloc位置切片
#
# 2:7不包含7，当前与loc[2:6]取同5行。

# %%
display(salesdata.iloc[2:7, [1, 3]])

# %% [markdown]
# ## 扩展内容 3.2-B｜换成文字行标签，真正看清loc与iloc（建议选讲）
#
# 业务问题：默认整数标签和位置恰好相同，怎样避免“两个方法一样”的错觉？
# 以下为**人工模拟表**。标签切片在这个有序且唯一的索引中含右端；位置切片不含右端。
# - `loc['乙店']`取标签乙店；`iloc[1]`取位置1。两个结果恰好相同只源于当前排布。
# - `loc[['乙店']]`仍是一行表。标签缺失会报KeyError，位置越界的单点访问会报IndexError。
# 观察：`loc['甲店':'乙店']`与`iloc[0:1]`各有几行？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_label_table = pd.DataFrame({'销售量/个': [3, 5, 2]}, index=['甲店', '乙店', '丙店'])
display(ext_label_table.loc['甲店':'乙店'])
display(ext_label_table.iloc[0:1])
print('标签取值：', ext_label_table.loc['乙店', '销售量/个'])
print('位置取值：', ext_label_table.iloc[1, 0])

# %% [markdown]
# ## 扩展内容 3.2-C｜只取一个值：at与iat（课后选做）
#
# 业务问题：只需要一格价格，是否还要取整行？
# - `at[行标签, 列标签]`按标签取单值，`iat[行位置, 列位置]`按位置取单值。
# - 适用于单格访问；多行多列或条件筛选仍用loc/iloc。不要把列表或切片放进at/iat。
# 观察：原表位置0、列位置4，与标签0、“销售价格/元”是否对应同一个单元格？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_price_at = salesdata.at[0, '销售价格/元']
ext_price_iat = salesdata.iat[0, 4]
print('at：', ext_price_at, 'iat：', ext_price_iat)

# %% [markdown]
# ## 原示例 21｜按商品ID筛选
#
# 10000019是本文件整数值；ID不是求平均的业务指标。

# %%
mask = salesdata['商品ID'] == 10000019
display(salesdata.loc[mask, ['销售量/个', '销售价格/元']])

# %% [markdown]
# ## 原示例 22｜修正原布尔索引错误
#
# 原代码拿整数ID与字符串比较，条件无法命中。改用loc加整数比较。带标签布尔Series不作为iloc的通用课堂写法；本机整数索引的特殊行为与官方文档限制存在差异，见审查说明。

# %%
display(salesdata.loc[salesdata['商品ID'] == 10000019, ['销售量/个', '销售价格/元']])

# %% [markdown]
# ## 原示例 23｜iloc布尔数组（对照）
#
# to_numpy()把同一表生成的布尔条件转为位置数组；初学者优先loc，别把别的表的条件直接套进来。

# %%
display(salesdata.iloc[(salesdata['商品ID'] == 10000019).to_numpy(), [3, 4]])

# %% [markdown]
# ## 扩展内容 3.2-D｜组合筛选：&、|、~、isin与between（建议选讲）
#
# 业务问题：选出指定类别中、单价在某区间的记录，如何把多个条件组合？
# - 每个比较条件加括号，用`&`表示同时成立、`|`表示任一成立、`~`表示取反；不要用Python的and/or拼接整列。
# - `isin([...])`表达多个候选值；`between(50, 100, inclusive='both')`包含两端。
# - `mask.sum()`计算True的数量；这里是命中记录条数，仍不是销量。
# 跟练：先口述区间是否包含50和100，再把候选类别改为只含类别A。
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_candidates = salesdata['商品类别'].isin(['类别A', '类别B'])
ext_range = salesdata['销售价格/元'].between(50, 100, inclusive='both')
ext_filter = ext_candidates & ext_range
print('命中记录数：', int(ext_filter.sum()))
display(salesdata.loc[ext_filter, ['商品类别', '销售量/个', '销售价格/元']].head(5))
print('低于50或高于100的记录数：', int(((salesdata['销售价格/元'] < 50) | (salesdata['销售价格/元'] > 100)).sum()))
print('不属于候选类别的记录数：', int((~ext_candidates).sum()))

# %% [markdown]
# ## 扩展内容 3.2-E｜布尔条件会按标签对齐（课后选做）
#
# 业务问题：表重新排序后，原来的条件是否还能直接按位置使用？以下为**人工模拟表**。
# - 带索引的布尔Series配合loc会按行标签对齐；布尔数组配合iloc只认当前位置。
# - `to_numpy()`会丢失标签。条件必须与当前表的顺序一致，不能为了避开报错随意转换。
# - 推荐从正在筛选的表生成条件；此处保留“旧条件”只为展示差异。
# 观察：甲乙标签的排列变了，为什么两种筛选选中了不同的店？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_align = pd.DataFrame({'销量': [10, 30]}, index=['甲店', '乙店'])
ext_old_mask = ext_align['销量'] > 20
ext_reordered = ext_align.iloc[::-1]
print('loc按标签对齐：')
display(ext_reordered.loc[ext_old_mask])
print('旧条件转数组后按位置，含义已改变：')
display(ext_reordered.iloc[ext_old_mask.to_numpy()])

# %% [markdown]
# ## 原示例 24｜在副本修改类别
#
# 仅演示修改，把类别B改为C不代表真实业务纠错。单步loc赋值符合Copy-on-Write。保留salesdata基线，后续统计使用基线。

# %%
edited = salesdata.copy()
edited.loc[edited['商品类别'] == '类别B', '商品类别'] = '类别C'
print('基线：', salesdata['商品类别'].value_counts().to_dict())
print('演示副本：', edited['商品类别'].value_counts().to_dict())

# %% [markdown]
# ## 扩展内容 3.2-F｜筛选后修改与Copy-on-Write（建议选讲）
#
# 业务问题：只在选中的两条记录上做演示修改，怎样保证原表的统计口径稳定？
# - 若要修改原表，用`df.loc[条件, '列'] = 值`一次完成；若要修改筛选结果，用`.copy()`明确建立演示副本。
# - 不使用`df[条件]['列'] = 值`这类链式赋值。pandas 3采用Copy-on-Write，链式写法不能完成对原表的预期修改；旧版本也不适合作为可靠写法。
# - 本例加1元仅演示语法，没有业务纠错依据，不代表真实调价。
# 观察：打印副本后，再看基线中同商品的价格，是否被改变？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_price_copy = salesdata.loc[salesdata['商品ID'] == 10000019].copy()
ext_price_copy.loc[:, '销售价格/元'] = ext_price_copy['销售价格/元'] + 1
display(ext_price_copy[['商品ID', '销售价格/元']])
display(salesdata.loc[salesdata['商品ID'] == 10000019, ['商品ID', '销售价格/元']])

# %% [markdown]
# ## 原示例 25｜增加月份
#
# 显式解析已知格式，再用.dt.month；原map(lambda...)仍支持，这里是简化教学。详细时间序列留到3.3。

# %%
dates = pd.to_datetime(edited['订单时间'], format='%Y/%m/%d %H:%M')
edited['月份'] = dates.dt.month
display(edited[['订单时间', '月份']].head())

# %% [markdown]
# ## 原示例 26｜增加常数列
#
# 所有行的“日”赋15只是赋值演示，不是真实订单日期。

# %%
edited['日'] = 15
display(edited['日'].head())

# %% [markdown]
# ## 扩展内容 3.2-G｜向量化增列与Series标签对齐（建议选讲）
#
# 业务问题：每行金额怎样由数量和单价得到？
# - 同一张表的两列可逐行相乘，通常比逐行for循环更清楚；`assign`返回带新列的表，适合保留基线。
# - 新列“数量×单价/元”只演示名义金额，未核实折扣、退货、税费，不能称为已确认收入。
# - Series赋给列时按标签对齐，列表按位置填入且长度必须匹配。下方对齐例为**人工模拟数据**。
# 观察：为什么传入Series先写乙、再写甲，结果仍按甲、乙对应？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_amount_table = salesdata.head(3).assign(
    **{'数量×单价/元': salesdata['销售量/个'].head(3) * salesdata['销售价格/元'].head(3)})
display(ext_amount_table)
ext_assign_table = pd.DataFrame({'门店': ['甲', '乙']}, index=[10, 20])
ext_assign_table['数量'] = pd.Series([5, 3], index=[20, 10])
display(ext_assign_table)

# %% [markdown]
# ## 原示例 27｜删除列
#
# pandas 3.1正式弃用drop的inplace参数，改为接收返回的新表；不是drop方法被移除。

# %%
edited = edited.drop(columns='日')
print(edited.columns.tolist())

# %% [markdown]
# ## 原示例 28｜删除标签行
#
# 删除标签1、2、3；不自动重排行号。展示标签与位置在删除后不同。

# %%
edited = edited.drop(index=[1, 2, 3])
print('原表行数：', len(salesdata), '演示副本行数：', len(edited))
print('前5个标签：', edited.index[:5].tolist())
print('删除后位置1对应标签：', edited.iloc[1].name)

# %% [markdown]
# ## 扩展内容 3.2-H｜重设行号与改列名：reset_index、rename（建议选讲）
#
# 业务问题：删除后行号出现空档，是数据丢失以外还需要“修复”的问题吗？
# - 标签有空档不影响统计。需要连续展示行号时可用`reset_index(drop=True)`；它不排序、不恢复已删记录。
# - 不写drop=True时，旧索引通常会作为一列保留。若旧标签有业务意义，应先决定是否保留。
# - `rename(columns={...})`修改副本列名；演示名称仍写清单位。
# 观察：重设后的第2行原来是什么标签？为什么原edited的索引没有变？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_reset = edited.reset_index(drop=True).rename(columns={'销售价格/元': '单价/元'})
print('edited原标签：', edited.index[:5].tolist())
print('展示表新标签：', ext_reset.index[:5].tolist())
display(ext_reset[['商品ID', '单价/元']].head(3))

# %% [markdown]
# ## 原示例 29｜NumPy均值对照（可略）
#
# 保留原示例对应。没有必要为算均值新引入NumPy；正课重点用Series.mean。统计未删行的基线。

# %%
import numpy as np
print(np.mean(salesdata['销售价格/元']))

# %% [markdown]
# ## 原示例 30｜销售价格均值
#
# 1351条销售记录的价格简单平均，单位元；不是销量加权平均，也不是工业产量。

# %%
price_mean = salesdata['销售价格/元'].mean()
print(f'基线销售价格简单平均：{price_mean:.2f}元')

# %% [markdown]
# ## 原示例 31｜描述性统计
#
# count为非缺失数；std是样本标准差ddof=1；25%、50%、75%为分位数，中位数为50%。

# %%
display(salesdata['销售价格/元'].describe())

# %% [markdown]
# ## 扩展内容 3.2-I｜定制统计：agg、quantile与round（建议选讲）
#
# 业务问题：只想交付均值、中位数、极值，是否一定要整份describe？
# - 单列`agg(['count', 'mean', ...])`一次列出所需指标；这里不做groupby。
# - `quantile(0.5)`对应中位数，四分位数默认线性插值；`std()`默认样本标准差ddof=1，整体标准差可显式写ddof=0，选哪种由分析对象决定。
# - `round(2)`用于展示，原价格列不改变；只对单价（元）统计，商品ID不作均值。
# 观察：count为何可能显示为小数？多个指标组合成Series后可能共用浮点dtype，条数含义没有改变。
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_price_summary = salesdata['销售价格/元'].agg(['count', 'mean', 'median', 'min', 'max'])
display(ext_price_summary.round(2))
display(salesdata['销售价格/元'].quantile([0.25, 0.5, 0.75]))
print('样本标准差：', round(salesdata['销售价格/元'].std(ddof=1), 2))
print('整体标准差：', round(salesdata['销售价格/元'].std(ddof=0), 2))

# %% [markdown]
# ## 扩展内容 3.2-J｜简单平均与销量加权平均（课后选做）
#
# 业务问题：10元卖1个、20元卖9个，“平均售价”应是哪一个数？以下为**人工模拟数据**，两行单位均为元/个、个。
# - 简单平均给每条记录相同权重；销量加权平均用“数量×单价”合计除以总数量。
# - 必须保证产品或计价口径可比、数量非负且总数量大于0；不能直接推广到跨单位产量，也不能把负数退货当普通销量。
# - 两个数字回答不同问题，应先写清统计口径再选公式。
# 先手算：这两个平均数分别是多少？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_weighted_demo = pd.DataFrame({'单价/元': [10, 20], '数量/个': [1, 9]})
ext_simple_mean = ext_weighted_demo['单价/元'].mean()
ext_total_quantity = ext_weighted_demo['数量/个'].sum()
ext_weighted_mean = (ext_weighted_demo['单价/元'] * ext_weighted_demo['数量/个']).sum() / ext_total_quantity
print('记录简单平均：', ext_simple_mean, '元')
print('按销量加权平均：', ext_weighted_mean, '元')

# %% [markdown]
# ## 原示例 32｜类别频数
#
# 统计记录条数，不是各类销售量；默认排除缺失，可用dropna=False显示缺失。

# %%
display(salesdata['商品类别'].value_counts(dropna=False))

# %% [markdown]
# ## 扩展内容 3.2-K｜频数、占比与不同值：normalize、unique、nunique（建议选讲）
#
# 业务问题：类别B占了多少条销售记录？这和B类销量占比相同吗？
# - `value_counts(normalize=True)`得到记录频率；默认排除缺失。这里显式`dropna=False`，分母包含缺失记录。
# - `unique()`列出不同值（按首次出现顺序），`nunique()`给出不同值个数；它们默认对缺失的处理不同，需显式说明。
# - 本表没有类别缺失，记录占比仍不等于销量占比或金额占比。
# 观察：为什么频数和占比的索引相同，数值的单位却不同？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_category_counts = salesdata['商品类别'].value_counts(dropna=False)
ext_category_shares = salesdata['商品类别'].value_counts(normalize=True, dropna=False)
ext_category_report = pd.DataFrame({'记录条数': ext_category_counts,
                                    '记录占比/%': (ext_category_shares * 100).round(2)})
display(ext_category_report)
print('出现过的类别：', salesdata['商品类别'].unique().tolist())
print('不同类别数（含缺失）：', salesdata['商品类别'].nunique(dropna=False))

# %% [markdown]
# ## 原示例 33｜category类型（选讲）
#
# 仍支持。分类Series适合有限类别，不能直接给未知新类别赋值；此处仅转换单独变量。

# %%
category = salesdata['商品类别'].astype('category')
print(category.dtype)

# %% [markdown]
# ## 原示例 34｜类别描述性统计（选讲）
#
# count非缺失条数、unique不同类别数、top最常见类别、freq该类别条数。

# %%
display(category.describe())

# %% [markdown]
# ## 补充：info与缺失值（基础）
#
# info直接打印，不要print(salesdata.info())，否则末尾多一个None。isna().sum()逐列统计缺失数量，先检查再决定怎么处理。

# %%
salesdata.info()
print(salesdata.isna().sum())

# %% [markdown]
# ## 扩展内容 3.2-L｜文本转数值：to_numeric与异常记录核查（课后选做）
#
# 业务问题：数量列混入“待核实”时，能否静默地当成0？下方是**人工模拟数量文本**。
# - `pd.to_numeric`默认遇到不合法文本报错；`errors='coerce'`会把它转成缺失，只适合配合异常核查。
# - 使用“原值非缺失且转换后缺失”找出新产生的异常，保留原文本等待确认；不要直接填0。
# - 空字符串是否算原始缺失取决于前面的读取规则，本模拟中用None代表原始缺失。
# 观察：原始缺失与解析失败各有几条，能否从转换后的列单独区分？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_number_text = pd.Series(['12', '8.5', '待核实', None], name='数量原文')
ext_number_parsed = pd.to_numeric(ext_number_text, errors='coerce')
ext_new_invalid = ext_number_text.notna() & ext_number_parsed.isna()
display(pd.DataFrame({'原文': ext_number_text, '转数值': ext_number_parsed,
                      '解析失败待核对': ext_new_invalid}))
print('原始缺失：', int(ext_number_text.isna().sum()), '解析失败：', int(ext_new_invalid.sum()))

# %% [markdown]
# ## 迁移：读取真正的工业产量数据（基础）
#
# 本文件是“任务实现/项目3”原版CSV副本，仅选取基础读取与统计，不执行原综合Notebook。
# 一行是“一个产品、一个月份”的观测。产品名称带单位，全表产量混有万吨、亿立方米、亿千瓦时等，不能直接全列求均值、求和或排名。
# 这里限定“原煤产量当期值/万吨”、2023年，避免跨单位。不要把销售量当产量。

# %%
industry = pd.read_csv(DATA / '工业产品产量数据.csv', encoding='utf-8')
print('完整产量表：', industry.shape)
display(industry.head(3))
# 年份筛选利用本文件的已知文本格式；不把字符串排序当作日期排序。
coal = industry.loc[
    (industry['工业产品名称'] == '原煤产量当期值/万吨')
    & industry['时间'].str.startswith('2023-'),
    ['工业产品名称', '时间', '产量']
].copy()
display(coal)

# %% [markdown]
# ## 迁移：统计对象与有效月份（基础）
#
# len包含缺失行，count不包含缺失。mean默认跳过缺失；空值不等于零。
# 下列均值仅是有值月份的简单平均；不能表述为完整12个月平均或全年总量，也不在本节补零或插值。
# 此文件按年份月份倒序排列，2023年1、2月产量为空；缺失原因及原统计发布口径未核验。

# %%
print('2023年原煤记录数：', len(coal))
print('有效月份：', coal['产量'].count(), '缺失月份：', coal['产量'].isna().sum())
print(f"有效月份平均产量：{coal['产量'].mean():.2f}万吨")
display(coal['产量'].describe())

# %% [markdown]
# ## 扩展内容 3.2-M｜缺失、0与合计：sum(min_count=...)（建议选讲）
#
# 业务问题：整列都缺失时，sum的结果能否说明产量为0？
# - 下方第一段是**人工模拟缺失列**。默认sum会把全缺失合计成0；`min_count=1`要求至少一个有效值，否则仍为缺失。
# - 原煤数据12条仅10个有效月份，`sum(min_count=12)`只用于本例“要求12个有效值”的条件演示；有效数不足则不报告合计。
# - **有效数达到12也不能独自证明12个月完整**：还需核查月份唯一性、覆盖和统计口径；同月重复不能冒充另一个月。
# 观察：均值、合计与完整年度统计各需要哪些前提？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_all_missing = pd.Series([float('nan'), float('nan')])
print('全缺失默认合计：', ext_all_missing.sum())
print('至少1个有效值才合计：', ext_all_missing.sum(min_count=1))
print('原煤有效月份数：', coal['产量'].count())
print('要求12个有效值的合计（当前不足）：', coal['产量'].sum(min_count=12))

# %% [markdown]
# ## 扩展内容 3.2-N｜排序后再看首尾，以及空筛选检查（课后选做）
#
# 业务问题：tail就是最新记录吗？筛选结果为空时，下一步还能直接取第1行吗？
# - `sort_values`按字段值排序，`sort_index`按行标签排序；它们不是同一目的。
# - 本文件月份是固定宽度YYYY-MM格式，先显式转日期，再按日期排序更容易说明意图；不扩展到重采样或增长率。
# - `empty`检查是否没有行；“有行但全缺失”的表并不empty，仍要配合count/isna检查。
# 观察：排序后的前两个月为什么有记录却没有产量值？这里只读现象，不推断缺失成因。
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_coal_sorted = coal.assign(时间=pd.to_datetime(coal['时间'], format='%Y-%m')).sort_values('时间')
display(ext_coal_sorted.head(3))
ext_no_match = salesdata.loc[salesdata['商品ID'] == -1]
print('无匹配结果是否为空：', ext_no_match.empty)
if ext_no_match.empty:
    print('先检查条件与类型，暂不取首行或报告均值。')
print('原煤表是否为空：', coal.empty, '有效值数：', coal['产量'].count())
