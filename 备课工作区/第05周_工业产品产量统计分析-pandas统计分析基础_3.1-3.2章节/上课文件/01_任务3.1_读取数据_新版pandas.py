# %% [markdown]
# # 任务3.1 读取工业产品产量数据｜新版 pandas 课堂版
#
# 适用：第五周第1课时及第2课时开头；知识准备3.1.1—3.1.3。
# 目标：认识 Series/DataFrame，正确读取 CSV、预览数据，理解分隔符、表头、编码，完成 CSV 导出回读；Excel 为教师演示与条件允许时跟练。
#
# 原题名沿用教材，实际基础示例是**工业制品销售数据**，不能称为工业产量。数据为教材提供的1351行销售记录，来源真实性未独立核实。工业产量的迁移在任务3.2末尾。
#
# 依赖：Python、pandas；Excel 另需 openpyxl。顺序：从上向下；输出仅在 outputs。3.1.4 SQL 已移出正课，见独立的《选做内容.ipynb》。验证见《验证记录.md》。

# %% [markdown]
# ## 本次新增：扩展内容导航（2026-10-25）
#
# 原教学单元按原顺序完整保留；下列扩展就地插入对应示例后，均可按学情跳过。160分钟原教学安排不变，建议每节只选1—2项，其余课后查阅。学生必做题与教师答案保持原样。
#
# - **3.1-A** 只读需要的列与少量行：usecols、nrows（建议选讲）
# - **3.1-B** 编号按字符串读取：dtype与前导零（建议选讲）
# - **3.1-C** 指定缺失标记：na_values与默认规则（课后选做）
# - **3.1-D** 导出指定字段与行号的取舍（建议选讲）
# - **3.1-E** Excel工作表选择：sheet_name（课后选做）
# - **3.1-F** 读入时解析日期：parse_dates、date_format（课后选做）
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
# ## 补充导入：从一列到一张表（基础）
#
# 以下3行是**人工模拟数据**。字典的键成为列名，列表提供各行；一列是 Series，双层方括号选出的是 DataFrame。
# 先预测两种选择的 shape，再运行。NumPy也能存文字或对象；pandas的优势是带标签的表格操作，不能说NumPy“无法存混合数据”。

# %%
mini = pd.DataFrame({'产品': ['甲', '乙', '丙'], '数量/个': [3, 5, 2]})
display(mini)
print(type(mini['数量/个']).__name__, mini['数量/个'].shape)
print(type(mini[['数量/个']]).__name__, mini[['数量/个']].shape)

# %% [markdown]
# ## 原示例 1｜read_table：明确分隔符
#
# 仍支持，不是弃用接口。先看前3行，不一次打印整张表。

# %%
salesdata = pd.read_table(DATA / 'salesdata.csv', sep=',', encoding='utf-8')
print('记录数：', len(salesdata))
display(salesdata.head(3))

# %% [markdown]
# ## 原示例 2｜read_csv：本周首选
#
# CSV通常用read_csv，默认逗号分隔。形状为（行数，列数），列名可以检验文件是否读对。

# %%
salesdata_csv = pd.read_csv(DATA / 'salesdata.csv', encoding='utf-8')
print(salesdata_csv.shape)
print(salesdata_csv.columns.tolist())
assert salesdata.equals(salesdata_csv)

# %% [markdown]
# ## 扩展内容 3.1-A｜只读需要的列与少量行：usecols、nrows（建议选讲）
#
# 业务问题：只想先检查产品与价格，是否必须把全部字段都展示出来？
# - `usecols`指定列名，`nrows`限制读取的数据行数（不含表头），适合初次检查格式。
# - 文件中列的顺序不一定按`usecols`列表重排；需要固定顺序时，再用双括号选列。
# - **前5行只是预览，不是随机抽样，不能据此代表全体销售记录。**正式统计仍用完整基线。
# 观察：把`nrows=5`改成2，shape中的哪个数会变化？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_preview = pd.read_csv(DATA / 'salesdata.csv', encoding='utf-8',
                          usecols=['商品ID', '销售价格/元'], nrows=5)
ext_preview = ext_preview[['商品ID', '销售价格/元']]
display(ext_preview)
print('仅供格式检查：', ext_preview.shape)

