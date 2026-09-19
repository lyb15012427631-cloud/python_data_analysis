from pathlib import Path
import json, io, contextlib, os, csv, statistics, hashlib, sys, subprocess
import numpy as np
base=Path(__file__).resolve().parents[1]
os.chdir(base)
records=[];spaces={}
for name in ['01_教师教学代码.ipynb','03_教师参考答案.ipynb','02_学生练习.ipynb']:
    obj=json.loads((base/name).read_text()); ns={}; count=0
    for cell in obj['cells']:
        if cell['cell_type']!='code': continue
        count+=1; out=io.StringIO()
        with contextlib.redirect_stdout(out): exec(compile(cell['source'],name,'exec'),ns)
        # 学生题保留空白状态；教师展示输出为本次重新运行生成。
        if not name.startswith('02'):
            cell['execution_count']=count
            cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue()}] if out.getvalue() else []
    if not name.startswith('02'): (base/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    spaces[name]=ns; records.append(f'{name}：{count}个代码单元顺序执行通过')
# 用标准库按CSV记录独立核算，避免把Notebook旧输出当依据。
with (base/'data/粮食产量年度数据.csv').open(encoding='utf-8-sig') as f: rows=list(csv.reader(f))
pairs=sorted((int(r[0].replace('年','')),float(r[1])) for r in rows[1:])
assert len(pairs)==75 and len(rows[0])==18
assert [y for y,v in pairs]==list(range(1949,2024))
selected=[(y,v) for y,v in pairs if 2014<=y<=2023]
y=[k for k,v in selected];v=[v for k,v in selected]
ns=spaces['03_教师参考答案.ipynb']
assert np.allclose(ns['yields'],v)
assert np.isclose(ns['mean_yield'],statistics.mean(v))
assert np.isclose(ns['std_yield'],statistics.pstdev(v))
diff=[v[i]-v[i-1] for i in range(1,10)]
rate=[diff[i]/v[i]*100 for i in range(9)]
assert np.allclose(ns['growth'],diff) and np.allclose(ns['growth_rate'],rate)
assert [y[i+1] for i,g in enumerate(diff) if g<0]==[2016,2018]
assert y[v.index(max(v))]==2023 and y[v.index(min(v))]==2014
assert len(diff)==9 and len(v)==10
assert np.allclose(np.array([[10,20],[30,40],[50,60]]).sum(axis=0),[90,120])
assert np.allclose(np.array([[10,20],[30,40],[50,60]]).sum(axis=1),[30,70,110])
# 乱序也必须保持配对；并列最值须返回全部年份。
idx=np.array([2,0,1]); yy=np.array([2021,2022,2023])[idx]; vv=np.array([100,120,110])[idx]
i=np.argsort(yy); assert np.array_equal(vv[i],[100,120,110])
assert np.array_equal(np.array([2021,2022,2023])[np.array([120,120,100])==120],[2021,2022])
original=next((base.parents[1]/'课程配套资源').glob('*正文数据和代码/任务实现/项目2/data/*.csv'))
assert original.read_bytes()==(base/'data/粮食产量年度数据.csv').read_bytes()
# 核对脚本与Notebook代码逐单元一致。
obj=json.loads((base/'01_教师教学代码.ipynb').read_text())
script=(base/'01_教师教学代码.py').read_text()
for c in obj['cells']:
    if c['cell_type']=='code': assert c['source'].strip() in script
result=subprocess.run([sys.executable,str(base/'01_教师教学代码.py')],cwd=base.parent,capture_output=True,text=True,check=True)
(base/'outputs/教师脚本运行输出.txt').write_text(result.stdout)
export=np.loadtxt(base/'outputs/2015至2023年增长分析.csv',delimiter=',',skiprows=1,encoding='utf-8-sig')
assert export.shape==(9,4) and np.array_equal(export[:,0],np.arange(2015,2024))
assert np.allclose(export[:,2],diff,atol=0.005)
assert np.allclose(export[:,3],rate,atol=0.00005)
above=[k for k,t in selected if t>statistics.mean(v)]
rank=sorted(selected,key=lambda r:r[1],reverse=True)[:5]
early=[t for k,t in pairs if 1949<=k<=1958]
text=f'''# 教师结果核对表

2026-09-19由本地配发CSV重新计算，标准库csv/statistics独立复核NumPy结果。单位万吨；主范围2014—2023年，共10年。仅为本教材文件的统计结果。

| 指标 | 结果 |
|---|---|
| 10年累计产量 | {sum(v):.2f} 万吨 |
| 平均年产量 | {statistics.mean(v):.3f} 万吨 |
| 总体标准差（ddof=0） | {statistics.pstdev(v):.6f} 万吨 |
| 最高 | 2023年，{max(v):.2f} 万吨 |
| 最低 | 2014年，{min(v):.2f} 万吨 |
| 高于均值的年份 | {above}，共{len(above)}年 |
| 前5年（产量降序） | {rank} |
| 下降年份 | 2016、2018 |
| 最早10年平均（1949—1958） | {statistics.mean(early):.2f} 万吨 |
| 两期平均水平增幅 | {(statistics.mean(v)/statistics.mean(early)-1)*100:.6f}% |
| 2014—2023复合年均增长率（9个间隔） | {((v[-1]/v[0])**(1/9)-1)*100:.6f}% |

| 年份 | 增长量（万吨） | 同比（%） |
|---|---|---|
'''
for year,g,r in zip(y[1:],diff,rate): text+=f'| {year} | {g:.2f} | {r:.4f} |\n'
text+='\n结论：期末高于期初，期间有下降；不能写逐年持续增长。2023年同比约1.29%，表示相对2022年产量增长，而非9年总增幅。原始来源和修订口径未重新核验，不能直接作当年现状或因果判断。\n'
(base/'06_教师结果核对表.md').write_text(text)
record=f'''# 第三周验证记录

日期：2026-09-19。Python {sys.version.split()[0]}，NumPy {np.__version__}，本机macOS。未安装依赖、未修改全局环境；源Notebook只静态阅读，未执行。

## 已执行验证

'''+ '\n'.join('- '+r for r in records)+'''
- 教师脚本从备课包上一级目录运行通过；脚本与Notebook代码一致。
- 标准库csv/statistics独立复核数据规模、连续年份、主任务均值、总体标准差、增长量和同比。
- 核对10年9项变化、2016/2018下降、极值年份、axis手算结果、乱序配对及并列极值。
- 核对导出CSV的9行4列、年份归属、数值精度；导出与日志仅在outputs内。
- 配发CSV与原件逐字节一致，原件未修改。教师Notebook输出为本次新执行结果。
- 学生模板起始单元可运行，TODO/pass仍未填写；这不表示学生任务已完成。

## 限制

以Python逐单元执行方式验证，未启动Jupyter真实内核或前端；本地缺少nbformat/nbclient，未为此安装依赖。本次不等于Windows机房实测，也未对所有NumPy旧版本做兼容性测试。开课前仍须在已配置机房环境中核对内核、中文路径、CSV编码和从头运行结果。
代码单元有顺序依赖，不宣称每个单元独立可运行。第三周实际课堂使用和掌握情况待教师反馈。
'''
(base/'验证记录.md').write_text(record)
print('\n'.join(records));print('独立数值核对、脚本、导出、源数据副本一致性检查全部通过')
print(text)
