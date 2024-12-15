
import streamlit as st
import pandas as pd
import os
from datetime import date
from datos import registrar_almacen

def borrar_precio_unitario():
    st.session_state['precio_unitario'] = 0.0

def reset_form():
    st.session_state['form_data'] = {
        'sku': '',
        'material': '',
        'categoria': '---',
        'cantidad': 1,
        'proveedor': '',
        'ubicacion': '',
        'notas': ''
    }
def cargar_materiales():
    ruta_material = os.path.join('datos', 'material.csv')
    material_df = pd.read_csv(ruta_material)
    return material_df

def almacen_tab():
    st.header('Inventario')
    material_df = cargar_materiales()
    materiales = material_df['SKU'].sort_values().tolist()
    with st.form('Registro de Entradas'):
        st.title('Registro de Entrada')

        sku = st.selectbox('Codigo identificador',['---']+materiales, help='Si el codigo no esta en la lista registrelo en la pestaña nuevo')
        if sku and sku != '---':
            material = material_df.loc[material_df['SKU']==sku,'Material'].values
            categoria = material_df.loc[material_df['SKU']==sku,'Categoria'].values
            if len(material)>0:
                material = material[0] 
            else:
                material = 'Desconocido'
            if len(categoria)>0:
                categoria = categoria[0]
            else:
                categoria = 'Desconocido'
            
        else:
            categoria = None
            material = None

        cantidad = st.number_input('Cantidad',min_value=0,value=None,step=1)
        st.write(f"Precio unitario")
        # Inicializar el precio unitario en el estado de sesión
        if 'precio_unitario' not in st.session_state:
            st.session_state['precio_unitario'] = 0.0
        if 'Moneda' not in st.session_state:
            st.session_state['Moneda'] = 0.0
        # Crear las columnas para los botones
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.form_submit_button('Pesos'):
                st.session_state['Moneda'] = 'pesos'
        with col2:
            if st.form_submit_button('Bolivares'):
                st.session_state['Moneda'] = 'bs'
        with col3:
            if st.form_submit_button('Dolares'):
                st.session_state['Moneda'] = 'dolares'

        if st.session_state['Moneda'] == 'pesos':
            pesos = st.number_input('Valor en pesos',min_value=0, step=100, value=None)
            cambio_pesos = st.number_input('Tasa de cambio',min_value=0, value=None)
            submit_pesos = st.form_submit_button('Peso-Dolar')
            if submit_pesos:
                if cambio_pesos > 0 and pesos>0:
                    st.session_state['precio_unitario'] = pesos / cambio_pesos
                else:
                    st.error('Faltan montos')

        if st.session_state['Moneda'] == 'bs':
            bs = st.number_input('Valor en Bs.',min_value=0, value=None)
            cambio_bs = st.number_input('Tasa de cambio',min_value=0, value=None)
            submit_bs = st.form_submit_button('Bs-Dolar')
            if submit_bs:
                if cambio_bs>0 and bs>0:
                    st.session_state['precio_unitario'] = bs / cambio_bs
                else:
                    st.error('Faltan montos')
        
        if st.session_state['Moneda'] == 'dolares':
            dolares = st.number_input('Valor en Dolares.',min_value=0,value=None, step=0.1)
            submit_dolares =  st.form_submit_button('Precio Unitario')
            if submit_dolares:
                if dolares>0:
                    st.session_state['precio_unitario'] = dolares
                else:
                    st.error('Faltan montos')
        st.write(f'## Precio unitario: ${st.session_state["precio_unitario"]:.2f}')
        st.form_submit_button('Borrar Precio Unitario', on_click=borrar_precio_unitario)
        

        # Input manual para ajustar el precio unitario
        precio_unitario = round(st.session_state['precio_unitario'],2) 


        fecha_ingreso = date.today().strftime('%d/%m/%Y') #Formato dia-mes-año
        proveedor = st.text_input('Proveedor', placeholder='Libreria Mundial')
        ubicacion = st.text_input('Ubicación en almacén', placeholder='Ej.: Estante 2, Zona A')
        notas = st.text_area('Notas adicionales', placeholder='Ingrese detalles adicionales...')

        #boton de enviar
        submitted = st.form_submit_button('Registrar')

        #Validaciones
        if submitted:
            if not sku:
                st.error('El campo "Código SKU" es obligatorio.')
            elif not material:
                st.error('El campo "Nombre del material" es obligatorio.')
            elif cantidad <= 0:
                st.error('La cantidad debe ser mayor a 0.')
            elif not ubicacion:
                st.error('El campo "Ubicación en almacén" es obligatorio')
            elif categoria == '---':
                st.error('Seleccione una categoria correcta')
            else:
                st.write("**Datos registrados:**")
                st.write(f"- Código o SKU: {sku}")
                st.write(f"- Nombre del material: {material}")
                st.write(f"- Categoría: {categoria}")
                st.write(f"- Cantidad: {cantidad}")
                st.write(f"- Precio unitario: ${precio_unitario:.2f}")
                st.write(f"- Fecha de ingreso: {fecha_ingreso}")
                st.write(f"- Proveedor: {proveedor}")
                st.write(f"- Ubicación: {ubicacion}")
                st.write(f"- Notas: {notas if notas else 'Sin notas adicionales'}")
                registrar_almacen('Entrada',sku,material,categoria,cantidad,precio_unitario,fecha_ingreso,proveedor,None,ubicacion,notas)
                reset_form()
    #Salidas 
    with st.form('Registro de salidas'):
        st.title('Registro de Salida')
        sku_s = st.selectbox('Codigo identificador',['---']+materiales, help='Si el codigo no esta en la lista registrelo en la pestaña nuevo')

        cantidad_s = st.number_input('Cantidad',min_value=0, value=None, step=1)
        usuario = st.selectbox(
            'Usuario Responsable',
            options=['---','Angela','Joel'],
        )
        fecha_s =  date.today().strftime('%d/%m/%Y') #Formato dia-mes-año
        notas_s = st.text_area('Notas adicionales', placeholder='Ingrese detalles adicionales...')

        submitted_s = st.form_submit_button('Registrar')

        # validación
        if submitted_s:
            #cargamos todos los sku de almacen    
            ruta_almacen = os.path.join('datos', 'almacen.csv')
            almacen_df = pd.read_csv(ruta_almacen)
            sku_df = almacen_df[almacen_df['SKU']==sku_s]
            saldo = sku_df['Cantidad'].sum()
            if not sku_s:
                st.error('El campo "Código SKU" es obligatorio.')
            elif cantidad_s == None:
                st.error('La cantidad debe ser mayor a 0.')
            elif usuario == '---':
                st.error('Seleccione un usuario responsable')
            elif (saldo-cantidad_s) < 0:
                st.error('No hay suficiente material')
            else:
                st.write("**Datos registrados:**")
                st.write(f"- Código o SKU: {sku_s}")
                st.write(f"- Cantidad: {cantidad_s}")
                st.write(f"- Fecha de salida: {fecha_s}")
                st.write(f"- Usuario Responsable: {usuario}")
                st.write(f"- Notas: {notas_s if notas_s else 'Sin notas adicionales'}")
                registrar_almacen('Salida',sku_s,None,None,cantidad_s,None,fecha_s,None,usuario,None,notas_s)