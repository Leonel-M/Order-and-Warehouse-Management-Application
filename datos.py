import os
from datetime import datetime, date
import pandas as pd

def documentos():
    carpeta = 'datos'

    #verificar 'datos'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        print(f'Carpeta "{carpeta}" creada con éxito')
    
    #listas de archivos y sus columnas iniciales
    archivos = {
        'clientes.csv': ['Cliente_ID', 'Nombre', 'Tipo_Cliente', 'Ubicacion','Telefono'],
        'productos.csv':['Producto_ID','Producto'],
        'ordenes.csv': ['Orden_ID','Cliente','Tipo_Cliente','Prioridad','Tipo_Pago','Fecha_Registro','Fecha_Entrega','Hora_Entrega','Nota_Orden','Ubicacion','Estado'],
        'detalles_ordenes.csv': ['Orden_ID','Producto_ID','Cantidad'],
        'material.csv':['SKU','Material','Categoria'],
        'almacen.csv': [
            "Almacen_ID",             # Numero de registro unico
            "Tipo_Registro",          # Entrada o Salida
            "SKU",                    # Identificador único del material
            "Material",               # Nombre del material (solo para entradas)
            "Categoria",              # Tipo de material (solo para entradas)
            "Cantidad",               # Número de unidades (positivo para entradas, negativo para salidas)
            "Precio_Unitario",        # Costo por unidad (solo para entradas)
            "Fecha",                  # Fecha del registro
            "Proveedor",              # Nombre del proveedor (solo para entradas)
            "Usuario",                # Persona o departamento (solo para salidas)
            "Ubicacion",              # Lugar físico en el almacén
            "Notas"                   # Información adicional
            ]
    }

    #Verifica o crea los archivos
    for archivo, columnas in archivos.items():
        ruta = os.path.join(carpeta, archivo)
        if not os.path.exists(ruta):
            # DF vacio con las columnas iniciales
            df = pd.DataFrame(columns=columnas)
            #guardar DF como CSV
            df.to_csv(ruta, index=False)
            print(f'Archivo "{archivo}" creado con las columnas: {', '.join(columnas)}')
        #else:
            #print(f'El archivo "{archivo}" ya existe.')

def registrar_cliente(cliente):
    #Ruta del archivo
    ruta_archivo = os.path.join('datos','clientes.csv')
    
    #Verificamos que exista el documento
    if os.path.exists(ruta_archivo):
        clientes_df = pd.read_csv(ruta_archivo)
    else:
        clientes_df = pd.DataFrame(columns=['Cliente_ID','Nombre'])
        
    #Verificamos si el cliente existe
    if cliente in clientes_df['Nombre'].values:
        print(f'El cliente "{cliente}" ya existe en el sistema')
        cliente_id = clientes_df.loc[clientes_df['Nombre'] == cliente, 'Cliente_ID'].values[0]
    else:
        #Crear un ID único
        nuevo_id = len(clientes_df) + 1
        nuevo_cliente = {'Cliente_ID': nuevo_id, 'Nombre': cliente}
        clientes_df = pd.concat([clientes_df,pd.DataFrame([nuevo_cliente])], ignore_index=True)
        clientes_df.to_csv(ruta_archivo, index=False)
        print(f'Nuevo cliente agregado: {cliente} con ID {nuevo_id}')
        cliente_id = nuevo_id
    return cliente_id

def registrar_producto(producto_cantidad):
    #Ruta del archivo
    ruta_archivo = os.path.join('datos','productos.csv')

    #Verificamos que exista el documento
    if os.path.exists(ruta_archivo):
        productos_df = pd.read_csv(ruta_archivo)
    else:
        productos_df = pd.DataFrame(columns=['Producto_ID','Producto'])
    
    #verificamos si los productos existen
    producto_id = {}
    
    #Eliminar duplicados en la lista de entradad
    productos_unicos = {item['producto'] for item in producto_cantidad}

    for producto in productos_unicos:
        if producto in productos_df['Producto'].values: # si existe obtenemos la ID
            print(f'El producto "{producto}" ya existe en el sistema.')
            producto_id[producto] = productos_df.loc[productos_df['Producto'] == producto, 'Producto_ID'].values[0]
        else: # si no existe creamos ID y agregamos 
            nuevo_id = len(productos_df) + 1
            nuevo_producto = {'Producto_ID': nuevo_id, 'Producto': producto}
            productos_df = pd.concat([productos_df, pd.DataFrame([nuevo_producto])], ignore_index=True)
            print(f'Nuevo producto agregado: {producto} con ID {nuevo_id}')
            producto_id[producto]=nuevo_id    

    productos_df.to_csv(ruta_archivo, index=False)
    return producto_id

