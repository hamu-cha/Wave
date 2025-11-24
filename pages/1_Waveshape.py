# -----------setting-----------------
import numpy as np
import matplotlib.pyplot as plt

def wave(ax, x, t, wavelength, period, A = 1, linestyle = None, color = None):
    y = A*np.sin(2*np.pi*(x/wavelength - t/period))
    if not np.isscalar(x) and np.isscalar(t):
        ax.plot(x, y, linestyle=linestyle, linewidth=2, color=color, zorder=1)

    elif np.isscalar(x) and not np.isscalar(t):
        ax.plot(t, y, linestyle=linestyle, linewidth=2, color=color, zorder=1)

def axis(ax, start, finish, width=0.005):
    xmin, xmax = start
    ymin, ymax = finish
    ax.quiver([0, 0], [0, ymin], [xmax - 0, 0], [0, ymax - ymin],
                angles='xy', scale_units='xy', scale=1.0, width=width,
                headwidth=4.5, headlength=7.5, headaxislength=6, zorder=2)
    
    ax.tick_params(axis="both", which="major", direction="inout", length=7)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)


def sppos(ax, l=0, b=0, r=None, t=None):
    if l is not None:
        ax.spines['left'].set_position(('data', l))
    if b is not None:
        ax.spines['bottom'].set_position(('data', b))
    if r is not None:
        ax.spines['right'].set_position(('data', r))
    if t is not None:
        ax.spines['top'].set_position(('data', t))

def spoff(ax, l=False, b=False, r=False, t=False):
    ax.spines["left"].set_visible(l)
    ax.spines["bottom"].set_visible(b)
    ax.spines["right"].set_visible(r)
    ax.spines["top"].set_visible(t)

def AxLabel(ax):
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_bbox(dict(facecolor='white', edgecolor='none', pad=1.5))

def MakeFig(ax, x, t, wavelength, term, x_range, y_range, A = 1):
    
    ax.grid(color="black", linestyle = "--", linewidth=0.5, zorder=0)
    wave(ax, x, t, wavelength, term, A, linestyle = "-", color = "black")
    axis(ax, x_range, y_range, width = 0.003)
    sppos(ax)
    spoff(ax)
    AxLabel(ax)

# --------------------------- 

import streamlit as st

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams["font.size"] = 16

st.title('波形')

fig1, ax1 = plt.subplots(figsize=(7, 5))
x1 = np.linspace(0, 5, 500)

# 入力欄
wanp = st.slider('振幅', 0.0, 2.0, 1.0, step = 0.1)
wlen = st.slider('波長', 2.0, 10.0, 4.0, step = 0.50)
time = st.slider('時刻', 0.0, 1.0, 0.0, step = 0.1)

# 入力がすべて揃っていれば計算
A = wanp
lam = wlen
t = time
y1 = A * np.sin(2 * np.pi * (x1 / lam - t))

ax1.plot(x1, y1, zorder = 6)
ax1.text(5.5, 0.2, r'$x[\rm{m}]$')
ax1.text(-0.6, 2.25, r'$y[\rm{m}]$')

# 軸設定
start = (-0.5, 6)
finish = (-2.5, 2.5)
axis(ax1, start, finish)
spoff(ax1)
sppos(ax1)

ax1.grid(True, zorder = 0)

ax1.set_xticks(np.arange(1, 6, 1))
if A is not None:
    ax1.set_yticks(np.arange(-A, A + 0.1, A))
else:
    ax1.set_yticks([])

for label in ax1.get_xticklabels() + ax1.get_yticklabels():
        label.set_bbox(dict(facecolor='white', edgecolor='none', pad=1.5))
# グラフ描画
st.pyplot(fig1)

