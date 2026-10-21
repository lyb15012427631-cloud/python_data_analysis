"""在临时工作副本执行2.3，不运行课本原件。--更新输出写回新备课Notebook及5个演示文件。"""
from pathlib import Path
import argparse
import json
import math
import re
import shutil
import statistics
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
from jupyter_client import AsyncKernelManager

TASK_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK = TASK_DIR / '任务2.3 对粮食产量进行统计分析_新版NumPy.ipynb'
EXPECTED_FILES = {'save_arr.npy', 'savez_arr.npz', 'arr.txt', 'arr_整数格式对照.txt', '模拟产量_含缺失.csv'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--更新输出', action='store_true', help='验证通过后更新备课副本输出；不影响课本原件')
    args = parser.parse_args()
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    numbered = [c.metadata.get('original_cell_number') for c in notebook.cells if c.cell_type == 'code' and 'original_cell_number' in c.metadata]
    assert numbered == list(range(1, 44)), numbered
    code_count = sum(c.cell_type == 'code' for c in notebook.cells)
    assert code_count == 59, code_count
    for i, cell in enumerate(notebook.cells, 1):
        if cell.cell_type == 'code':
            compile(cell.source, f'cell_{i}', 'exec')
            cell.outputs = []
            cell.execution_count = None
    # 校验单元仅用于测试，不加入交付的课堂代码。
    checks = nbformat.v4.new_code_cell('''
import math, statistics, json, sys
from pathlib import Path
# 标准库独立构造预期，不把原课本输出当作正确性证据。
expected_grid = [[r * 10 + c for c in range(10)] for r in range(10)]
assert np.array_equal(np.load(OUTPUT_DIR / 'save_arr.npy', allow_pickle=False), expected_grid)
with np.load(OUTPUT_DIR / 'savez_arr.npz', allow_pickle=False) as z:
    assert set(z.files) == {'arr1', 'arr2'}
    assert np.array_equal(z['arr1'], [[1, 2, 3], [4, 5, 6]])
    assert all(math.isclose(float(x), i / 10, abs_tol=1e-14) for i, x in enumerate(z['arr2']))
expected_text = [[(r * 6 + c) / 2 for c in range(6)] for r in range(4)]
assert np.array_equal(loaded_data, expected_text)
raw_lines = (OUTPUT_DIR / 'arr.txt').read_text(encoding='utf-8').splitlines()
actual_text = [[float(v) for v in line.split(',')] for line in raw_lines]
assert actual_text == expected_text
lost_lines = (OUTPUT_DIR / 'arr_整数格式对照.txt').read_text(encoding='utf-8').splitlines()
assert [[int(v) for v in line.split(',')] for line in lost_lines] == [[int(v) for v in row] for row in expected_text]
assert np.isnan(missing_table[1, 1]) and np.count_nonzero(np.isnan(missing_table[:, 1])) == 1
assert math.isclose(float(np.nanmean(missing_table[:, 1])), statistics.mean([10.5, 12.0]))
assert years_sorted.tolist() == [2021, 2022, 2023]
assert yields_sorted.tolist() == [10.0, 11.0, 12.0]
assert order.tolist() == [1, 2, 0]
assert labels[asc].tolist() == ['乙', '丁', '甲', '丙']
assert labels[desc].tolist() == ['甲', '丙', '乙', '丁']
assert list(zip(region[lex_order].tolist(), year[lex_order].tolist())) == [(1, 2021), (1, 2023), (2, 2021), (2, 2022)]
expected_first = list(dict.fromkeys(names.tolist()))
assert names[np.sort(first)].tolist() == expected_first
assert dict(zip(values.tolist(), counts.tolist())) == {name: names.tolist().count(name) for name in set(names.tolist())}
assert column_mean.tolist() == [[12.0, 22.0]] and column_mean.shape == (1, 2)
assert math.isclose(float(np.var(sample, ddof=0)), statistics.pvariance([10, 12, 14]))
assert math.isclose(float(np.var(sample, ddof=1)), statistics.variance([10, 12, 14]))
assert (int(max_row), int(max_col)) == (3, 4)
assert np.argwhere(ties == np.max(ties)).tolist() == [[0, 0], [1, 1]]
from itertools import accumulate
assert np.cumsum(arr).tolist() == list(accumulate(range(2, 10)))
assert np.cumprod(arr, dtype=np.int64).tolist() == list(accumulate(range(2, 10), lambda a, b: a * b))
assert np.cumprod(small, dtype=np.int8).tolist() == [100, -56, -112]
assert np.cumprod(small, dtype=np.int64).tolist() == [100, 200, 400]
assert np.cumprod(big, dtype=object).tolist() == [10**10, 10**20]
assert math.isclose(float((np.cumprod(factors)[-1] - 1) * 100), 6.59, abs_tol=1e-12)
print(json.dumps({'python': sys.version.split()[0], 'numpy': np.__version__, 'independent_checks': 'passed'}, ensure_ascii=False))
''')
    with tempfile.TemporaryDirectory(prefix='week04-task23-') as scratch:
        work = Path(scratch) / 'work'; work.mkdir()
        nbformat.write(notebook, work / NOTEBOOK.name)
        kernel = Path(scratch) / 'kernels' / 'week04-verification'; kernel.mkdir(parents=True)
        (kernel / 'kernel.json').write_text(json.dumps({'argv': [sys.executable, '-B', '-m', 'ipykernel_launcher', '-f', '{connection_file}'], 'display_name': 'Week04 verification', 'language': 'python'}))
        manager = KernelSpecManager(kernel_dirs=[str(kernel.parent)])
        notebook.cells.append(checks)
        km = AsyncKernelManager(kernel_name='week04-verification', kernel_spec_manager=manager)
        client = NotebookClient(notebook, timeout=120, km=km, resources={'metadata': {'path': str(work)}})
        client.execute(cleanup_kc=True)
        check_cell = notebook.cells.pop()
        check_text = ''.join(o.get('text', '') for o in check_cell.outputs if o.output_type == 'stream')
        environment = json.loads(check_text.strip())
        warnings_found = []
        for cell in notebook.cells:
            for output in cell.get('outputs', []):
                assert output.output_type != 'error', output
                if output.output_type == 'stream' and output.name == 'stderr':
                    warnings_found.append(output.text)
        assert not warnings_found, warnings_found
        # 对真正原示例运行输出做独立复核，避免只验证重算的NumPy表达式。
        numeric_expect = {29: sum(range(20)), 32: statistics.mean(range(20)), 35: statistics.pstdev(range(20)), 36: statistics.pvariance(range(20)), 37: 0, 38: 19, 39: 0, 40: 19}
        for cell in notebook.cells:
            idx = cell.metadata.get('original_cell_number')
            if idx in numeric_expect:
                printed = ''.join(o.get('text', '') for o in cell.outputs)
                actual = float(printed.split('：')[-1].strip())
                assert math.isclose(actual, numeric_expect[idx], rel_tol=1e-12, abs_tol=1e-12), (idx, actual, numeric_expect[idx])
        axis_expect = {30: [30, 34, 38, 42, 46], 31: [10, 35, 60, 85], 33: [7.5, 8.5, 9.5, 10.5, 11.5], 34: [2.0, 7.0, 12.0, 17.0]}
        for cell in notebook.cells:
            idx = cell.metadata.get('original_cell_number')
            if idx in axis_expect:
                printed = ''.join(o.get('text', '') for o in cell.outputs)
                actual = [float(x) for x in re.findall(r'-?\d+(?:\.\d*)?', printed.split('：')[-1])]
                assert actual == axis_expect[idx], (idx, actual)
        produced = {p.name for p in (work / 'outputs').iterdir()}
        assert produced == EXPECTED_FILES, produced
        assert {p.name for p in work.iterdir()} == {NOTEBOOK.name, 'outputs'}
        nbformat.validate(notebook)
        if args.更新输出:
            nbformat.write(notebook, NOTEBOOK)
            output_dir = TASK_DIR / 'outputs'; output_dir.mkdir(exist_ok=True)
            for filename in EXPECTED_FILES:
                shutil.copy2(work / 'outputs' / filename, output_dir / filename)
        result = dict(environment, notebook_code_cells=code_count, original_examples=43, supplementary_code_cells=code_count - 43, generated_files=sorted(produced), numeric_output_checks=12, no_stderr=True, updated_outputs=args.更新输出)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