def registrar_orden(cliente,tipo_cliente,producto_id,producto_cantidad,prioridad,
                    tipo_pago,fecha_registro,fecha_entrega,hora_entrega,nota_orden,ubicacion,estado):

    #Ruta del archivo
    ruta_ordenes = os.path.join('datos','ordenes.csv')
    #Verificamos que exista el documento
    if os.path.exists(ruta_ordenes):
        orden_df = pd.read_csv(ruta_ordenes)
    else:
        orden_df = pd.DataFrame(columns=[
            'Orden_ID',
            'Cliente',
            'Tipo_Cliente',
            'Prioridad',
            'Tipo_Pago',
            'Fecha_Registro',
            'Fecha_Entrega',
            'Hora_Entrega'
            'Nota_Orden',
            'Ubicacion',
            'Estado'
        ])
    #Generamos la ID unica de la orden
    if not orden_df.empty:
        orden_id = orden_df['Orden_ID'].max() + 1 
    else:
        orden_id = 1   
    
    #Fechas y tipo de variable
    if isinstance(fecha_registro, date):
        fecha_registro_dt = fecha_registro
    else: 
        fecha_registro_dt = datetime.strptime(fecha_registro, '%d/%m/%Y').date()  # Formato día/mes/año
    
    if isinstance(fecha_entrega, date):
        fecha_entrega_dt = fecha_entrega
    else: 
        fecha_entrega_dt = datetime.strptime(fecha_entrega, '%d/%m/%Y').date()  # Formato día/mes/año

    #Creamos la Orden
    nueva_orden ={
        'Orden_ID': orden_id,
        'Cliente':cliente,
        'Tipo_Cliente':tipo_cliente,
        'Prioridad': prioridad,
        'Tipo_Pago':tipo_pago,
        'Fecha_Registro':fecha_registro_dt,
        'Fecha_Entrega':fecha_entrega_dt,
        'Hora_Entrega':hora_entrega,
        'Nota_Orden':nota_orden,
        'Ubicacion':ubicacion,
        'Estado':estado}
    orden_df = pd.concat([orden_df, pd.DataFrame([nueva_orden])], ignore_index=True)
    orden_df.to_csv(ruta_ordenes, index=False)
    
    #Creamos los detalles de orden
    #Ruta del archivo
    ruta_detalles = os.path.join('datos','detalles_ordenes.csv')
    #Verificamos que exista el documento
    if os.path.exists(ruta_detalles):
        detalles_df = pd.read_csv(ruta_detalles)
    else:
        detalles_df = pd.DataFrame(columns=[
            'Orden_ID',
            'Producto_ID',
            'Cantidad'
        ])
    
    nuevo_detalles = []
    for item in producto_cantidad:
        nuevo_detalles.append({
            'Orden_ID': int(orden_id),
            'Producto_ID':int(producto_id[item['producto']]),
            'Cantidad':int(item['cantidad']) 
        })
    print(f'Nuevo Detalles: {nuevo_detalles}\n\n')
    nuevo_detalles_df = pd.DataFrame(nuevo_detalles,columns=['Orden_ID', 'Producto_ID', 'Cantidad'])
    detalles_df = pd.concat([detalles_df,nuevo_detalles_df], ignore_index=True)
    detalles_df.to_csv(ruta_detalles, index=False)
    return

def registrar_datos(cliente,tipo_cliente,producto_cantidad,
                    prioridad,tipo_pago,fecha_registro,fecha_entrega,hora_entrega,nota_orden,ubicacion,estado):

    cliente_id = registrar_cliente(cliente)
    producto_id = registrar_producto(producto_cantidad)
    registrar_orden(cliente,tipo_cliente,producto_id,producto_cantidad,prioridad,tipo_pago,fecha_registro,fecha_entrega,hora_entrega,nota_orden,ubicacion,estado)

    return #print(f'cliente ID {cliente_id} y producto ID {producto_id}')

