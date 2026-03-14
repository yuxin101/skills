#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert.py - 一键 Word → 清华 MBA thuthesis PDF 转换器
用法: python3 convert.py <input.docx> [output_dir]
"""

import sys
import os
import subprocess
from pathlib import Path

def run(cmd, cwd=None, check=True):
    print(f'▶ {cmd}')
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if check and result.returncode != 0:
        print(f'❌ 命令失败 (exit {result.returncode})')
        sys.exit(result.returncode)
    return result.returncode

def main():
    if len(sys.argv) < 2:
        print('用法: python3 convert.py <input.docx> [output_dir]')
        print('示例: python3 convert.py 我的论文.docx ./output')
        sys.exit(1)

    docx_path = Path(sys.argv[1]).resolve()
    if not docx_path.exists():
        print(f'❌ 找不到文件: {docx_path}')
        sys.exit(1)

    # 输出目录默认为 ./output/<论文名>
    if len(sys.argv) >= 3:
        base_out = Path(sys.argv[2]).resolve()
    else:
        base_out = Path('output') / docx_path.stem

    scripts_dir = Path(__file__).parent
    project_root = scripts_dir.parent

    json_dir = project_root / 'output'
    latex_dir = base_out

    print(f'\n{"="*60}')
    print(f'📄 输入: {docx_path.name}')
    print(f'📁 输出: {latex_dir}')
    print(f'{"="*60}\n')

    # ── Step 1: 解析 Word ───────────────────────────────────────
    print('【Step 1/3】解析 Word 文档...')
    run(f'python3 "{scripts_dir}/parse_docx.py" "{docx_path}" "{json_dir}"')

    # 找到生成的 JSON 文件
    json_files = sorted(json_dir.glob('parsed_*.json'), key=lambda f: f.stat().st_mtime, reverse=True)
    if not json_files:
        print('❌ 未找到解析输出的 JSON 文件')
        sys.exit(1)
    json_path = json_files[0]
    print(f'   → JSON: {json_path.name}')

    # ── Step 2: 渲染 LaTeX 项目 ─────────────────────────────────
    print('\n【Step 2/3】渲染 LaTeX 项目...')
    run(f'python3 "{scripts_dir}/render.py" "{json_path}" "{latex_dir}"')

    # ── Step 3: 编译 PDF ─────────────────────────────────────────
    print('\n【Step 3/3】编译 PDF...')
    # xelatex 查找顺序：
    #   1. 环境变量 XELATEX_PATH（指定完整路径）
    #   2. 常见 macOS TeX Live 路径 /Library/TeX/texbin
    #   3. PATH 中的 xelatex（Linux/其他）
    _tex_bin = os.environ.get('XELATEX_PATH', '')
    if _tex_bin:
        extra_path = str(Path(_tex_bin).parent)
    elif Path('/Library/TeX/texbin/xelatex').exists():
        extra_path = '/Library/TeX/texbin'
    else:
        extra_path = ''
    export_path = (extra_path + ':' + os.environ.get('PATH', '')) if extra_path else os.environ.get('PATH', '')
    env = os.environ.copy()
    env['PATH'] = export_path

    def xelatex(cwd, label=''):
        result = subprocess.run(
            'xelatex -interaction=nonstopmode thesis.tex',
            shell=True, cwd=cwd, env=env,
            capture_output=True, text=True
        )
        for line in result.stdout.split('\n'):
            if any(k in line for k in ['Error', 'error', 'Fatal', '!']):
                if 'Font Warning' not in line and 'microtype' not in line:
                    print(f'   {line}')
        return result.returncode

    def toc_hash(cwd):
        """读取 .toc 文件内容的 hash，用于检测目录是否稳定"""
        import hashlib
        toc = Path(cwd) / 'thesis.toc'
        return hashlib.md5(toc.read_bytes()).hexdigest() if toc.exists() else ''

    # BibTeX 编译流程: xelatex → bibtex → xelatex → xelatex → (xelatex)
    # 第1次：生成 .aux 文件（含 \citation 记录）
    print('   第 1 次编译（生成 .aux）...')
    xelatex(latex_dir)
    h1 = toc_hash(latex_dir)

    # 运行 bibtex 生成 .bbl 文件
    bibtex_bin = str(Path(env['PATH'].split(':')[0]) / 'bibtex') if extra_path else 'bibtex'
    if not Path(bibtex_bin).exists():
        bibtex_bin = 'bibtex'
    print('   运行 bibtex...')
    result = subprocess.run(
        f'bibtex thesis',
        shell=True, cwd=latex_dir, env=env,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f'   ⚠️  bibtex 警告（可能是部分引用未找到）:')
        for line in result.stdout.splitlines()[-5:]:
            print(f'      {line}')

    # 第2次：把参考文献 .bbl 写入
    print('   第 2 次编译（写入参考文献）...')
    xelatex(latex_dir)
    h2 = toc_hash(latex_dir)

    # 第3次：修正目录/交叉引用
    print('   第 3 次编译（稳定目录）...')
    xelatex(latex_dir)
    h3 = toc_hash(latex_dir)

    # 若 toc 还不稳定，补第4次
    if h3 != h2:
        print('   第 4 次编译（目录稳定中）...')
        xelatex(latex_dir)

    pdf_path = latex_dir / 'thesis.pdf'
    if pdf_path.exists():
        size_kb = pdf_path.stat().st_size // 1024
        print(f'\n{"="*60}')
        print(f'✅ 完成！PDF 已生成:')
        print(f'   {pdf_path}  ({size_kb} KB)')

        # 同时把 PDF 复制到 Word 原文件同目录，文件名与 Word 相同
        import shutil
        word_pdf = docx_path.with_suffix('.pdf')
        shutil.copy2(pdf_path, word_pdf)
        print(f'   → 已复制到: {word_pdf}')
        print(f'{"="*60}\n')

        # 打开 PDF（macOS open；Linux/Windows 跳过）
        import platform
        if platform.system() == 'Darwin':
            subprocess.run(['open', str(word_pdf)], check=False)
    else:
        print(f'\n❌ PDF 未生成，请检查 {latex_dir}/thesis.log')
        sys.exit(1)

if __name__ == '__main__':
    main()
