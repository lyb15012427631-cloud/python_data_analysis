# -*- coding: utf-8 -*-
# 第二周教师演示脚本；数据均为教学模拟，单位元。
# 无第三方依赖、无文件读写、无网络操作。

# %% [markdown]
# # 第二周：让Python判断、重复和复用
# 
# 教师演示版。适用于五个统一进度班级；已学print、input、int/float/str和简单运算。
# 
# 本周目标：能判断一个数、遍历一组数、定义可复用函数，最后完成一份小型收支分析。
# 全部金额和规则均为2026-09-12编制的教学模拟数据，金额单位元，不代表真实机构数据或业务政策。
# 无外部文件、网络访问或第三方库；输出只显示在单元格中。
# 
# 按顺序运行；每个编号示例的代码单元自带所需数据和函数，也可单独重跑。运行本身不保存文件。
# 先在Jupyter中选对本课程环境的内核。每次改动代码后重新运行才能更新结果。

# %% [markdown]
# ## 第1学时：复习与条件判断
# ### 01 先复习“数据类型决定操作方式”
# 预测：字符串相加和数字相加各得到什么？input的结果是什么类型？
# 本例使用固定字符串模拟input返回的文本，方便直接运行；课堂可将第一行替换为`amount_text = input("请输入金额：")`并输入合法数字。
# `a ** b`是a的b次幂，只有b为2时才是平方。