def registrar_almacen(Tipo_Registro,SKU,Material,Categoria,Cantidad,Precio_Unitario,Fecha,Proveedor,Usuario,Ubicacion,Notas):
        #Ruta del archivo
    ruta_almacen = os.path.join('datos','almacen.csv')
    ruta_material = os.path.join('datos','material.csv')
    #Verificamos que exista el documento
    if os.path.exists(ruta_almacen):
        almacen_df = pd.read_csv(ruta_almacen)
    else:
        almacen_df = pd.DataFrame(columns=[
            "Almacen_ID",             # Numero de registro unico
            "Tipo_Registro",          # Entrada o Salida
            "SKU",                    # Identificador único del material
            "Material",               # Nombre del material (solo para entradas)
            "Categoria",              # Tipo de material (solo para entradas)
            "Cantidad",               # Número de unidades (positivo para entradas, negativo para salidas)
            "Precio_Unitario",        # Costo por unidad (solo para entradas)
            "Fecha",                  # Fecha del registro
            "Proveedor",              # Nombre del proveedor (solo para entradas)
            "Usuario",                # Persona o departamento (solo para salidas)
            "Ubicacion",              # Lugar físico en el almacén
            "Notas"                   # Información adicional
        ])
    
    Almacen_ID = len(almacen_df)+1

    if Tipo_Registro == 'Entrada':
        nueva_entrada = {
            "Almacen_ID": Almacen_ID,
            "Tipo_Registro": Tipo_Registro,
            "SKU": SKU,
            "Material": Material,
            "Categoria": Categoria,
            "Cantidad": Cantidad,
            "Precio_Unitario": Precio_Unitario,
            "Fecha": Fecha,
            "Proveedor": Proveedor,
            "Usuario": None,  # No aplica para entradas
            "Ubicacion": Ubicacion,
            "Notas": Notas
        }
        almacen_df = pd.concat([almacen_df, pd.DataFrame([nueva_entrada])], ignore_index=True)
        

    elif Tipo_Registro == 'Salida':
        nueva_salida = {
            "Almacen_ID": Almacen_ID,
            "Tipo_Registro": Tipo_Registro,
            "SKU": SKU,
            "Material": None,  # No aplica para salidas
            "Categoria": None,  # No aplica para salidas
            "Cantidad": -Cantidad,
            "Precio_Unitario": None,  # No aplica para salidas
            "Fecha": Fecha,
            "Proveedor": None,  # No aplica para salidas
            "Usuario": Usuario,
            "Ubicacion": None, # No aplica para salidas
            "Notas": Notas
            }
        almacen_df = pd.concat([almacen_df, pd.DataFrame([nueva_salida])], ignore_index=True)
    else:
        print("Error: Tipo de registro no válido (debe ser 'Entrada' o 'Salida').")
        # Guardar el DataFrame actualizado
    try:
        almacen_df.to_csv(ruta_almacen, index=False)
        print(f"Registro {Tipo_Registro} añadido exitosamente.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
    
    #CODIGOS SKU Y MATERIAL
    if os.path.exists(ruta_material):
        material_df = pd.read_csv(ruta_material)
    else:
        material_df = pd.DataFrame(columns=['SKU','Material'])
    
    # Verificar si el SKU ya existe en material_df
    if not material_df['SKU'].str.contains(SKU).any():
        # Crear un nuevo registro para el material
        nuevo_material = {
            "SKU": SKU,
            "Material": Material
        }
        # Agregar el nuevo material al DataFrame
        material_df = pd.concat([material_df, pd.DataFrame([nuevo_material])], ignore_index=True)
        
        # Guardar el DataFrame actualizado en el archivo material.csv
    try:
        material_df.to_csv(ruta_material, index=False)
        print(f"Nuevo material registrado: SKU={SKU}, Material={Material}")
    except Exception as e:
        print(f"Error al guardar el archivo de materiales: {e}")
    else:
        print(f"El SKU {SKU} ya está registrado en material.csv.")


    return