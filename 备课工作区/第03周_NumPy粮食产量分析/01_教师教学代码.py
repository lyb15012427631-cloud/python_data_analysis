# 01 启动与先修检查
from pathlib import Path
import numpy as np
# Notebook请在本备课包文件夹启动；脚本以自身所在目录为基准。
BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA = BASE / "data" / "粮食产量年度数据.csv"
print("NumPy版本：", np.__version__)
print("数据文件存在：", DATA.exists())

# 02 从列表到数组
values = [100, 120, 110]
a = np.array(values, dtype=float)
print("列表乘2：", values * 2)
print("数组乘2：", a * 2)
print("shape、ndim、size、dtype：", a.shape, a.ndim, a.size, a.dtype)
print("平均产量：", np.mean(a))

# 03 创建二维数组与形状
region = np.array([[10, 20], [30, 40], [50, 60]])
print(region)
print(region.shape, region.ndim, region.size)
print(np.arange(2014, 2024))
print(np.arange(6).reshape(3, 2))
print(np.zeros((2, 3)))
print(np.ones((2, 3)))

# 04 索引、切片与配对
demo_years = np.array([2021, 2022, 2023])
demo_yields = np.array([100.0, 120.0, 110.0])
table = np.column_stack((demo_years, demo_yields))
print(table)
print("第一行第二列：", table[0, 1])
print("所有产量：", table[:, 1])
print("前两年：", table[:2, :])
print("最后一年：", demo_years[-1], demo_yields[-1])
print("转置后形状：", table.T.shape)

# 05 axis：哪个维度被汇总
region = np.array([[10, 20], [30, 40], [50, 60]])
print("各地区三年累计：", region.sum(axis=0))  # [90, 120]
print("每年两地合计：", region.sum(axis=1))   # [30, 70, 110]
print("每地区三年平均：", region.mean(axis=0))

# 06 比较与布尔筛选
demo_years = np.array([2021, 2022, 2023])
demo_yields = np.array([100.0, 120.0, 110.0])
above = demo_yields > demo_yields.mean()
print("条件：", above)
print("高于均值年份：", demo_years[above])
print("产量：", demo_yields[above])
print("100以上且不足120：", demo_yields[(demo_yields > 100) & (demo_yields < 120)])

# 07 读取CSV并整理时间
# 文件有中文年份和表头，先按字符串只读前两列。
raw = np.loadtxt(DATA, delimiter=",", skiprows=1, usecols=(0, 1),
                 dtype=str, encoding="utf-8-sig")
year_list = []
for text in raw[:, 0]:
    year_list.append(int(text.replace("年", "")))
years_all = np.array(year_list)
yields_all = raw[:, 1].astype(float)
# 对年份排序后，产量必须用同一组位置重排，保持一一对应。
order = np.argsort(years_all)
years_all = years_all[order]
yields_all = yields_all[order]
print("形状：", raw.shape)
print("时间范围：", years_all[0], years_all[-1])
print("产量均为有限数：", np.all(np.isfinite(yields_all)))

# 08 选定本周统计范围
# 明确筛选年份，不依赖文件前10行恰好是最近10年。
mask = (years_all >= 2014) & (years_all <= 2023)
years = years_all[mask]
yields = yields_all[mask]
print("年份：", years)
print("产量（万吨）：", yields)

# 09 描述统计与极值
mean_yield = np.mean(yields)
std_yield = np.std(yields, ddof=0)  # 描述选定10年的总体离散程度，分母为10。
print(f"2014—2023年累计产量：{np.sum(yields):.2f} 万吨")
print(f"平均年产量：{mean_yield:.2f} 万吨")
print(f"总体标准差：{std_yield:.2f} 万吨")
print("最高年份：", years[yields == np.max(yields)], "产量：", np.max(yields))
print("最低年份：", years[yields == np.min(yields)], "产量：", np.min(yields))
print("首个最大值的位置：", np.argmax(yields))

# 10 高于均值与排名
above = yields > mean_yield
print("高于均值年份：", years[above])
print("数量：", np.sum(above))
rank = np.argsort(yields)[::-1]
print("前5年份：", years[rank[:5]])
print("对应产量（万吨）：", yields[rank[:5]])

# 11 相邻年增长分析
# 时间已经升序；今年在后，上年在前，分母必须是上年产量。
growth = yields[1:] - yields[:-1]
growth_rate = growth / yields[:-1] * 100
growth_years = years[1:]
print("对应年份：", growth_years)
print("年增长量（万吨）：", np.round(growth, 2))
print("同比增长率（%）：", np.round(growth_rate, 2))
print("下降年份：", growth_years[growth < 0])

# 12 规范导出分析结果
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
result = np.column_stack((growth_years, yields[1:], growth, growth_rate))
np.savetxt(OUT / "2015至2023年增长分析.csv", result, delimiter=",",
           header="年份,粮食产量_万吨,年增长量_万吨,同比增长率_百分数",
           comments="", fmt=["%d", "%.2f", "%.2f", "%.4f"], encoding="utf-8-sig")
print("结果保存到：", OUT / "2015至2023年增长分析.csv")

# 拓展A 随机数与矩阵概念
rng = np.random.default_rng(42)
area_sim = np.round(rng.uniform(110000, 120000, size=10), 2)
print("模拟面积（千公顷）：", area_sim)
left = np.array([[1, 2], [3, 4]])
right = np.array([[2, 0], [0, 2]])
print("逐元素乘法：", left * right)
print("矩阵乘法：", left @ right)

# 拓展B 全历史与时期比较
early = yields_all[(years_all >= 1949) & (years_all <= 1958)]
late = yields_all[(years_all >= 2014) & (years_all <= 2023)]
print("最早10年平均年产量（万吨）：", early.mean())
print("最新10年平均年产量（万吨）：", late.mean())
print("两期平均水平增幅（%）：", (late.mean() / early.mean() - 1) * 100)
print("全75年累计产量（万吨）：", yields_all.sum())
print("全75年平均年产量（万吨）：", yields_all.mean())
# 2014到2023是9个年度间隔，不能用10作指数分母。
cagr = ((yields[-1] / yields[0]) ** (1 / (years[-1] - years[0])) - 1) * 100
print("2014—2023年复合年均增长率（%）：", cagr)
