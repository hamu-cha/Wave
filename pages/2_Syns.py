import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("波の合成")
st.text('右向きに進む波1と左向きに進む波2の合成波を確認しよう。')
amplitude1 = st.slider('波1の振幅', -1.0, 1.0, 1.0, step = 0.1)
amplitude2 = st.slider('波2の振幅', -1.0, 1.0, 1.0, step = 0.1)

# 波設定
x2 = np.linspace(0, 10, 400)
wavelength = 4
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
               amplitude1 * np.sin(2 * np.pi * (x2 - t/2) / wavelength),
               0)
y2m = np.where((x2 >= 8 - t/2) & (x2 <= 10 - t/2),
               amplitude2 * np.sin(2 * np.pi * (x2 + t/2) / wavelength),
               0)

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.plot(x2, y2p, color='black', linestyle = '--', linewidth=1.5, zorder=1)
ax2.plot(x2, y2m, color='red', linestyle = '--', linewidth=1.5, zorder=1)
ax2.plot(x2, y2p + y2m, color='blue', linewidth=2, zorder=2)
ax2.plot([0, 10], [0, 0], color='black', linewidth=3, zorder=3)
ax2.set_xlim(0, 10)
ax2.set_ylim(-2, 2)
ax2.set_xticks([])
ax2.set_yticks(np.arange(-2, 2.1, 0.25))
ax2.set_yticklabels([])
ax2.tick_params('both', which = 'major', length = 0)
ax2.grid(axis = 'y')
st.pyplot(fig2)
plt.close(fig2)

# ==== 🎞 自動再生処理 ====
if st.session_state.playing2:
    time.sleep(0.5)
    st.session_state.frame2 = (st.session_state.frame2 + 1) % n_frames
    st.rerun()