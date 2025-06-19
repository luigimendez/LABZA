

import streamlit as st
import pandas as pd
import os
from datetime import date

# Archivo de datos
data_file = "pacientes_labza.xlsx"
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Nombre", "Teléfono", "Edad", "Estudios", "Fecha", "Costo"])
    df.to_excel(data_file, index=False, engine='openpyxl')

def cargar_datos():
    return pd.read_excel(data_file, engine='openpyxl')

def guardar_datos(nuevo):
    df = cargar_datos()
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_excel(data_file, index=False, engine='openpyxl')

def app():
    st.title("Laboratorio de Análisis Clínicos LABZA")

    menu = st.sidebar.radio("Menú", ["Registro de Paciente", "Pacientes Registrados", "Buscar Paciente"])

    if menu == "Registro de Paciente":
        st.header("Registrar nuevo paciente")

        nombre = st.text_input("Nombre completo")
        telefono = st.text_input("Teléfono")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        estudios_opciones = [
            "Biometria Hematica", "SMAC 24", "SMAC 30", "RX Frebiles", "Examen Prenatales",
            "Glucosa-Colesterol-Trigliceridos", "Examen Prenupciales", "Perfil Tiroideo Completo 5",
            "Perfil Tiroideo 3", "Perfil Hormonal", "Perfil Lipidos", "Perfil Hepatico",
            "Perfil Reumatoide", "Factor Reumatoide Solo", "VDRL", "Helicobacter Pylori",
            "Copro Unico", "Copro Seriado 3", "Urocultivo", "Coprocultivo", "Cultivo Faringeo",
            "Antigeno Prostatico Especifico", "Hemoglobina Glucosilada", "Influenza + COVID",
            "Paq. Básico BH", "SMAC24", "RX FEB", "Creatinina Serica", "Prolactina", "Testosterona",
            "Insulina", "Tamiz Glusemico", "Vitamina D", "CA 125", "Cortisol", "CA 19-9",
            "Antigeno Carcinoembrionario", "Alfafetoproteina", "HLA-B27", "Proteina C Reactiva",
            "Anticuerpos Ntinucleares", "Dimero D", "Ferritina", "Proteinas en Orina", "HCG Cuantitativa",
            "Grupo y RH", "Antidoping Basico", "Antidoping Completo", "Panel Hepatitis"
        ]
        estudios = st.multiselect("Estudios realizados", estudios_opciones)
        fecha = st.date_input("Fecha del estudio", value=date.today())
        costo = st.number_input("Costo (MXN)", min_value=0.0, format="%.2f")

        if st.button("Guardar"):
            if nombre and telefono and edad and estudios and fecha and costo:
                nuevo_paciente = {
                    "Nombre": nombre,
                    "Teléfono": telefono,
                    "Edad": edad,
                    "Estudios": ", ".join(estudios),
                    "Fecha": fecha.strftime("%Y-%m-%d"),
                    "Costo": costo,
                }
                guardar_datos(nuevo_paciente)
                st.success("✅ Paciente registrado exitosamente.")
            else:
                st.error("❌ Todos los campos son obligatorios.")

    elif menu == "Pacientes Registrados":
        st.header("Listado de Pacientes")
        df = cargar_datos()
        st.dataframe(df)

        if st.download_button("📥 Exportar a Excel", df.to_excel(index=False), file_name="pacientes_labza_export.xlsx"):
            st.success("Archivo exportado correctamente.")

    elif menu == "Buscar Paciente":
        st.header("Buscar paciente por nombre")
        df = cargar_datos()
        nombre_buscado = st.text_input("Ingrese el nombre del paciente")
        if nombre_buscado:
            resultados = df[df["Nombre"].str.contains(nombre_buscado, case=False, na=False)]
            if not resultados.empty:
                st.dataframe(resultados)
            else:
                st.info("🔍 No se encontraron pacientes con ese nombre.")

if __name__ == "__main__":
    app()
