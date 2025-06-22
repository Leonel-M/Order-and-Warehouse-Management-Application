import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,time
import os

def ver_ordenes(ordenes, productos, detalles_ordenes):
    # Convertir y limpiar la columna Fecha_Entrega
    ordenes['Fecha_Entrega'] = pd.to_datetime(ordenes['Fecha_Entrega'], errors='coerce')
    ordenes = ordenes[ordenes['Fecha_Entrega'].notna()]
    if ordenes['Fecha_Entrega'].isna().any():
        st.error("Existen valores no válidos en la columna 'Fecha_Entrega'.")
        error_ingreso = ordenes[ordenes['Fecha_Entrega'].isna()]
        st.write(f' LOS PROBLEMAS SON: {error_ingreso}')
        return
    
    hoy = pd.Timestamp(datetime.now().date())

    #Visualización de las ordenes pendientes
    ordenes_pendientes = ordenes[(ordenes['Fecha_Entrega'] < hoy) & (ordenes['Estado'] == 'Pendiente')]
    st.markdown('### Ordenes Pendientes')
    if ordenes_pendientes.empty:
        st.info('No hay órdenes pendientes')
    else:
        ordenes_pendientes = ordenes_pendientes.sort_values(by=['Fecha_Entrega','Hora_Entrega'], ascending=True)
        st.dataframe(ordenes_pendientes)


    # Visualización de las órdenes del día
    ordenes_hoy = ordenes[ordenes['Fecha_Entrega'] == hoy]
    
    st.markdown(f'### Ordenes del dia ({hoy.strftime('%Y-%m-%d')})')
    if ordenes_hoy.empty:
        st.info('No hay órdenes para el día de hoy')
    else:
        
        if 'Orden_ID' in ordenes_hoy.columns and 'Orden_ID' in detalles_ordenes.columns:
            ordenes_hoy = pd.merge(ordenes_hoy, detalles_ordenes, on='Orden_ID', how='left')
        else:
            st.warning("La clave 'Orden_ID' no está presente en los DataFrames necesarios.")
            return

        if 'Producto_ID' in ordenes_hoy.columns and 'Producto_ID' in productos.columns:
            ordenes_productos = pd.merge(ordenes_hoy, productos, on='Producto_ID', how='left')
        else:
            st.warning("La clave 'Producto_ID' no está presente en los DataFrames necesarios.")
            ordenes_productos = ordenes_hoy

        # Verificar columnas necesarias
        required_columns = ['Orden_ID', 'Producto', 'Cantidad']
        
        for col in required_columns:
            if col not in ordenes_productos.columns:
                st.error(f"Falta la columna '{col}' en el DataFrame 'ordenes_productos'.")
                return        
        ordenes_productos['Producto_Cantidad'] = ordenes_productos.apply(
            lambda row: f"{row['Producto']} (x{row['Cantidad']})", axis=1
            )
        ordenes_productos['Nota_Orden'] = ordenes_productos['Nota_Orden'].fillna("Sin nota")
        fichas = ordenes_productos.groupby(
            ['Orden_ID', 'Fecha_Entrega', 'Cliente', 'Nota_Orden', 'Estado','Hora_Entrega']
        ).agg(
            Productos=('Producto_Cantidad',', '.join)
        ).reset_index()
        fichas = fichas.sort_values(by='Hora_Entrega')
        for _, fila in fichas.iterrows():
            st.markdown(f"""
            **Orden ID:** {fila['Orden_ID']}  
            **Hora de Entrega:** {datetime.strptime(fila['Hora_Entrega'], '%H:%M:%S').strftime('%H:%M')}  
            **Cliente:** {fila['Cliente']}  
            **Productos:** {fila['Productos']}  
            **Notas:** {fila['Nota_Orden']}  
            **Estado:** {fila['Estado']}
            """)

    # Visualización de la semana
    proximas_ordenes = ordenes[(ordenes['Estado'] == 'Pendiente') & (ordenes['Fecha_Entrega'] > hoy)]
    st.markdown('### Próximas Órdenes')
    if not proximas_ordenes.empty:
        proximas_ordenes = proximas_ordenes.sort_values(by=['Fecha_Entrega','Hora_Entrega'], ascending=True)
        st.dataframe(proximas_ordenes)
    else:
        st.info('No hay órdenes programadas.')
    
    # Formulario para modificar orden
    with st.form(key='cargar_orden'):
        st.markdown('## Modificar Orden') 
        orden = st.text_input('Número de Orden', value=st.session_state.get('num_orden', ''), placeholder='Ej. 125')
        submit_m_orden = st.form_submit_button('Cargar Orden')
        
        if submit_m_orden:
            st.session_state['num_orden'] = orden
            st.session_state['guardado_exitoso'] = False

    if st.session_state.get('num_orden'):
        if not st.session_state['num_orden'].isdigit():
            st.error('Ingresa un número válido')
        else:
            num_orden = int(st.session_state['num_orden'])
            if num_orden not in ordenes['Orden_ID'].values:
                st.error('El número no está en el registro de órdenes')
            else:
                datos_orden = ordenes[ordenes['Orden_ID'] == num_orden].iloc[0].to_dict()
                st.session_state['orden_info'] = datos_orden
    #Modificar Ordenes
    if st.session_state.get('orden_info') and any(st.session_state['orden_info'].values()):
        with st.form('form_modificar'):
            st.markdown(f"""
            ### Orden ID: {st.session_state['orden_info']['Orden_ID']}  
            **Cliente:** {st.session_state['orden_info']['Cliente']}
            """)           
            # Mostrar productos asociados a la orden
            orden_id_actual = st.session_state['orden_info']['Orden_ID']
            productos_detalles = detalles_ordenes[detalles_ordenes['Orden_ID'] == orden_id_actual]
            productos_orden = pd.merge(productos_detalles,productos,on='Producto_ID',how='left')

            productos_list = productos_orden.apply(
                lambda row: f'{row['Producto']} (x{row['Cantidad']})', axis=1).tolist()
            
            st.write("**Productos asociados:**")
            for producto in productos_list:
                st.write(f"- {producto}")
            col1,col2 = st.columns([1,2])
            with col1:
                # Fecha de Entrega
                fecha_entrega = st.session_state['orden_info']['Fecha_Entrega']
                fecha_entrega = pd.to_datetime(fecha_entrega) if fecha_entrega else hoy
                fecha_entrega_input = st.date_input(
                    'Fecha de Entrega',
                    value=fecha_entrega,
                    format='DD/MM/YYYY',
                    key='Fecha_Entrega'
                )
            with col2:
                # Hora de Entrega
                hora_entrega_str = st.session_state['orden_info']['Hora_Entrega']
                hora_entrega = (
                    datetime.strptime(hora_entrega_str, '%H:%M:%S').time()
                    if hora_entrega_str else time(7, 0)
                )
                hora_entrega_input = st.slider(
                    "Hora de Entrega:",
                    min_value=time(7, 0),
                    max_value=time(20, 0),
                    step=timedelta(hours=1),
                    format="HH:mm:ss",
                    value=hora_entrega,
                    key='Hora_Entrega'
                )

            # Notas
            nota_orden = st.session_state['orden_info']['Nota_Orden']
            nota_orden_input = st.text_area("Notas", value=nota_orden, key='Nota_Orden')

            # Estado
            estado_actual = st.session_state['orden_info']['Estado']
            estado_input = st.selectbox("Estado", ['Pendiente', 'Completado','Incompleto','No entregado'], index=['Pendiente', 'Completado','Incompleto','No entregado'].index(estado_actual) if estado_actual in ['Pendiente', 'Completado','Incompleto','No entregado'] else 0, key='Estado')

            submit_modificar = st.form_submit_button('Guardar Cambios')

            # Actualización de los datos 
            if submit_modificar and not st.session_state.get('guardado_exitoso', False):
                orden_id = st.session_state['orden_info']['Orden_ID']
                if orden_id is not None:
                    # Actualizar Fecha_Entrega
                    fecha_entrega_str = fecha_entrega_input.strftime('%Y-%m-%d')
                    ordenes.loc[ordenes['Orden_ID'] == orden_id, 'Fecha_Entrega'] = fecha_entrega_str

                    # Actualizar Hora_Entrega
                    hora_entrega_str = hora_entrega_input.strftime('%H:%M:%S')
                    ordenes.loc[ordenes['Orden_ID'] == orden_id, 'Hora_Entrega'] = hora_entrega_str

                    # Actualizar Notas
                    ordenes.loc[ordenes['Orden_ID'] == orden_id, 'Nota_Orden'] = nota_orden_input

                    # Actualizar Estado
                    ordenes.loc[ordenes['Orden_ID'] == orden_id, 'Estado'] = estado_input

                    # Guardar cambios
                    ruta_ordenes = os.path.join('datos', 'ordenes.csv')    
                    ordenes.to_csv(ruta_ordenes, index=False)

                    st.session_state['guardado_exitoso'] = True
                    st.success('La orden ha sido actualizada')
                else:
                    st.error('No se pudo identificar la Orden para actualizar')