# %% [markdown]
# ## 扩展内容 3.1-B｜编号按字符串读取：dtype与前导零（建议选讲）
#
# 业务问题：商品编号“0019”能否当作数字19？编号用于识别，通常不需要加减或平均。
# - 可在读取时用`dtype={'商品ID': 'string'}`明确为文本；此时筛选值也应写成字符串。
# - 下方前两行读取教材数据，后半段是**人工模拟CSV文本**，`StringIO`由教师提供，用于对比前导零。
# - 不在读取时保留的前导零，之后直接`astype('string')`不能自动恢复。原示例的整数读取路线仍保留。
# 先预测：字符串路线查询商品ID时，应写`10000019`还是`'10000019'`？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_text_ids = pd.read_csv(DATA / 'salesdata.csv', encoding='utf-8', dtype={'商品ID': 'string'})
display(ext_text_ids.loc[ext_text_ids['商品ID'] == '10000019'].head())
from io import StringIO
ext_id_csv = '''客户编号,数量
0019,3
0020,5
'''
ext_id_auto = pd.read_csv(StringIO(ext_id_csv))
ext_id_text = pd.read_csv(StringIO(ext_id_csv), dtype={'客户编号': 'string'})
print('自动推断：', ext_id_auto['客户编号'].tolist())
print('明确文本：', ext_id_text['客户编号'].tolist())

# %% [markdown]
# ## 原示例 3｜错误分隔符对照
#
# 故意使用分号会把整行读成一列；没报错也不等于读取正确。

# %%
wrong_sep = pd.read_csv(DATA / 'salesdata.csv', sep=';', encoding='utf-8')
print('错误分隔符下的形状：', wrong_sep.shape)
display(wrong_sep.head(2))

# %% [markdown]
# ## 原示例 4｜header=None对照
#
# 本文件有表头。header=None会把原表头当成数据，所以多出1行，列名变成数字。

# %%
wrong_header = pd.read_csv(DATA / 'salesdata.csv', header=None, encoding='utf-8')
print(wrong_header.shape)
display(wrong_header.head(2))

# %% [markdown]
# ## 扩展内容 3.1-C｜指定缺失标记：na_values与默认规则（课后选做）
#
# 业务问题：文件里的“未报”与数值0是不是同一件事？下方是**人工模拟产品数据**，不用于解释教材缺失成因。
# - `na_values=['未报']`可把约定标记读成缺失；pandas默认还会识别空字段、NA等常见标记。
# - `keep_default_na=False`关闭默认标记，只保留自己指定的规则；若“NA”恰是合法代码，读取规则需另行设计。
# - 缺失标记必须有数据字典或业务依据，不能凭感觉把文字全部转成0。
# 观察：两种规则下，代码列的`NA`是否都成为缺失？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
from io import StringIO
ext_na_csv = '''产品代码,数量
NA,0
B,未报
C,12
'''
ext_na_default = pd.read_csv(StringIO(ext_na_csv), na_values=['未报'])
ext_na_explicit = pd.read_csv(StringIO(ext_na_csv), keep_default_na=False, na_values=['未报'])
display(ext_na_default)
display(ext_na_explicit)
print('显式规则下数量缺失数：', ext_na_explicit['数量'].isna().sum())

# %% [markdown]
# ## 原示例 5｜编码错误演示
#
# 源文件是UTF-8。只捕获预期编码错误以保证课堂可以继续；不能靠errors="ignore"悄悄丢字。若某文件解码成功仍应检查中文字段是否正确。try/except由教师解释，不列为考查点。

# %%
try:
    wrong_encoding = pd.read_csv(DATA / 'salesdata.csv', encoding='gbk')
except UnicodeDecodeError:
    print('预期演示：GBK不能正确解码本UTF-8文件，应改回utf-8。')
else:
    print('未报解码错仍需核查列名：', wrong_encoding.columns.tolist())

# %% [markdown]
# ## 原示例 6｜CSV导出与回读
#
# 输出只写本包。index=False不写额外行号；utf-8-sig方便Windows Excel识别中文。教材分号分隔保留，回读也要指定分号。

# %%
salesdata.to_csv(OUTPUT / 'salesdataInfo.csv', sep=';', index=False, encoding='utf-8-sig')
roundtrip_csv = pd.read_csv(OUTPUT / 'salesdataInfo.csv', sep=';', encoding='utf-8-sig')
assert salesdata.equals(roundtrip_csv)
print('导出回读一致：', roundtrip_csv.shape)

