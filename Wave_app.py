# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
# import setting as set

# # st.title('波形')

# # fig1, ax1 = plt.subplots(figsize=(7, 5))
# # x1 = np.linspace(0, 5, 500)

# # # 入力欄
# # wanp = st.text_input('振幅')
# # wlen = st.text_input('波長')
# # time = st.text_input('時刻')

# # # 初期値
# # A = None
# # y1 = np.zeros_like(x1)

# # # 入力がすべて揃っていれば計算
# # if wanp and wlen and time:
# #     try:
# #         A = float(wanp)
# #         lam = float(wlen)
# #         t = float(time)
# #         y1 = A * np.sin(2 * np.pi * (x1 / lam - t))
# #     except ValueError:
# #         st.warning("すべての値を数値で入力してください。")

# # ax1.plot(x1, y1, zorder = 1)
# # ax1.grid(True)

# # # 軸設定
# # start = (-0.5, 6)
# # if A is not None:
# #     finish = (-1.5 * A, 1.5 * A)
# # else:
# #     finish = (-1, 1)
# # set.axis(ax1, start, finish)
# # set.spoff(ax1)
# # set.sppos(ax1)

# # ax1.set_xticks(np.arange(1, 6, 1))
# # if A is not None:
# #     ax1.set_yticks(np.arange(-A, A + 0.1, A))
# # else:
# #     ax1.set_yticks([])

# # for label in ax1.get_xticklabels() + ax1.get_yticklabels():
# #         label.set_bbox(dict(facecolor='white', edgecolor='none', pad=1.5))
# # # グラフ描画
# # st.pyplot(fig1)

# # fig2, ax2 = plt.subplots(figsize = (7, 5))
# # x2 = np.linspace(0, 10, 100)
# # y2 = np.sin(2*np.pi*x2/4)

# # y2p = np.where((x2 >= 0) & (x2 <= 2), y2, 0)
# # y2m = np.where((x2 >= 8) & (x2 <= 10), y2, 0)

# # ax2.plot(x2, y2p, zorder = 1)
# # ax2.plot(x2, y2m, zorder = 1)
# # ax2.plot([0, 10], [0, 0], linewidth = 3, color = 'black', zorder = 2)

# # ax2.set_xlim(0, 10)
# # ax2.set_ylim(-2, 2)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("波の合成")

# 波設定
x2 = np.linspace(0, 10, 400)
wavelength = 4
amplitude = 1
n_frames = 16

# セッション状態の初期化
if "frame2" not in st.session_state:
    st.session_state.frame2 = 0
if "playing2" not in st.session_state:
    st.session_state.playing2 = False

# ==== 🎛 コントロールバー（1行にボタンを配置） ====
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⏮ 戻る"):
            st.session_state.frame2 = max(0, st.session_state.frame2 - 1)
    with col2:
        if st.button("▶ 再生 / ⏸ 停止"):
            st.session_state.playing2 = not st.session_state.playing2
    with col3:
        if st.button("⏭ 進む"):
            st.session_state.frame2 = min(n_frames - 1, st.session_state.frame2 + 1)
    with col4:
        if st.button("⏹ リセット"):
            st.session_state.playing2 = False
            st.session_state.frame2 = 0

# ==== 🪄 グラフ描画 ====
t = st.session_state.frame2
y2 = np.sin(2 * np.pi * x2 / wavelength)

y2p = np.where((x2 >= 0 + t/2) & (x2 <= 2 + t/2),
               amplitude * np.sin(2 * np.pi * (x2 - t/2) / wavelength),
               0)
y2m = np.where((x2 >= 8 - t/2) & (x2 <= 10 - t/2),
               amplitude * np.sin(2 * np.pi * (x2 + t/2) / wavelength),
               0)

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.plot(x2, y2p, color='black', linewidth=2, zorder=1)
ax2.plot(x2, y2m, color='red', linewidth=2, zorder=1)
ax2.plot(x2, y2p + y2m, color='blue', linewidth=2, zorder=2)
ax2.plot([0, 10], [0, 0], color='black', linewidth=3, zorder=3)
ax2.set_xlim(0, 10)
ax2.set_ylim(-2, 2)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.grid(False)
st.pyplot(fig2)
plt.close(fig2)

# ==== 🎞 自動再生処理 ====
if st.session_state.playing2:
    time.sleep(0.5)
    st.session_state.frame2 = (st.session_state.frame2 + 1) % n_frames
    st.rerun()