def info_ordenes(ordenes,productos,detalles_ordenes):
    st.markdown(f'### Ordenes')
    #Convertir fecha de registro en datetime
    if ('Fecha_Registro' and 'Fecha_Entrega') in ordenes.columns:
        ordenes['Fecha_Registro'] = pd.to_datetime(ordenes['Fecha_Registro'], errors='coerce')
        ordenes['Fecha_Entrega'] = pd.to_datetime(ordenes['Fecha_Entrega'], errors='coerce')
    # Elimina filas con fechas inválidas
    ordenes = ordenes.dropna(subset=['Fecha_Registro', 'Fecha_Entrega'])

    
    fecha_actual = datetime.today()
    fecha_limite = fecha_actual - timedelta(days=90)

    # Distribución menual de ordenes
    df_dist_mensual = ordenes
    df_dist_mensual['Ano'] = ordenes['Fecha_Registro'].dt.year
    df_dist_mensual['Mes'] = ordenes['Fecha_Registro'].dt.month
    distribucion = df_dist_mensual.groupby(['Ano','Mes']).size().reset_index(name='Cantidad_Ordenes')
    distribucion = distribucion.sort_values(by=['Ano','Mes'])

    fig, ax=plt.subplots(figsize=(10,6))
    ax.plot(distribucion['Mes'],
             distribucion['Cantidad_Ordenes'],
             marker='o')
    ax.set_xticks(range(1, 13))
    ax.set_title('Distribución Mensual de Ordenes', fontsize=14)
    ax.set_xlabel('Mes', fontsize=12)
    ax.set_ylabel('Cantidad de Órdenes', fontsize=12)
    ax.grid(True)
    st.pyplot(fig)
    st.markdown(f'### CLientes y Estados los ultimos 90 dias')
    #Clientes con más pedidos los ultimos 90 días
    df_cliente_90d = ordenes[ordenes['Fecha_Registro'] >= fecha_limite]
    frecuencia_clientes =df_cliente_90d['Cliente'].value_counts()

    sns.set_style('whitegrid')

    fig, ax=plt.subplots(figsize=(10,6))
    sns.barplot(x=frecuencia_clientes.head(10).index,
                y=frecuencia_clientes.head(10).values,
                palette='Blues_r')
    ax.set_title('Clientes con mas pedidos en los ultimos 90 dias', fontsize=12)
    ax.set_xlabel('Cliente', fontsize=6)
    ax.set_ylabel('Cantidad de Ordenes', fontsize=6)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    #Torta de 'ESTADO'
    estado_counts = df_cliente_90d['Estado'].value_counts()
    
    fig, ax =plt.subplots(figsize=(10,6))
    colores = sns.color_palette('pastel')[0:len(estado_counts)]
    ax.pie(estado_counts, labels=estado_counts.index, colors=colores, autopct='%1.1f%%',startangle=90)
    ax.set_title('Distribucion de Ordenes por "Estado" en los ultimos 90 dias', fontsize=10)
    st.pyplot(fig)

    
