import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfiguration der Seite
st.set_page_config(page_title="Martina Weickmann Inventar", layout="centered")

st.title("🎨 Martina Weickmann - Kunst-Inventar")
st.write("Hier kannst du neue Werke scannen und für das Management erfassen.")

# Datei für die Datenbank (CSV)
DB_FILE = "inventar.csv"

# Formular für die Erfassung
with st.form("art_entry_form", clear_on_submit=True):
    st.subheader("Neues Werk aufnehmen")
    
    # Kamera-Input
    uploaded_file = st.camera_input("Bild aufnehmen")
    
    # Details
    title = st.text_input("Titel des Kunstwerks")
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Breite (cm)", min_value=0.0, step=0.1)
    with col2:
        height = st.number_input("Höhe (cm)", min_value=0.0, step=0.1)
        
    medium = st.selectbox("Technik", ["Öl auf Leinwand", "Acryl", "Aquarell", "Mischtechnik", "Skizze"])
    price = st.number_input("Preisvorstellung (€)", min_value=0)
    
    submitted = st.form_submit_button("In Inventar speichern")

    if submitted:
        if title and uploaded_file:
            # Zeitstempel für den Dateinamen des Bildes
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_filename = f"bild_{timestamp}.png"
            
            # Bild lokal speichern (optional, für den Anfang)
            with open(img_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Daten in Liste speichern
            new_data = {
                "Datum": [datetime.now().strftime("%d.%m.%Y")],
                "Titel": [title],
                "Breite": [width],
                "Höhe": [height],
                "Technik": [medium],
                "Preis": [price],
                "Bild-Datei": [img_filename]
            }
            df = pd.DataFrame(new_data)
            
            # In CSV schreiben
            if not os.path.isfile(DB_FILE):
                df.to_csv(DB_FILE, index=False)
            else:
                df.to_csv(DB_FILE, mode='a', header=False, index=False)
                
            st.success(f"Erfolgreich gespeichert: {title}")
        else:
            st.error("Bitte einen Titel angeben und ein Foto machen!")

# Bereich: Inventar anzeigen
st.divider()
st.subheader("Aktuelles Inventar")
if os.path.isfile(DB_FILE):
    inventory_df = pd.read_csv(DB_FILE)
    st.dataframe(inventory_df)
else:
    st.info("Noch keine Werke im Inventar erfasst.")