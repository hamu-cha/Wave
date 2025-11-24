import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time

st.title("固定端反射のアニメーション")
st.write("固定端では反射波が**逆位相（符号反転）**になり、端点は常に節になります。")

# ---- Parameter UI ----
A = st.slider("振幅 A", 0.5, 2.0, 1.0)
wlen = st.slider("波長 λ", 1.0, 10.0, 4.0)
period = st.slider("周期 T", 0.2, 3.0, 1.5)

fps = 30  # frame rate
duration = 5  # animation length (sec)

x = np.linspace(0, 5, 500)
placeholder = st.empty()

if st.button("▶ アニメーション開始"):
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        t = elapsed % period  # 周期的に循環

        # ---- 波形 ----
        incoming = A * np.sin(2*np.pi*(x/wlen - t/period))     # 入射波
        reflected = -A * np.sin(2*np.pi*(x/wlen + t/period))   # 固定端反射（反転）
        y = incoming + reflected                               # 合成波

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(x, incoming, linestyle="--", label="入射波")
        ax.plot(x, reflected, linestyle="--", label="反射波")
        ax.plot(x, y, linewidth=2, label="合成波")

        ax.set_ylim(-A*2, A*2)
        ax.set_xlim(0, 5)
        ax.legend()
        ax.set_xlabel("x [m]")

        placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(0)

        if elapsed > duration:
            break
