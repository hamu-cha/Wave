import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("縦波・横波アニメーション")

amp = st.slider('振幅', -1.0, 1.0, -0.5, step = 0.1)

frames_tot = 129
x_line = np.linspace(-32, 16, 481)
x_point = np.linspace(-32, 16, 97)
x_rest = x_point.copy()

# --- state of session---
#session_state is rememmber freme number.
if "frame2" not in st.session_state: 
    #session_state of frame number is 0 at start point.
    st.session_state.frame2 = 0 
if "playing2" not in st.session_state:
    #session_state of animetion state is 0 at start point.
    st.session_state.playing2 = False

# ==== cntrole panel ====
with st.container():
    col1, col2, col3, col4 = st.columns(4) #prepare 4 rows
    with col1:
        if st.button("Back"):
            #if press button frame number is decrese
            st.session_state.frame2 -= 1
    with col2:
        if st.button("Play/Stop"):
            st.session_state.playing2 = not st.session_state.playing2
            # if press button frame state become reversal current state
    with col3:
        if st.button("Next"):
            #if press button frame number is increse
            st.session_state.frame2 += 1

    with col4:
        if st.button("Reset"):
            #if press button frame state become start state
            st.session_state.playing2 = False
            st.session_state.frame2 = 0

x_shift = np.linspace(0, 32, frames_tot)[st.session_state.frame2]

fig, ax = plt.subplots(figsize=(7, 3.25))
ax.set_aspect('equal')

L_mask = (x_line >= -33 + x_shift) & (x_line <= 0 + x_shift)
P_mask = (x_point >= -33 + x_shift) & (x_point <= 0 + x_shift)
y_l = amp*np.sin(2*np.pi*((x_line - x_shift)/8))
y_p = amp*np.sin(2*np.pi*((x_point - x_shift)/8))

y_line = np.where(L_mask, y_l, 0)
y_point = np.where(P_mask, y_p, 0)

xp_white = x_point < 0
xp_color  = x_point >= 0
xl_white = x_line < 0
xl_color  = x_line >= 0

ax.plot(x_line[xl_white], y_line[xl_white], '-', color='white', alpha = 0, zorder=3)
ax.plot(x_point[xp_white], y_point[xp_white], 
        linestyle='None', marker='o', color='white', alpha = 0, zorder=4)
ax.plot(x_line[xl_color], y_line[xl_color], '-', color='orange', zorder=3)
ax.plot(x_point[xp_color], y_point[xp_color], 
        linestyle='None', marker='o', color='orange', zorder=4)
ax.plot([-1, 17], [0, 0], '-', color='black', zorder=2)

x_longitudinal = np.where(P_mask, x_rest + y_p, x_rest)
ax.scatter(x_longitudinal[xp_white], 2*np.ones(len(x_rest))[xp_white], 
           color='white', alpha = 0, zorder=4)
ax.scatter(x_longitudinal[xp_color], 2*np.ones(len(x_rest))[xp_color], 
           color='black', zorder=4)

ax.set_xlim(-1, 16)
ax.set_ylim(-2, 3)
ax.set_xticks(np.arange(0, 17, 1))
ax.set_xticklabels([])
ax.set_yticks(np.arange(-1, 1.1, 0.5))
ax.tick_params(axis = 'y', which = 'major', direction = 'in')
ax.tick_params(axis = 'x', which = 'major', length = 0)
ax.grid(zorder=0)
st.pyplot(fig)

if st.session_state.playing2:
    st.session_state.frame2 = (st.session_state.frame2 + 1) % frames_tot
    st.write(st.session_state.frame2)
    time.sleep(0.05)
    st.rerun()
else:
    st.session_state.frame2 = (st.session_state.frame2 + 1) % frames_tot
    st.write(st.session_state.frame2)