def visualizacion_tab():
    st.title('Visualizacion de Datos')
    if not 'tipo_datos' in st.session_state:
        st.session_state['tipo_datos']=''    

    with st.form('menu_visualizacion'):    
        tipo_datos = st.selectbox('Tipo de Datos', ['---','Ordenes','Informe de ordenes'])
        submit = st.form_submit_button('Seleccionar Data')

        if submit:
            if tipo_datos == '---':
                st.error('Seleccione los datos')
            else:
                st.session_state['tipo_datos'] = tipo_datos

    #Tomamos los datos del CSV que queremos
    ruta_ordenes = os.path.join('datos', 'ordenes.csv')    
    ordenes = pd.read_csv(ruta_ordenes)
    ruta_productos = os.path.join('datos', 'productos.csv')    
    productos = pd.read_csv(ruta_productos)
    ruta_almacen = os.path.join('datos', 'almacen.csv')    
    almacen = pd.read_csv(ruta_almacen)
    ruta_clientes = os.path.join('datos', 'clientes.csv')    
    clientes = pd.read_csv(ruta_clientes)
    ruta_detalles_ordenes = os.path.join('datos', 'detalles_ordenes.csv')    
    detalles_ordenes = pd.read_csv(ruta_detalles_ordenes)
    ruta_material = os.path.join('datos', 'material.csv')    
    material = pd.read_csv(ruta_material)

    match st.session_state['tipo_datos']:
        case 'Ordenes':
            ver_ordenes(ordenes,productos,detalles_ordenes)
        case 'Informe de ordenes':
            info_ordenes(ordenes,productos,detalles_ordenes)