# %%
amount_text = "120"
print(amount_text + "30")
amount = float(amount_text)
print(amount + 30)
print(type(amount_text), type(amount))
print(2 ** 3)  # 2的3次幂
print(7 // 2)  # 整除
print(7 % 2)   # 余数


# %% [markdown]
# ### 02 比较得到bool：True或False
# `=`用于赋值，`==`用于比较是否相等。还可以使用`!=、>、>=、<、<=`。
# 跟练：将spending改为100，再预测每个结果。

# %%
spending = 120
print(spending > 100)
print(spending >= 100)
print(spending == 100)
print(spending != 100)
print(type(spending > 100))


# %% [markdown]
# ### 03 if / else：满足条件才执行
# 冒号后换行，分支内统一缩进4个空格。最后一行不缩进，所以不管哪个分支都会执行。
# 跟练：分别把spending改为80、100、120，说明“超过预算”和“达到预算”的区别。

# %%
spending = 120
budget = 100
if spending > budget:
    print("超过预算")
else:
    print("未超过预算")
print("本次检查结束")


# %% [markdown]
# ### 04 if / elif / else：从上向下，命中后停止
# 教学规则：金额必须非负；0至不足100为小额，100至不足500为中额，500及以上为大额。
# 先排除负数，再按阈值从小到大判断。elif表示“前面的分支都没进入，再判断”。
# 跟练：测试-1、0、99、100、499、500。

# %%
amount = 500
if amount < 0:
    print("金额不能为负数")
elif amount < 100:
    print("小额")
elif amount < 500:
    print("中额")
else:
    print("大额")


# %% [markdown]
# ### 05 and / or / not：组合条件
# and要求两边都满足；or至少满足一边；not把真假反过来。这里使用Python基础条件表达式。
# 不要把本例的and/or直接套到未来的Pandas整列筛选，届时会单独学习对应语法。

# %%
amount = 120
print(amount >= 100 and amount < 500)
print(amount < 0 or amount > 1000)
print(not (amount < 0))
if amount >= 100 and amount < 500:
    print("金额落在中额区间")


# %% [markdown]
# ## 第2学时：列表与for循环
# ### 06 列表：把一组数据放在一起
# 方括号创建列表，逗号分隔元素。第一个元素的位置是0，最后一个可用-1。
# `values[1:3]`取位置1和2，不包含3。`.append()`是列表的方法，在原列表末尾添加元素。
# 本周只需掌握一维列表；字典、嵌套列表等按后续库学习需要再补充。

# %%
expenses = [35, 120, 0, 68, 250]
print(expenses)
print(expenses[0])
print(expenses[-1])
print(expenses[1:3])
expenses.append(50)
print(expenses)


# %% [markdown]
# ### 07 for：逐个取值，执行同一段代码
# expense每一轮是一个金额，不是位置编号。先让学生口述前两轮变量的值。
# 跟练：给每笔支出加上“元”的单位。

# %%
expenses = [35, 120, 0, 68, 250]
for expense in expenses:
    print("本笔支出：", expense)
print("全部读取完成")


# %% [markdown]
# ### 08 range：重复指定次数
# `range(1, 4)`产生1、2、3，不含4。`range(3)`产生0、1、2。
# range本身是一个可迭代的range对象；用list转换后能直观看到这些数。

# %%
print(list(range(3)))
print(list(range(1, 4)))
total_saved = 0
for month in range(1, 4):
    total_saved = total_saved + 100
    print("第", month, "月，累计存入", total_saved, "元")


# %% [markdown]
# ### 09 累加器与计数器
# total累计金额，large_count统计满足条件的笔数。都在循环前初始化为0。
# `total += expense`等价于`total = total + expense`，初学先使用完整写法。
# 跟练：把阈值改为200，并先手算应有几笔。

# %%
expenses = [35, 120, 0, 68, 250]
total = 0
large_count = 0
for expense in expenses:
    total = total + expense
    if expense >= 100:
        large_count = large_count + 1
print("总支出：", total, "元")
print("至少100元的笔数：", large_count)


# %% [markdown]
# ### 10 条件判断+循环：筛选数据
# 本例约定：非负数表示有效支出，负数是待核对记录。真实业务中的负数也可能是退款，不能一概删除。
# 先创建空列表，再把符合规则的数放进去。此处使用普通for循环，不引入列表推导式。

# %%
raw_expenses = [35, -20, 120, 0, 68, 250]
valid_expenses = []
invalid_expenses = []
for expense in raw_expenses:
    if expense >= 0:
        valid_expenses.append(expense)
    else:
        invalid_expenses.append(expense)
print("有效支出：", valid_expenses)
print("待核对记录：", invalid_expenses)


# %% [markdown]
# ## 第3学时：while与函数
# ### 11 while：不知道要重复几次时，根据条件继续
# 教学情景：初始为0，每次存入100元，直到至少350元。while在每轮开始前判断。
# 目标是至少350，最终会到400；不是金额计算错误，而是每次存100。
# 循环必须更新余额，否则条件一直成立会无限循环。遇到无限循环，先点Jupyter停止/中断内核。

# %%
balance = 0
target = 350
months = 0
while balance < target:
    balance = balance + 100
    months = months + 1
    print("第", months, "个月：", balance)
print("达到目标，共需要", months, "个月")


# %% [markdown]
# ### 12 def：把重复操作起一个名字
# amount和budget叫形参；调用时传入的80和100等叫实参。
# def只定义，不会自动执行函数体；函数调用时才执行。return把结果交回调用位置，并结束本次调用。
# 跟练：把返回结果保存在变量中，再打印。

# %%
def check_budget(amount, budget):
    if amount > budget:
        return "超预算"
    else:
        return "未超预算"

result = check_budget(80, 100)
print(result)
print(check_budget(120, 100))
print(check_budget(100, 100))


# %% [markdown]
# ### 13 print与return：显示出来不等于交回结果
# 下面两个函数都会被调用，但show_double没有return，其返回值是None。
# 函数内部的result是局部变量。想在外部继续计算，应return并接收结果，不依赖函数内部名字。

# %%
def show_double(number):
    print(number * 2)

def calculate_double(number):
    result = number * 2
    return result

shown = show_double(10)
calculated = calculate_double(10)
print("只有print的函数返回：", shown)
print("使用return的函数返回：", calculated)
print("返回后继续加5：", calculated + 5)


# %% [markdown]
# ### 14 把分档规则写成函数
# 本例输入约定为数值，字符串输入需先转换；不在本周增加异常处理语法。
# 每次调用互相独立；return提前结束本次调用，不会结束外层for循环。

# %%
def spending_level(amount):
    if amount < 0:
        return "待核对"
    elif amount < 100:
        return "小额"
    elif amount < 500:
        return "中额"
    else:
        return "大额"

amounts = [-1, 0, 99, 100, 499, 500]
for amount in amounts:
    print(amount, spending_level(amount))


# %% [markdown]
# ## 第4学时：常用函数与综合应用
# ### 15 len / sum / min / max / round / abs
# len计数，sum求和，min/max找最值，round用于本例结果展示，abs取绝对值。
# 空列表的len和sum都是0；min/max不能直接处理空列表，平均值也不能除以0。
# round不保证打印出固定两位小数；显示固定两位可用f-string的`:.2f`。
# 浮点运算可能有表示误差；这里是基础教学，不是生产会计结算程序。

# %%
expenses = [35, 120, 0, 68, 250]
print("笔数：", len(expenses))
print("总支出：", sum(expenses))
print("最少：", min(expenses))
print("最多：", max(expenses))
average = sum(expenses) / len(expenses)
print("平均每笔支出：", round(average, 2))
print(f"固定两位小数显示：{average:.2f}")
print("离预算500元的差额大小：", abs(sum(expenses) - 500))


# %% [markdown]
# ### 16 sorted：得到排序后的新列表
# `reverse=True`表示降序；不写时默认升序。
# 排序能找金额高低，但会失去原先时间顺序，不能拿排序后的金额计算相邻日涨跌。

# %%
expenses = [35, 120, 0, 68, 250]
print("升序：", sorted(expenses))
print("降序：", sorted(expenses, reverse=True))
print("原列表：", expenses)


# %% [markdown]
# ### 17 平均值函数：先判断有没有数据
# 本函数的输入是数值列表。空列表返回None，表示没有可计算的平均值，而不是平均值为0。
# 先讲正常列表，再解释空列表保护；不用学生死记None，重点是先检查分母。

# %%
def average_amount(values):
    if len(values) == 0:
        return None
    return sum(values) / len(values)

print(average_amount([35, 120, 0, 68, 250]))
print(average_amount([]))


# %% [markdown]
# ### 18 综合演示：一组支出数据能回答什么？
# 任务：保留非负支出；统计有效、待核对笔数；求总额、均值、极值；筛选至少100元的记录；比较预算500元。
# 原始列表保持不变。所有统计都针对有效记录，包含0元记录，不把它误认为缺失值。
# 先拆任务，学生尝试后再展示完整代码。本例函数自身先做数值列表筛选。

# %%
def show_expense_report(raw_values, budget):
    valid_values = []
    invalid_count = 0
    large_values = []
    for value in raw_values:
        if value < 0:
            invalid_count = invalid_count + 1
        else:
            valid_values.append(value)
            if value >= 100:
                large_values.append(value)

    print("有效笔数：", len(valid_values))
    print("待核对笔数：", invalid_count)
    if len(valid_values) == 0:
        print("没有有效支出，暂不计算均值、极值或预算结论")
        return

    total = sum(valid_values)
    print("总支出：", total)
    print("平均每笔支出：", round(total / len(valid_values), 2))
    print("最小与最大：", min(valid_values), max(valid_values))
    print("至少100元的记录：", large_values)
    print("金额降序：", sorted(valid_values, reverse=True))
    if total > budget:
        print("超预算：", total - budget, "元")
    else:
        print("预算内剩余：", budget - total, "元")

raw_expenses = [35, -20, 120, 0, 68, 250]
show_expense_report(raw_expenses, 500)
print("原始数据：", raw_expenses)


# %% [markdown]
# ## 拓展选做：不作为本周基础达标门槛
# ### 19 enumerate：同时获得序号和值
# for后有两个变量，分别接收序号和值，称为解包。start=1使显示序号从1开始；不改变列表位置从0开始的规则。

# %%
expenses = [35, 120, 68]
for number, expense in enumerate(expenses, start=1):
    print("第", number, "笔：", expense, "元")


# %% [markdown]
# ### 20 zip：让两组数据一一对应
# 仅在数量相等、顺序确实对应时适合这样配对。zip默认以较短的一组为准停止，先检查长度可避免漏掉记录。

# %%
categories = ["餐饮", "交通", "学习"]
expenses = [35, 12, 80]
if len(categories) != len(expenses):
    print("项目和金额数量不一致，请先核对")
else:
    for category, expense in zip(categories, expenses):
        print(category, expense)


# %% [markdown]
# ### 21 break与continue：结束循环与跳过当前轮
# 本例约定：遇到None结束读取；遇到负数跳过。None是一个特殊值，不是字符串"None"。
# break结束所在循环；continue只跳过本轮后续代码。先保证学生会普通for，再选讲本例。

# %%
values = [35, -20, 120, None, 999]
for value in values:
    if value is None:
        break
    if value < 0:
        continue
    print("处理：", value)


# %% [markdown]
# ### 22 默认参数与关键字参数
# 调用时不提供threshold就用默认值100；也可以写threshold=200覆盖默认值。
# 这为以后理解库函数的参数做准备。

# %%
def count_large(values, threshold=100):
    count = 0
    for value in values:
        if value >= threshold:
            count = count + 1
    return count

print(count_large([35, 120, 250]))
print(count_large([35, 120, 250], threshold=200))


# %% [markdown]
# ## 下课自查
# 1. `=`和`==`有什么区别？金额为100时进入哪一档？
# 2. 累加器为何在循环外初始化？range(1, 4)有几轮？
# 3. while循环的条件由哪一句改变？
# 4. 为什么一个只print的函数不能直接提供数值结果继续计算？
# 5. 平均值的分母是什么？没有有效数据时应该输出0还是“暂无数据”？
# 
# 完成学生练习后再阅读教师答案。下一阶段库学习的安排由教师确认，不因本Notebook存在而认定本周已授完。
