import streamlit as st
from registro_tab import registro_tab
from modificacion_tab import modificacion_tab
from visualizacion_tab import visualizacion_tab
from almacen_tab import almacen_tab
from datos import documentos
from nuevo_tab import nuevo_tab

def main():

    # Cargar datos iniciales
    try:
        documentos()
    except Exception as e:
        st.error(f"Error al cargar documentos: {e}")
        return

    # Configuración de las pestañas
        st.title("Aplicación con Pestañas")
    tabs = st.tabs(['Orden','Almacen','Nuevo','Visualizacion', 'Modificacion'])

    # Pestaña Registro
    with tabs[0]:
        registro_tab()

   # Pestaña almacen 
    with tabs[1]:
        almacen_tab()

    # Pestaña Visualización
    with tabs[2]:
        nuevo_tab()

    # Pestaña Visualización
    with tabs[3]:
        visualizacion_tab()

    # Pestaña Modificación
    with tabs[4]:
        modificacion_tab()
    



# Punto de entrada principal
if __name__ == "__main__":
    main()