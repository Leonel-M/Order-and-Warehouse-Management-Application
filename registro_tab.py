import streamlit as st
import pandas as pd
import datetime
from datetime import date
import os
from datos import registrar_datos

def limpiar_campos():
    """Función para limpiar los campos del formulario."""
    st.session_state['cliente'] = ''
    st.session_state['productos'] = []
    st.session_state['tipo_cliente']='---'
    st.session_state['ubicacion'] = '---'
    st.session_state['nota_orden'] = ''
    st.session_state['fecha_entrega'] = date.today()
def borrar_productos():
    st.session_state['productos'] = []
#cargar los nombres de los clientes
def cargar_clientes():
    ruta_clientes = os.path.join('datos', 'clientes.csv')
    cliente_df = pd.read_csv(ruta_clientes)
    return cliente_df
#cargar los nombres de los productos
def cargar_productos():
    ruta_productos = os.path.join('datos','productos.csv')
    producto_df = pd.read_csv(ruta_productos)
    return producto_df

def registro_tab():

    st.header('Nueva Orden')

    #INICIALIZACION DE VARIABLES
    if 'productos' not in st.session_state:
        st.session_state['productos'] = []

    with st.form('Formulario_registro'):
        cliente_df = cargar_clientes()
        nombres = cliente_df['Nombre'].sort_values().tolist()
        cliente = st.selectbox('Nombre del Cliente',['---']+nombres, help='Si el nombre no esta en la lista registrelo en la pestaña nuevo')
        if cliente and cliente != '---':
            tipo_cliente = cliente_df.loc[cliente_df['Nombre']==cliente,'Tipo_Cliente'].values
            ubicacion = cliente_df.loc[cliente_df['Nombre']==cliente,'Ubicacion'].values
            if len(tipo_cliente)>0:
                tipo_cliente = tipo_cliente[0] 
            else:
                tipo_cliente = 'Desconocido'
            if len(ubicacion)>0:
                ubicacion = ubicacion[0]
            else:
                ubicacion = 'Desconocido'
            
        else:
            tipo_cliente = None
            ubicacion = None

        #Producto y cantidad
        producto_df = cargar_productos()
        productos_list = producto_df['Producto'].sort_values().tolist()
        producto = st.selectbox('Producto',['---']+productos_list, help='Si el producto no esta en la lista registrelo en la pestaña nuevo', key='producto')
        
        col1,col2,col3 = st.columns(3)

        with col1:
            cantidad = st.number_input('Cantidad de Producto', value=None,min_value=0, step=1, key='cantidad')
        with col2:
            st.markdown('   ')
            agregar = st.form_submit_button('Agregar Producto')
            if agregar and not cantidad==None:
                st.session_state['productos'].append({'producto':producto, 'cantidad':cantidad})
        with col3:
            st.markdown('   ')
            st.form_submit_button('Borrar productos',on_click=borrar_productos)

        #Mostrar productos agregados
        if st.session_state['productos']:
            st.write('### Productos agregados: ')
            for item in st.session_state['productos']:
                st.write(f'- {item['producto']} (Cantidad: {item['cantidad']})')
            producto = ''
            cantidad= 0


        fecha_registro = date.today().strftime('%d/%m/%Y') #Formato dia-mes-año

        col4,col5 = st.columns([1,2])
        with col4:
            fecha_entrega = st.date_input('Fecha de Entrega',format='DD/MM/YYYY')
        with col5:
            #Hora
            hora = st.slider(
            "Hora de Entrega:",
            min_value=datetime.time(7, 0),
            max_value=datetime.time(20, 0),
            step=datetime.timedelta(minutes=60),
            format="HH:mm"
            )
        
        nota_orden = st.text_area('Nota de Orden (Opcional)', placeholder='Ej.: Cliente quiere requerimientos extra')

        #Boton de envio completo del formulario
        submit = st.form_submit_button('Registrar Orden')

        if submit:
            if not cliente or not st.session_state['productos'] or cliente=='---':
                st.error('El nombre del cliente y el producto son obligatorios.')
            else:
                registrar_datos(
                    cliente = cliente,
                    tipo_cliente = tipo_cliente,
                    producto_cantidad = st.session_state['productos'],
                    fecha_registro = fecha_registro,
                    fecha_entrega = fecha_entrega,
                    hora_entrega = hora,
                    nota_orden = nota_orden,
                    ubicacion = ubicacion,
                    estado = 'Pendiente' 
                )
                print(f'{st.session_state['productos']}')
                limpiar_campos()
                st.success('La orden ha sido registrada exitosamente')

    