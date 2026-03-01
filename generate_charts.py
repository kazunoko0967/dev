#!/usr/bin/env python3
"""Chart generation for Sony & Nintendo Earnings Update Report"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Hiragino Sans'
import matplotlib.patches as mpatches
import numpy as np
import os

# Create output directory
os.makedirs("charts", exist_ok=True)

# ── Color palette ──────────────────────────────────────────────
SONY_BLUE   = "#003087"
SONY_LIGHT  = "#4A90D9"
NINTENDO_RED   = "#E60012"
NINTENDO_LIGHT = "#FF6B6B"
BEAT_GREEN  = "#2ECC71"
MISS_RED    = "#E74C3C"
GRAY        = "#BDC3C7"
DARK_GRAY   = "#2C3E50"
BG_WHITE    = "#FAFAFA"

def style_ax(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=11, fontweight="bold", color=DARK_GRAY, pad=10)
    ax.set_xlabel(xlabel, fontsize=8, color=DARK_GRAY)
    ax.set_ylabel(ylabel, fontsize=8, color=DARK_GRAY)
    ax.tick_params(colors=DARK_GRAY, labelsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRAY)
    ax.spines["bottom"].set_color(GRAY)
    ax.set_facecolor(BG_WHITE)
    ax.grid(axis="y", color=GRAY, linestyle="--", linewidth=0.5, alpha=0.7)

# ─────────────────────────────────────────────────────────────────
# Figure 1: Sony 四半期別売上高推移
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

quarters = ["Q1\nFY24", "Q2\nFY24", "Q3\nFY24", "Q4\nFY24",
            "Q1\nFY25", "Q2\nFY25", "Q3\nFY25"]
sony_rev = [2890, 2975, 3685, 3420, 2980, 3010, 3714]  # 億円 (¥B)
colors = [SONY_LIGHT]*6 + [SONY_BLUE]

bars = ax.bar(quarters, sony_rev, color=colors, width=0.6, edgecolor="white", linewidth=0.5)
for bar, val in zip(bars, sony_rev):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f"¥{val:,}B", ha="center", va="bottom", fontsize=7, color=DARK_GRAY)

ax.set_ylim(0, 4500)
style_ax(ax, "図1：ソニーグループ 四半期別売上高推移（単位：十億円）",
         ylabel="売上高（十億円）")
ax.text(0.99, 0.02, "出所：ソニーグループ決算短信 / 当社推計", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/sony_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 1 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 2: Sony 営業利益・利益率推移
# ─────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

op_income = [180, 205, 421, 310, 198, 248, 515]
op_margin = [6.2, 6.9, 11.5, 9.1, 6.6, 8.2, 13.9]

ax2 = ax1.twinx()
bars = ax1.bar(quarters, op_income, color=[SONY_LIGHT]*6 + [SONY_BLUE],
               width=0.6, edgecolor="white", alpha=0.85)
ax2.plot(quarters, op_margin, color=NINTENDO_RED, marker="o",
         linewidth=2, markersize=6, zorder=5)
ax2.set_ylim(0, 20)
ax2.set_ylabel("営業利益率（%）", fontsize=8, color=NINTENDO_RED)
ax2.tick_params(axis="y", colors=NINTENDO_RED, labelsize=7)

for bar, val in zip(bars, op_income):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f"¥{val}B", ha="center", va="bottom", fontsize=6.5, color=DARK_GRAY)

ax1.set_ylim(0, 700)
style_ax(ax1, "図2：ソニーグループ 営業利益・営業利益率推移", ylabel="営業利益（十億円）")
ax1.text(0.99, 0.02, "出所：ソニーグループ決算短信 / 当社推計", transform=ax1.transAxes,
         ha="right", va="bottom", fontsize=6, color=GRAY)
patch_bar = mpatches.Patch(color=SONY_BLUE, label="営業利益（十億円）")
line_margin = plt.Line2D([0], [0], color=NINTENDO_RED, marker="o", markersize=5,
                          label="営業利益率（%）")
ax1.legend(handles=[patch_bar, line_margin], fontsize=7, loc="upper left")
plt.tight_layout()
plt.savefig("charts/sony_operating_income.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 2 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 3: Sony セグメント別売上高 (Q3 FY2025)
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

segments = ["G&NS\nゲーム", "I&SS\nセンサー", "ET&S\nエレクトロ", "Music\n音楽", "Pictures\n映像"]
seg_sales = [1614, 585, 658, 542, 340]  # ¥B approx
seg_oi    = [141, 95, 59, 106, 27]      # operating income ¥B
seg_colors = [SONY_BLUE, "#2980B9", "#5DADE2", "#85C1E9", "#AED6F1"]

x = np.arange(len(segments))
w = 0.35
b1 = ax.bar(x - w/2, seg_sales, w, label="売上高（十億円）", color=seg_colors, edgecolor="white")
b2 = ax.bar(x + w/2, seg_oi,   w, label="営業利益（十億円）",
            color=BEAT_GREEN, alpha=0.7, edgecolor="white")

for bar, v in zip(b1, seg_sales):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"{v}", ha="center", va="bottom", fontsize=6.5, color=DARK_GRAY)
for bar, v in zip(b2, seg_oi):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"{v}", ha="center", va="bottom", fontsize=6.5, color=DARK_GRAY)

ax.set_xticks(x)
ax.set_xticklabels(segments, fontsize=8)
ax.legend(fontsize=8, loc="upper right")
style_ax(ax, "図3：ソニーグループ セグメント別業績（Q3 FY2025）", ylabel="金額（十億円）")
ax.text(0.99, 0.02, "出所：ソニーグループ決算短信 2026年2月5日", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/sony_segments.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 3 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 4: Sony Beat/Miss サマリー
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 3.5))
fig.patch.set_facecolor(BG_WHITE)

metrics  = ["売上高", "営業利益", "純利益", "EPS（ADR）"]
reported = [3714, 515, 377, 41]
est      = [3680, 422, 340, 33]
unit     = ["¥B", "¥B", "¥B", "¢"]
beat     = [(r - e) / e * 100 for r, e in zip(reported, est)]
colors_b = [BEAT_GREEN if b >= 0 else MISS_RED for b in beat]

bars = ax.barh(metrics, beat, color=colors_b, edgecolor="white", height=0.5)
ax.axvline(0, color=DARK_GRAY, linewidth=1)
for bar, b_val in zip(bars, beat):
    xpos = b_val + 0.2 if b_val >= 0 else b_val - 0.2
    ha = "left" if b_val >= 0 else "right"
    ax.text(xpos, bar.get_y() + bar.get_height()/2,
            f"{b_val:+.1f}%", va="center", ha=ha, fontsize=9, color=DARK_GRAY, fontweight="bold")

ax.set_xlim(-10, 35)
style_ax(ax, "図4：ソニーQ3 FY2025 コンセンサス比較（ビート/ミス）", xlabel="コンセンサス比（%）")
ax.text(0.99, 0.02, "出所：Bloomberg / ソニーグループ決算短信 2026年2月5日", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/sony_beat_miss.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 4 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 5: Nintendo 四半期別売上高推移
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

n_quarters = ["Q1\nFY25", "Q2\nFY25", "Q3\nFY25", "Q4\nFY25",
               "Q1\nFY26", "Q2\nFY26", "Q3\nFY26"]
n_rev = [430, 460, 820, 610, 580, 568, 758]  # ¥B approx
n_colors = [NINTENDO_LIGHT]*6 + [NINTENDO_RED]

bars = ax.bar(n_quarters, n_rev, color=n_colors, width=0.6, edgecolor="white", linewidth=0.5)
for bar, val in zip(bars, n_rev):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"¥{val}B", ha="center", va="bottom", fontsize=7, color=DARK_GRAY)

ax.set_ylim(0, 950)
style_ax(ax, "図5：任天堂 四半期別売上高推移（単位：十億円）", ylabel="売上高（十億円）")
ax.text(0.99, 0.02, "出所：任天堂決算短信 / 当社推計", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/nintendo_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 5 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 6: Nintendo Switch 2 販売台数推移
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

sw2_quarters  = ["Q1 FY26\n(Jun-Sep)", "Q2 FY26\n(Jul-Sep)", "Q3 FY26\n(Oct-Dec)"]
sw2_quarterly = [6.26, 4.1, 7.01]   # million units per quarter (approx)
sw2_cumulative = [6.26, 10.36, 17.37]

ax2 = ax.twinx()
bars = ax.bar(sw2_quarters, sw2_quarterly, color=[NINTENDO_LIGHT, NINTENDO_LIGHT, NINTENDO_RED],
              width=0.5, edgecolor="white")
ax2.plot(sw2_quarters, sw2_cumulative, color=DARK_GRAY, marker="s",
         linewidth=2, markersize=7, zorder=5)
ax2.set_ylim(0, 25)
ax2.set_ylabel("累計販売台数（百万台）", fontsize=8, color=DARK_GRAY)
ax2.tick_params(axis="y", colors=DARK_GRAY, labelsize=7)

for bar, v in zip(bars, sw2_quarterly):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"{v:.2f}M", ha="center", va="bottom", fontsize=8, color=DARK_GRAY)
for xp, yp, v in zip(range(3), sw2_cumulative, sw2_cumulative):
    ax2.text(xp + 0.15, yp + 0.5, f"累計{v}M台", fontsize=7, color=DARK_GRAY)

ax.set_ylim(0, 12)
style_ax(ax, "図6：Nintendo Switch 2 四半期別・累計販売台数", ylabel="四半期販売台数（百万台）")
patch_q = mpatches.Patch(color=NINTENDO_RED, label="四半期販売台数（百万台）")
line_c = plt.Line2D([0], [0], color=DARK_GRAY, marker="s", markersize=5, label="累計販売台数（百万台）")
ax.legend(handles=[patch_q, line_c], fontsize=7, loc="upper left")
ax.text(0.99, 0.02, "出所：任天堂決算短信 2026年2月3日", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/nintendo_switch2.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 6 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 7: Nintendo 営業利益・利益率推移
# ─────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

n_op_income = [65, 80, 156, 98, 55, 62, 143]
n_op_margin = [15.1, 17.4, 19.0, 16.1, 9.5, 10.9, 19.2]

ax2 = ax1.twinx()
bars = ax1.bar(n_quarters, n_op_income, color=[NINTENDO_LIGHT]*6 + [NINTENDO_RED],
               width=0.6, edgecolor="white", alpha=0.85)
ax2.plot(n_quarters, n_op_margin, color=SONY_BLUE, marker="D",
         linewidth=2, markersize=6, zorder=5)
ax2.set_ylim(0, 30)
ax2.set_ylabel("営業利益率（%）", fontsize=8, color=SONY_BLUE)
ax2.tick_params(axis="y", colors=SONY_BLUE, labelsize=7)

for bar, v in zip(bars, n_op_income):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f"¥{v}B", ha="center", va="bottom", fontsize=6.5, color=DARK_GRAY)

ax1.set_ylim(0, 200)
style_ax(ax1, "図7：任天堂 営業利益・営業利益率推移", ylabel="営業利益（十億円）")
patch_bar = mpatches.Patch(color=NINTENDO_RED, label="営業利益（十億円）")
line_m = plt.Line2D([0], [0], color=SONY_BLUE, marker="D", markersize=5, label="営業利益率（%）")
ax1.legend(handles=[patch_bar, line_m], fontsize=7, loc="upper left")
ax1.text(0.99, 0.02, "出所：任天堂決算短信 / 当社推計", transform=ax1.transAxes,
         ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/nintendo_operating_income.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 7 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 8: Nintendo ソフトウェア 主要タイトル販売
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

titles   = ["Mario Kart\nWorld", "Pokémon\nZ-A", "その他\nSW2タイトル"]
sw2_units = [14.03, 3.89, 20.01]  # million units
bar_colors = [NINTENDO_RED, NINTENDO_LIGHT, GRAY]

bars = ax.bar(titles, sw2_units, color=bar_colors, width=0.5, edgecolor="white")
for bar, v in zip(bars, sw2_units):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f"{v:.2f}M本", ha="center", va="bottom", fontsize=9, color=DARK_GRAY, fontweight="bold")

ax.set_ylim(0, 22)
style_ax(ax, "図8：Nintendo Switch 2 主要ソフトウェア販売本数（FY2026 Q1-Q3累計）",
         ylabel="販売本数（百万本）")
ax.text(0.99, 0.02, "出所：任天堂決算短信 2026年2月3日", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/nintendo_software.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 8 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 9: 両社比較 — 営業利益率
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

comp_quarters = ["Q1\nFY25/26", "Q2\nFY25/26", "Q3\nFY25/26"]
sony_margins  = [6.6, 8.2, 13.9]
nint_margins  = [9.5, 10.9, 19.2]

ax.plot(comp_quarters, sony_margins, color=SONY_BLUE, marker="o",
        linewidth=2.5, markersize=8, label="ソニーグループ", zorder=5)
ax.plot(comp_quarters, nint_margins, color=NINTENDO_RED, marker="s",
        linewidth=2.5, markersize=8, label="任天堂", zorder=5)

for xp, (sm, nm) in enumerate(zip(sony_margins, nint_margins)):
    ax.text(xp + 0.05, sm + 0.4, f"{sm}%", fontsize=8, color=SONY_BLUE)
    ax.text(xp + 0.05, nm + 0.4, f"{nm}%", fontsize=8, color=NINTENDO_RED)

ax.set_ylim(0, 25)
ax.legend(fontsize=9)
style_ax(ax, "図9：ソニー vs 任天堂 営業利益率比較（FY2026 Q1-Q3）", ylabel="営業利益率（%）")
ax.text(0.99, 0.02, "出所：各社決算短信 / 当社推計", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/comparison_margins.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 9 saved")

# ─────────────────────────────────────────────────────────────────
# Figure 10: Sony 通期予想修正（旧 vs 新）
# ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BG_WHITE)

categories = ["売上高\n（兆円）", "営業利益\n（千億円）"]
old_vals   = [11.94, 14.26]
new_vals   = [12.30, 15.40]
x = np.arange(len(categories))
w = 0.3

bars_old = ax.bar(x - w/2, old_vals, w, label="旧予想（11月時点）", color=GRAY, edgecolor="white")
bars_new = ax.bar(x + w/2, new_vals, w, label="新予想（2月修正）", color=SONY_BLUE, edgecolor="white")

for bar, v in zip(bars_old, old_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"{v}", ha="center", va="bottom", fontsize=9)
for bar, v in zip(bars_new, new_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"{v}", ha="center", va="bottom", fontsize=9, color=SONY_BLUE, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9)
ax.legend(fontsize=8)
style_ax(ax, "図10：ソニー FY2025 通期業績予想修正（旧 vs 新）", ylabel="金額")
ax.text(0.99, 0.02, "出所：ソニーグループ 2026年2月5日決算発表", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=6, color=GRAY)
plt.tight_layout()
plt.savefig("charts/sony_guidance.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Figure 10 saved")

print("\n✅ All charts generated in ./charts/")
