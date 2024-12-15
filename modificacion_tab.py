import streamlit as st
import pandas as pd
import os

def cargar_data(info):
    #Tomamos los datos del CSV que queremos
    try:
        match info:
            case 'Clientes':
                ruta = os.path.join('datos','clientes.csv')
            case 'Productos':
                ruta = os.path.join('datos','productos.csv')
            case 'Ordenes':
                ruta = os.path.join('datos','ordenes.csv')
            case 'Detalles de Ordenes':
                ruta = os.path.join('datos','detalles_ordenes.csv')
            case 'Material':
                ruta = os.path.join('datos','material.csv')
        
        df = pd.read_csv(ruta, index_col=0)
        return df
    
    except FileNotFoundError:
        st.error(f'Archivo no encontrado: {ruta}')
    except Exception as e:
        st.error(f'Error al cargar datos: {e}')
    return None


def modificacion_tab():
    st.title('Modificación de Datos')

    
    with st.form('Selección de Datos Almacenados'):

        tipo_datos = st.selectbox('Tipo de Datos', ['---','Clientes','Productos','Ordenes','Detalles de Ordenes','Material'])
        submit = st.form_submit_button('Seleccionar Data')

        if submit:
            if tipo_datos == '---':
                st.error('Seleccione los datos')
            else:
                df = cargar_data(tipo_datos)
                st.data_editor(df)
    return
