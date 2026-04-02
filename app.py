import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Martina Weickmann Inventar", layout="centered")

st.title("🎨 Martina Weickmann - Kunst-Inventar")

# Verbindung zu Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("art_entry_form", clear_on_submit=True):
    st.subheader("Neues Werk aufnehmen")
    uploaded_file = st.camera_input("Bild aufnehmen")
    title = st.text_input("Titel des Kunstwerks")
    
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Breite (cm)", min_value=0.0, step=0.1)
    with col2:
        height = st.number_input("Höhe (cm)", min_value=0.0, step=0.1)
        
    medium = st.selectbox("Technik", ["Öl auf Leinwand", "Acryl", "Aquarell", "Mischtechnik", "Skizze"])
    price = st.number_input("Preisvorstellung (€)", min_value=0)
    
    submitted = st.form_submit_button("Sicher in Google Cloud speichern")

    if submitted:
        if title:
            try:
                # 1. Bestehende Daten von Google holen
                existing_data = conn.read(worksheet="Inventar")
                
                # 2. Neue Zeile erstellen
                new_row = pd.DataFrame([{
                    "Datum": datetime.now().strftime("%d.%m.%Y"),
                    "Titel": title,
                    "Breite": width,
                    "Höhe": height,
                    "Technik": medium,
                    "Preis": price,
                    "Bild_URL": "Foto erfasst"
                }])
                
                # 3. Zusammenfügen
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # 4. ALLES zurückschreiben (das löst den 400er Fehler meistens)
                conn.update(worksheet="Inventar", data=updated_df)
                
                st.success(f"✅ Wunderbar! '{title}' wurde gespeichert.")
                st.balloons()
            except Exception as e:
                st.error(f"Verbindung steht, aber Google meldet: {e}")
        else:
            st.warning("Bitte gib einen Titel ein.")

st.divider()
st.subheader("Deine Google Tabelle (Live)")
try:
    df = conn.read(worksheet="Inventar")
    st.dataframe(df, use_container_width=True)
except:
    st.info("Suche Tabelle...")
