
import streamlit as st
import pandas as pd
import os
import time

def nuevo_cliente():
    ruta_clientes = os.path.join('datos', 'clientes.csv')
    if os.path.exists(ruta_clientes):
        cliente_df = pd.read_csv(ruta_clientes)
    else:
        cliente_df = pd.DataFrame(columns=['Cliente_ID', 'Nombre', 'Tipo_Cliente', 'Ubicacion'])

    with st.form('nuevo_cliente'):
        st.title('Nuevo Cliente')
        nombre = st.text_input('Nombre del cliente', placeholder='Ej. Rey de las tortas')
        tipo_cliente = st.selectbox('Tipo de Cliente', ['---','Repostero','Personal','Empresa no repostera'])
        ubicacion = st.selectbox('Ubicación', ['---','Rubio','San Antonio','San Cristobal', 'Otro'])
        telefono = st.text_input('Informacion de contacto', placeholder='Ej. +58 0424-3779850')

        if st.form_submit_button('Registrar nuevo cliente'):
            if nombre.strip() == '':
                st.error('El nombre del cliente no puede estar vacio')
            elif tipo_cliente == '---':
                st.error('Debe seleccionar un tipo de cliente')
            elif ubicacion == '---':
                st.error('Debe seleccionar una ubicacion')
            elif nombre in cliente_df['Nombre'].values:
                st.error('El cliente ya existe')
            else:
                #verificar si el cliente existe
                if cliente_df.empty:
                    nuevo_id=1
                elif nombre in cliente_df['Nombre'].values:
                    st.error('El cliente ya existe')
                else:
                    nuevo_id = cliente_df['Cliente_ID'].max()+1
            
                #Crear el diccionario de  nuevo cliente
                nuevo_cliente = {
                'Cliente_ID': nuevo_id,
                'Nombre': nombre,
                'Tipo_Cliente': tipo_cliente,
                'Ubicacion': ubicacion,
                'Telefono':telefono
                }
                cliente_df = pd.concat([cliente_df, pd.DataFrame([nuevo_cliente])], ignore_index=True)
                cliente_df.to_csv(ruta_clientes, index=False)
                st.write(f"""
                Cliente_ID: {nuevo_id}\n
                Nombre: {nombre}\n
                Tipo Cliente: {tipo_cliente}\n
                Ubicacion: {ubicacion}\n
                Telefono: {telefono}""")
def nuevo_producto():    
    ruta_productos = os.path.join('datos', 'productos.csv')
    if os.path.exists(ruta_productos):
        producto_df = pd.read_csv(ruta_productos)
    else:
        producto_df = pd.DataFrame(columns=['Producto_ID','Producto'])
    
    with st.form('nuevo_producto'):
        st.title('Nuevo Producto')
        producto = st.text_input('Producto',placeholder='Ej. Topper Caballo1')

        if st.form_submit_button('Registrar nuevo producto'):
            if producto.strip() =='':
                st.error('El producto no puede estar vacio')
            elif producto in producto_df['Producto'].values:
                st.error('El producto ya existe')
            else:
                #verificar si el producto existe
                if producto_df.empty:
                    producto_id = 1
                else:
                    producto_id = producto_df['Producto_ID'].max()+1
                nuevo_producto = {
                    'Producto_ID': producto_id,
                    'Producto': producto
                }
                producto_df = pd.concat([producto_df,pd.DataFrame([nuevo_producto])], ignore_index=True)
                producto_df.to_csv(ruta_productos, index=False)
                st.write(f"""
                Producto ID: {producto_id}\n
                Producto: {producto}
                         """)
def nuevo_material():
    ruta_materiales =os.path.join('datos','material.csv')
    if os.path.exists(ruta_materiales):
        material_df = pd.read_csv(ruta_materiales)
    else: 
        material_df = pd.DataFrame(columns=['SKU','Material','Categoria'])            
    
    with st.form('nuevo_material'):
        st.title('Nuevo Material')
        sku = st.text_input('Identificador único del material',placeholder='Ej. CAR-A4-RS')
        material = st.text_input('Nombre del material',placeholder='Ej. Cartulina Rosa')
        categoria = st.selectbox(
            'Categoría del material',
            options=['---','Cartulina','Pegamento','Foami','Insumos de maquinaria', 'Otros'],
        )
        if st.form_submit_button('Registrar nuevo material'):
            if sku.strip()=='':
                st.error('El codigo unico no puede estar vacio')
            elif material.strip()=='':
                st.error('El nombre del material no puede estar vacio')
            elif categoria == '---':
                st.error('Debe elegir una categoria')
            else:
                nuevo_material = {
                    'SKU':sku,
                    'Material':material,
                    'Categoria':categoria
                }
                material_df = pd.concat([material_df,pd.DataFrame([nuevo_material])], ignore_index=True)
                material_df.to_csv(ruta_materiales, index=False)
                st.write(f"""
                Codigo Unico: {sku}\n
                Material: {material}\
                Categoria: {categoria}
                         """)

def nuevo_tab():
    if 'tipo_datos' not in st.session_state:
        st.session_state['tipo_datos'] = ''
        st.session_state['formulario_llamado'] = False
    with st.form('menu_nuevo'):    
        tipo_datos = st.selectbox('Nuevo Ingreso al sistema', ['---','Nuevo Cliente','Nuevo Producto','Nuevo material'],key='tipo_dato_menu')
        submit = st.form_submit_button('Seleccionar Nuevo Ingreso')    
        if submit:
            st.session_state['tipo_datos'] = tipo_datos
            st.session_state['formulario_llamado'] = False  # Reiniciar el formulario al cambiar opción
    if not st.session_state['formulario_llamado']:
        match st.session_state['tipo_datos']:
            case '---':
                st.error('Seleccione nuevo ingreso')
            case 'Nuevo Cliente':
                nuevo_cliente()
            case 'Nuevo Producto':
                nuevo_producto()
            case 'Nuevo material':
                nuevo_material()



