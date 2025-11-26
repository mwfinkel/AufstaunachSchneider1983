# Datei: schneider_1983_demo_streamlit.py

# Interaktive App zur Visualisierung des Grundwasseraufstaus nach Schneider (1983).
# Parameter wie hydraulischer Gradient, Strömungswinkel und Bauwerkslänge können angepasst  und die Auswirkungen direkt angesehen werden.

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Aufstau und Absenkung nach Schneider (1983)", layout="wide")

st.markdown("""
    <style>
    label[data-baseweb="form-control"] > div {
        font-size: 44px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Grundwasseraufstau und -absenkung nach Schneider (1983)")
st.header("Linienförmiges Bauwerk, reine Umströmung (Gl. 1 in Schneider 1983)")


# Eingabeparameter
st.markdown("<h3 style='font-size:24px;'>Hydraulischer Gradient J (-)</h3>", unsafe_allow_html=True)
J = st.slider(" ", min_value=0.0001, max_value=0.01, value=0.0025, step=0.0001, format="%f",)

st.markdown("<h3 style='font-size:24px;'>Strömungswinkel (Grad)</h3>", unsafe_allow_html=True)
theta_deg = st.slider("", min_value=0, max_value=90, value=0)

st.markdown("<h3 style='font-size:24px;'>Bauwerkslänge L (m)</h3>", unsafe_allow_html=True)
L = st.slider("", min_value=10, max_value=200, value=100)

# Berechnungen
theta = np.radians(theta_deg)
t = L / 2
dx = 1.
dy = 1.

x = np.arange(-2 * L, 2 * L, dx)
y = np.arange(-2 * L, 2 * L, dy)
X, Y = np.meshgrid(x, y)

Dh_um = np.sign(X) * 0.5 * J * np.cos(theta) * np.sqrt(2.) * np.sqrt(np.sqrt(np.power((np.power(X,2.) - np.power(Y,2.) + np.power(t,2.)),2.) + 4. * np.power(X,2.) * np.power(Y,2.)) + np.power(X,2.) - np.power(Y,2.) + np.power(t,2.)) - J * X * np.cos(theta)

# term1 = (X**2 - Y**2 + t**2)**2 + 4 * X**2 * Y**2
# term2 = np.sqrt(term1)
# term3 = np.sqrt(term2 + X**2 - Y**2 + t**2)
# Dh_um = np.sign(X) * 0.5 * J * np.cos(theta) * np.sqrt(2) * term3 - J * X * np.cos(theta)

Dh_um_max = J * np.cos(theta) * t * 100
st.metric("Maximaler Aufstau", f"{Dh_um_max:.1f} cm")

max_level = round(Dh_um_max/10)*10

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
contour = ax.contour(X, Y, Dh_um*100, [-30, -20, -10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10, 20, 30], linewidths=2, colors='blue')
ax.clabel(contour, inline=True, fontsize=8)
ax.set_title("Aufstauverteilung nach Schneider 1983")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_xlim([-2 * L, 2 * L])
ax.set_ylim([-2 * L, 2 * L])
ax.add_patch(plt.Rectangle((-L/100, -L / 2), L/50, L, color='red',zorder=200))
ax.grid(True)

st.pyplot(fig)
