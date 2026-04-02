import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Seite konfigurieren
st.set_page_config(page_title="Martina Weickmann Inventar", layout="centered")

st.title("🎨 Martina Weickmann - Kunst-Inventar")
st.write("Hier werden alle Werke sicher in die Cloud gespeichert.")

# Verbindung zu Google Sheets aufbauen
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Verbindung zu Google fehlgeschlagen. Bitte prüfe die Secrets im Dashboard!")

# Formular für die Eingabe
with st.form("art_entry_form", clear_on_submit=True):
    st.subheader("Neues Werk aufnehmen")
    
    # Kamera-Input
    uploaded_file = st.camera_input("Bild aufnehmen")
    
    # Text-Eingaben
    title = st.text_input("Titel des Kunstwerks")
    
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Breite (cm)", min_value=0.0, step=0.1)
    with col2:
        height = st.number_input("Höhe (cm)", min_value=0.0, step=0.1)
        
    medium = st.selectbox("Technik", ["Öl auf Leinwand", "Acryl", "Aquarell", "Mischtechnik", "Skizze"])
    price = st.number_input("Preisvorstellung (€)", min_value=0)
    
    # Speicher-Button
    submitted = st.form_submit_button("Sicher in Google Cloud speichern")

    if submitted:
        if title: # Wir prüfen erst mal nur den Titel
            try:
                # Neue Datenzeile erstellen
                new_row = pd.DataFrame([{
                    "Datum": datetime.now().strftime("%d.%m.%Y"),
                    "Titel": title,
                    "Breite": width,
                    "Höhe": height,
                    "Technik": medium,
                    "Preis": price,
                    "Bild_URL": "Foto erfasst" 
                }])
                
                # Bestehende Daten von Google lesen
                existing_data = conn.read(worksheet="Inventar")
                
                # Neue Zeile anhängen
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # Das Ganze zurück zu Google schicken
                conn.update(worksheet="Inventar", data=updated_df)
                
                # Erfolg feiern!
                st.success(f"✅ Wunderbar! '{title}' ist jetzt in deiner Google Tabelle sicher gespeichert.")
                st.balloons()
            except Exception as e:
                st.error(f"Fehler beim Speichern in Google Sheets: {e}")
        else:
            st.warning("Bitte gib mindestens einen Titel für das Bild ein.")

# Live-Vorschau der echten Google Tabelle
st.divider()
st.subheader("Live-Vorschau deiner Google Tabelle")
try:
    # Wir laden die Daten direkt von Google Sheets
    live_data = conn.read(worksheet="Inventar")
    if not live_data.empty:
        st.dataframe(live_data, use_container_width=True)
    else:
        st.info("Die Google Tabelle ist noch leer. Zeit für das erste Kunstwerk!")
except Exception as e:
    st.info("Suche Verbindung zu Google Sheets... Bitte stelle sicher, dass das Tabellenblatt 'Inventar' heißt.")
