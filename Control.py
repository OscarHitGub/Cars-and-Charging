# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 13:16:03 2025

@author: oscar
"""

import laadpaalData as lpd
import ElectricCars as ec
import GeodataEnCars as gc

import streamlit as st

# --- Pagina instellingen ---
st.set_page_config(page_title="Auto Dashboard", layout="wide")

# --- Navigatie ---
st.sidebar.title("📂 Navigatie")
pagina = st.sidebar.radio(
    "Kies een sectie:",
    ["🚗 Auto Dashboard", "⚡Laadpalen Data"]
)

if pagina == "⚡Laadpalen Data":
    lpd.laadpaal()
    
elif pagina == "🚗 Auto Dashboard":
    gc.car_data()
    ec.cars()