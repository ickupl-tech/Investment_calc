import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Procentu Składanego", layout="centered")

st.title("📈 Kalkulator Procentu Składanego")
st.write("Zobacz moc procentu składanego i nakładające się linie zysku oraz dopłat.")

# --- INICJALIZACJA PARAMETRÓW DOMYŚLNYCH ---
# Wartości startowe (będą nadpisywane przez slidery pod wykresem)
kwota_startowa_val = 22947.21
wplata_miesieczna_val = 0.0
lata_val = 5
stopa_zwrotu_val = 11.0

# Tworzymy kontenery, aby wymusić kolejność wyświetlania elementów na stronie
miejsce_na_wykres = st.container()
st.markdown("---")
miejsce_na_suwaki = st.container()

# --- PANEL Z SUWAKAMI (WYŚWIETLANY POD WYKRESEM) ---
with miejsce_na_suwaki:
    st.subheader("⚙️ Ustawienia inwestycji")
    
    # Blokada wartości ujemnych przez min_value=0.0
    kwota_startowa = st.number_input("Kwota początkowa (PLN)", min_value=0.0, value=kwota_startowa_val, step=500.0)
    wplata_miesieczna = st.number_input("Miesięczna dopłata (PLN)", min_value=0.0, value=wplata_miesieczna_val, step=50.0)
    
    col1, col2 = st.columns(2)
    with col1:
        lata = st.slider("Okres inwestycji (lata)", min_value=1, max_value=40, value=lata_val)
    with col2:
        stopa_zwrotu = st.slider("Średnioroczna stopa zwrotu (%)", min_value=0.0, max_value=30.0, value=stopa_zwrotu_val, step=0.5)

# --- OBLICZENIA ROK PO ROKU ---
kapital_total = kwota_startowa
suma_doplat = kwota_startowa
dane_wykresu = []

# Rok 0 (stan początkowy)
dane_wykresu.append({
    "Rok": 0, 
    "Suma dopłat (Twój wkład)": round(suma_doplat, 2),
    "Wartość portfela (Zysk + Wkład)": round(kapital_total, 2)
})

for rok in range(1, lata + 1):
    suma_wplat_w_roku = wplata_miesieczna * 12
    suma_doplat += suma_wplat_w_roku
    
    # Naliczenie stopy zwrotu na koniec roku (kapitalizacja roczna)
    kapital_total = (kapital_total + suma_wplat_w_roku) * (1 + stopa_zwrotu / 100)
    
    dane_wykresu.append({
        "Rok": rok, 
        "Suma dopłat (Twój wkład)": round(suma_doplat, 2),
        "Wartość portfela (Zysk + Wkład)": round(kapital_total, 2)
    })

df = pd.DataFrame(dane_wykresu).set_index("Rok")

# --- GENEROWANIE WYNIKÓW (WYŚWIETLANE NA SAMEJ GÓRZE STRONY) ---
with miejsce_na_wykres:
    st.subheader("📊 Wynik symulacji")
    
    c1, c2 = st.columns(2)
    czysty_zysk = kapital_total - suma_doplat
    
    with c1:
        st.metric(label=f"Wartość portfela za {lata} lat(a)", value=f"{round(kapital_total, 2):,} PLN")
    with c2:
        st.metric(label="Wypracowany czysty zysk", value=f"{round(czysty_zysk, 2):,} PLN", delta=f"{round((czysty_zysk/suma_doplat)*100, 1)}% względem wkładu")
    
    # Wykres liniowy z dwoma nakładającymi się liniami
    # Streamlit automatycznie dopasuje osie od 0 (brak wartości ujemnych z racji min_value)
    st.line_chart(df, y=["Suma dopłat (Twój wkład)", "Wartość portfela (Zysk + Wkład)"], color=["#FF4B4B", "#00F0FF"])

    # Opcjonalna tabela
    if st.checkbox("Pokaż szczegółowe dane liczbowe rok po roku"):
        st.dataframe(df)
