#!/usr/bin/env python3
"""PRISMA 2020 系統性文獻回顧流程圖生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def generate_prisma(identified, duplicates, screened_excl, fulltext_excl, included, output):
    fig, ax = plt.subplots(1, 1, figsize=(10, 14))
    ax.set_xlim(0, 10); ax.set_ylim(0, 14)
    ax.axis('off')

    # 臺灣教育藍色系
    C_BLUE   = '#1A5276'
    C_MID    = '#2471A3'
    C_YELLOW = '#F9E79F'
    C_ORANGE = '#FDEBD0'
    C_GREEN  = '#D5F5E3'
    C_RED    = '#FDEDEC'
    C_GRAY   = '#F0F0F0'

    # Helper
    def box(ax, x, y, w, h, text, bg, fc='#1C2A35', fontsize=10):
        rect = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.1',
                              facecolor=bg, edgecolor=C_BLUE, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, color=fc, fontweight='bold',
                fontfamily='DejaVu Sans', wrap=True, multialignment='center')

    def arrow(ax, x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=C_BLUE, lw=1.5))

    def side_box(ax, x, y, w, h, text, bg=C_RED):
        rect = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.1',
                              facecolor=bg, edgecolor='#E74C3C', linewidth=1, linestyle='--')
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=8.5, color='#922B21', fontfamily='DejaVu Sans',
                multialignment='center')

    # 標題
    ax.text(5, 13.5, 'PRISMA 2020 Flow Diagram', ha='center', va='center',
            fontsize=14, fontweight='bold', color=C_BLUE)

    # 識別階段
    screened = identified - duplicates
    fulltext = screened - screened_excl

    box(ax, 1.5, 11.2, 7, 1.2,
        f'識別（Identification）\n資料庫搜尋：N = {identified}\n移除重複：n = {duplicates}',
        '#D6EAF8', fontsize=9.5)
    arrow(ax, 5, 11.2, 5, 10.3)

    box(ax, 1.5, 9.0, 7, 1.2,
        f'篩選（Screening）\n標題/摘要篩選：n = {screened}\n排除：n = {screened_excl}',
        C_YELLOW, fontsize=9.5)
    side_box(ax, 8.7, 9.2, 1.1, 0.7,
             f'排除\nn = {screened_excl}')
    ax.annotate('', xy=(8.7, 9.55), xytext=(8.5, 9.55),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1))
    arrow(ax, 5, 9.0, 5, 8.1)

    box(ax, 1.5, 6.8, 7, 1.2,
        f'資格審查（Eligibility）\n全文審查：n = {fulltext}\n排除：n = {fulltext_excl}',
        C_ORANGE, fontsize=9.5)
    side_box(ax, 8.7, 7.0, 1.1, 0.7,
             f'排除\nn = {fulltext_excl}')
    ax.annotate('', xy=(8.7, 7.35), xytext=(8.5, 7.35),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1))
    arrow(ax, 5, 6.8, 5, 5.9)

    box(ax, 1.5, 4.6, 7, 1.2,
        f'納入（Included）\n最終納入文獻：n = {included}',
        C_GREEN, fontsize=10.5)

    # 說明文字
    ax.text(0.2, 12.5, '識別', fontsize=11, color=C_BLUE, fontweight='bold', rotation=90, va='center')
    ax.text(0.2, 9.5,  '篩選', fontsize=11, color='#8E6914', fontweight='bold', rotation=90, va='center')
    ax.text(0.2, 7.3,  '審查', fontsize=11, color='#784212', fontweight='bold', rotation=90, va='center')
    ax.text(0.2, 5.1,  '納入', fontsize=11, color='#1E8449', fontweight='bold', rotation=90, va='center')

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'✓ PRISMA 流程圖已儲存：{output}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--identified',     type=int, default=523)
    parser.add_argument('--duplicates',     type=int, default=89)
    parser.add_argument('--screened_excl',  type=int, default=320)
    parser.add_argument('--fulltext_excl',  type=int, default=67)
    parser.add_argument('--included',       type=int, default=47)
    parser.add_argument('--output',         default='PRISMA流程圖.png')
    args = parser.parse_args()
    generate_prisma(args.identified, args.duplicates, args.screened_excl,
                    args.fulltext_excl, args.included, args.output)

if __name__ == '__main__':
    main()