# %% [markdown]
# ## 扩展内容 3.1-D｜导出指定字段与行号的取舍（建议选讲）
#
# 业务问题：给同学分享两列预览表，怎样避免把临时行号也当作业务字段？
# - `columns=`控制导出字段及顺序；`index=False`适合当前没有业务含义的默认行号。
# - 如果索引本身是有意义的客户编号，就应先明确保留策略，不能机械地丢掉。
# - 这里输出到内存字符串，不额外写文件。原示例中的文件导出与回读流程继续适用。
# 观察：预览文本的第一行是否出现无名列或0、1、2等额外行号？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_export_text = salesdata.head(3).to_csv(
    index=False, columns=['商品ID', '销售量/个'])
print(ext_export_text)
from io import StringIO
ext_export_back = pd.read_csv(StringIO(ext_export_text))
print('回读字段：', ext_export_back.columns.tolist())

# %% [markdown]
# ## 原示例 7｜读取Excel（依赖具备时演示）
#
# Excel文件的订单时间是日期单元格，读入可能直接成为datetime；CSV读入通常还是字符串。检查类型差异，不要求两个原始dtype完全相同。没有openpyxl时只跳过Excel，不影响CSV正课。

# %%
import importlib.util
has_excel = importlib.util.find_spec('openpyxl') is not None
if has_excel:
    salesdata_excel = pd.read_excel(DATA / 'salesdata.xlsx', engine='openpyxl')
    print(salesdata_excel.shape)
    print(salesdata_excel.dtypes)
    display(salesdata_excel.head(3))
else:
    print('Excel未运行：缺少openpyxl，请教师课前检查；继续CSV路线。')

# %% [markdown]
# ## 扩展内容 3.1-E｜Excel工作表选择：sheet_name（课后选做）
#
# 业务问题：一个工作簿有多个Sheet时，读到的是哪张表？
# - `sheet_name=0`读第一张表；`sheet_name='表名'`按名称读取；`sheet_name=None`会返回“表名→DataFrame”的字典。
# - 当前教材文件很小，可演示全部Sheet。大型工作簿先核查表名，再只读需要的表，避免一次读完。
# - 缺少openpyxl则沿用原代码跳过；扩展不安装依赖。
# 观察：`ext_sheets`为什么不能直接当成一张DataFrame调用shape？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
if has_excel:
    ext_sheets = pd.read_excel(DATA / 'salesdata.xlsx', sheet_name=None, engine='openpyxl')
    print('工作表名：', list(ext_sheets))
    for ext_sheet_name, ext_sheet_table in ext_sheets.items():
        print(ext_sheet_name, ext_sheet_table.shape)
else:
    print('本扩展未运行：缺少openpyxl。')

# %% [markdown]
# ## 原示例 8｜Excel导出与回读
#
# 沿用CSV数据写Excel，index=False避免多出Unnamed列；结果输出不是精排报表。只有Excel依赖就绪才执行。

# %%
if has_excel:
    salesdata.to_excel(OUTPUT / 'salesdata.xlsx', index=False, engine='openpyxl')
    roundtrip_excel = pd.read_excel(OUTPUT / 'salesdata.xlsx', engine='openpyxl')
    assert salesdata.equals(roundtrip_excel)
    print('Excel导出回读一致：', roundtrip_excel.shape)
else:
    print('Excel导出未运行：缺少openpyxl。')

# %% [markdown]
# ## 扩展内容 3.1-F｜读入时解析日期：parse_dates、date_format（课后选做）
#
# 业务问题：已知日期格式时，能否在读入CSV时直接形成日期列？
# - `parse_dates=['订单时间']`指定日期列，`date_format`指定已知格式，减少后续重复转换。
# - 读取后必须核查dtype和样本；解析不成功时可能仍得到文本列，不能只看“读入没报错”。
# - 此写法需要pandas 2.0及以上；旧机房可保留原路线，再用`pd.to_datetime(..., format=...)`转换。这里只预告转换，时间序列分析留到后续。
# 观察：与原CSV基线相比，哪一列的数据类型发生变化？
#
# 本单元为扩展，不计入本周必做；依次运行本文件前置单元。扩展变量使用`ext_`前缀，不改变原教学基线。

# %%
ext_dates_read = pd.read_csv(DATA / 'salesdata.csv', encoding='utf-8',
                             parse_dates=['订单时间'], date_format='%Y/%m/%d %H:%M')
print(ext_dates_read['订单时间'].dtype)
display(ext_dates_read[['订单时间']].head(3))

# %% [markdown]
# 正课到此结束。完成学生练习第1题。原示例9—13（3.1.4数据库）仅保留在独立《选做内容.ipynb》，不计入160分钟。
