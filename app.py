import streamlit as st
import pandas as pd
import numpy as np

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Procentu Składanego", layout="centered")
st.title("📈 Kalkulator Procentu Składanego")
st.write("Zobacz, jak Twój kapitał rośnie w czasie dzięki magii procentu składanego.")

# Panel boczny z suwakami (dane wejściowe)
st.sidebar.header("Ustawienia symulacji")
kwota_startowa = st.sidebar.number_input("Kwota początkowa (PLN)", min_value=0.0, value=22947.21, step=500.0)
wplata_miesieczna = st.sidebar.number_input("Miesięczna dopłata (PLN)", min_value=0.0, value=0.0, step=50.0)
lata = st.sidebar.slider("Okres inwestycji (lata)", min_value=1, max_value=40, value=5)
stopa_zwrotu = st.sidebar.slider("Średnioroczna stopa zwrotu (%)", min_value=0.0, max_value=30.0, value=11.0, step=0.5)

# Obliczenia rok po roku
kapital = kwota_startowa
dane_wykresu = []

for rok in range(0, lata + 1):
    if rok > 0:
        # Dodanie wpłat miesięcznych w ciągu roku i naliczenie stopy zwrotu
        # Dla uproszczenia: kapitalizacja roczna
        suma_wplat_w_roku = wplata_miesieczna * 12
        kapital = (kapital + suma_wplat_w_roku) * (1 + stopa_zwrotu / 100)
    
    dane_wykresu.append({"Rok": rok, "Wartość portfela": round(kapital, 2)})

df = pd.DataFrame(dane_wykresu)

# Wyświetlenie wyników głównych
st.metric(label=f"Wartość portfela za {lata} lat(a)", value=f"{df.iloc[-1]['Wartość portfela']:,} PLN")

# Wykres
st.subheader("Wizualizacja wzrostu kapitału")
st.line_chart(df.set_index("Rok"))

# Tabela z danymi
if st.checkbox("Pokaż szczegółowe dane rok po roku"):
    st.dataframe(df)
