# Importar librerías necesarias
import mysql.connector
from datetime import datetime

# =============================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =============================================

# Datos de conexión a Clever Cloud (cambiar por tus datos reales)
config_bd = {
    'host': 'tu_host_de_clever_cloud',
    'database': 'panol_herramientas', 
    'user': 'tu_usuario',
    'password': 'tu_contraseña'
}

# =============================================
# FUNCIONES PARA CONECTAR A LA BASE DE DATOS
# =============================================

def conectar_bd():
    """Conectar a la base de datos MySQL"""
    conexion = mysql.connector.connect(**config_bd)
    return conexion

def desconectar_bd(conexion):
    """Cerrar la conexión a la base de datos"""
    conexion.close()

# =============================================
# FUNCIONES PARA MOSTRAR INFORMACIÓN
# =============================================

def mostrar_menu_principal():
    """Mostrar el menú principal del sistema"""
    print("\n" + "="*40)
    print("    SISTEMA GESTIÓN DE PAÑOL")
    print("="*40)
    print("1. VER todas las herramientas")
    print("2. AGREGAR nueva herramienta") 
    print("3. CAMBIAR estado de herramienta")
    print("4. ELIMINAR herramienta")
    print("5. VER personas registradas")
    print("6. AGREGAR nueva persona")
    print("7. REGISTRAR préstamo")
    print("8. REGISTRAR devolución")
    print("9. VER préstamos activos")
    print("0. SALIR del sistema")
    print("="*40)

def listar_herramientas():
    """Mostrar todas las herramientas en una tabla"""
    # Conectar a la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Consulta SQL para obtener todas las herramientas
    sql = """
        SELECT h.id, h.nombre, h.marca, h.modelo, c.nombre, h.estado 
        FROM herramientas h 
        LEFT JOIN categorias c ON h.id_categoria = c.id
        ORDER BY h.id
    """
    
    # Ejecutar la consulta
    cursor.execute(sql)
    
    # Obtener todos los resultados
    herramientas = cursor.fetchall()
    
    # Mostrar encabezado de la tabla
    print("\n--- LISTA DE HERRAMIENTAS ---")
    print("ID  Nombre              Marca       Modelo      Categoría           Estado")
    print("-" * 80)
    
    # Mostrar cada herramienta en una fila
    for herramienta in herramientas:
        print(f"{herramienta[0]:<3} {herramienta[1]:<18} {herramienta[2]:<11} {herramienta[3]:<11} {herramienta[4]:<18} {herramienta[5]:<15}")
    
    # Cerrar conexión
    cursor.close()
    desconectar_bd(conexion)

def listar_personas():
    """Mostrar todas las personas registradas"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Consulta para obtener todas las personas
    sql = "SELECT id, nombre, departamento, email FROM personas ORDER BY id"
    cursor.execute(sql)
    personas = cursor.fetchall()
    
    print("\n--- PERSONAS REGISTRADAS ---")
    print("ID  Nombre              Departamento  Email")
    print("-" * 60)
    
    for persona in personas:
        print(f"{persona[0]:<3} {persona[1]:<18} {persona[2]:<13} {persona[3]:<20}")
    
    cursor.close()
    desconectar_bd(conexion)

# =============================================
# FUNCIONES PARA AGREGAR DATOS
# =============================================

def agregar_herramienta():
    """Agregar una nueva herramienta al sistema"""
    print("\n--- AGREGAR NUEVA HERRAMIENTA ---")
    
    # Pedir datos al usuario
    nombre = input("Nombre de la herramienta: ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    
    # Mostrar categorías disponibles
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM categorias")
    categorias = cursor.fetchall()
    
    print("\nCategorías disponibles:")
    for categoria in categorias:
        print(f"{categoria[0]}. {categoria[1]}")
    
    categoria_id = input("ID de la categoría: ")
    
    # Consulta SQL para insertar nueva herramienta
    sql = "INSERT INTO herramientas (nombre, marca, modelo, id_categoria, estado) VALUES (%s, %s, %s, %s, 'Disponible')"
    datos = (nombre, marca, modelo, categoria_id)
    
    # Ejecutar la inserción
    cursor.execute(sql, datos)
    conexion.commit()  # Guardar cambios en la base de datos
    
    print("✅ Herramienta agregada correctamente")
    
    cursor.close()
    desconectar_bd(conexion)

def agregar_persona():
    """Agregar una nueva persona al sistema"""
    print("\n--- AGREGAR NUEVA PERSONA ---")
    
    # Pedir datos al usuario
    nombre = input("Nombre completo: ")
    departamento = input("Departamento: ")
    email = input("Email: ")
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Consulta para insertar nueva persona
    sql = "INSERT INTO personas (nombre, departamento, email) VALUES (%s, %s, %s)"
    datos = (nombre, departamento, email)
    
    cursor.execute(sql, datos)
    conexion.commit()
    
    print("✅ Persona agregada correctamente")
    
    cursor.close()
    desconectar_bd(conexion)

# =============================================
# FUNCIONES PARA ACTUALIZAR DATOS
# =============================================

def actualizar_estado_herramienta():
    """Cambiar el estado de una herramienta"""
    # Primero mostrar todas las herramientas
    listar_herramientas()
    
    print("\n--- CAMBIAR ESTADO DE HERRAMIENTA ---")
    herramienta_id = input("ID de la herramienta a actualizar: ")
    
    # Mostrar opciones de estado
    print("\Opciones de estado:")
    print("1. Disponible")
    print("2. Prestado") 
    print("3. En mantenimiento")
    print("4. Dañado")
    
    opcion = input("Seleccione opción (1-4): ")
    
    # Convertir opción a estado
    if opcion == "1":
        nuevo_estado = "Disponible"
    elif opcion == "2":
        nuevo_estado = "Prestado"
    elif opcion == "3":
        nuevo_estado = "Mantenimiento" 
    elif opcion == "4":
        nuevo_estado = "Dañado"
    else:
        print("❌ Opción inválida")
        return
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Consulta para actualizar el estado
    sql = "UPDATE herramientas SET estado = %s WHERE id = %s"
    datos = (nuevo_estado, herramienta_id)
    
    cursor.execute(sql, datos)
    conexion.commit()
    
    print(f"✅ Estado actualizado a: {nuevo_estado}")
    
    cursor.close()
    desconectar_bd(conexion)

# =============================================
# FUNCIONES PARA ELIMINAR DATOS
# =============================================

def eliminar_herramienta():
    """Eliminar una herramienta del sistema"""
    # Mostrar herramientas primero
    listar_herramientas()
    
    print("\n--- ELIMINAR HERRAMIENTA ---")
    herramienta_id = input("ID de la herramienta a eliminar: ")
    
    # Pedir confirmación
    confirmar = input("¿Está seguro de eliminar? (s/n): ")
    
    if confirmar.lower() == "s":
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        # Consulta para eliminar
        sql = "DELETE FROM herramientas WHERE id = %s"
        
        cursor.execute(sql, (herramienta_id,))
        conexion.commit()
        
        print("✅ Herramienta eliminada correctamente")
        
        cursor.close()
        desconectar_bd(conexion)
    else:
        print("❌ Eliminación cancelada")

# =============================================
# FUNCIONES PARA PRÉSTAMOS
# =============================================

def registrar_prestamo():
    """Registrar el préstamo de una herramienta"""
    print("\n--- REGISTRAR PRÉSTAMO ---")
    
    # Mostrar herramientas disponibles
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Buscar herramientas con estado "Disponible"
    cursor.execute("SELECT id, nombre FROM herramientas WHERE estado = 'Disponible'")
    herramientas_disp = cursor.fetchall()
    
    if not herramientas_disp:
        print("❌ No hay herramientas disponibles")
        cursor.close()
        desconectar_bd(conexion)
        return
    
    print("Herramientas disponibles:")
    for herramienta in herramientas_disp:
        print(f"{herramienta[0]}. {herramienta[1]}")
    
    herramienta_id = input("ID de la herramienta: ")
    
    # Mostrar personas
    listar_personas()
    persona_id = input("ID de la persona: ")
    
    # Obtener fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Insertar préstamo
    sql_prestamo = "INSERT INTO prestamos (id_herramienta, id_persona, fecha_prestamo) VALUES (%s, %s, %s)"
    datos_prestamo = (herramienta_id, persona_id, fecha_actual)
    cursor.execute(sql_prestamo, datos_prestamo)
    
    # Cambiar estado de la herramienta a "Prestado"
    sql_estado = "UPDATE herramientas SET estado = 'Prestado' WHERE id = %s"
    cursor.execute(sql_estado, (herramienta_id,))
    
    conexion.commit()
    print("✅ Préstamo registrado correctamente")
    
    cursor.close()
    desconectar_bd(conexion)

def registrar_devolucion():
    """Registrar la devolución de una herramienta"""
    print("\n--- REGISTRAR DEVOLUCIÓN ---")
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Buscar préstamos activos (sin fecha de devolución)
    sql_prestamos = """
        SELECT p.id, h.nombre, per.nombre 
        FROM prestamos p
        JOIN herramientas h ON p.id_herramienta = h.id
        JOIN personas per ON p.id_persona = per.id
        WHERE p.fecha_devolucion IS NULL
    """
    cursor.execute(sql_prestamos)
    prestamos_activos = cursor.fetchall()
    
    if not prestamos_activos:
        print("✅ No hay préstamos activos")
        cursor.close()
        desconectar_bd(conexion)
        return
    
    print("Préstamos activos:")
    for prestamo in prestamos_activos:
        print(f"{prestamo[0]}. {prestamo[1]} - {prestamo[2]}")
    
    prestamo_id = input("ID del préstamo a devolver: ")
    
    # Obtener ID de la herramienta para este préstamo
    cursor.execute("SELECT id_herramienta FROM prestamos WHERE id = %s", (prestamo_id,))
    resultado = cursor.fetchone()
    herramienta_id = resultado[0]
    
    # Obtener fecha actual para la devolución
    fecha_devolucion = datetime.now().strftime("%Y-%m-%d")
    
    # Actualizar préstamo con fecha de devolución
    sql_actualizar = "UPDATE prestamos SET fecha_devolucion = %s WHERE id = %s"
    cursor.execute(sql_actualizar, (fecha_devolucion, prestamo_id))
    
    # Cambiar estado de la herramienta a "Disponible"
    sql_estado = "UPDATE herramientas SET estado = 'Disponible' WHERE id = %s"
    cursor.execute(sql_estado, (herramienta_id,))
    
    conexion.commit()
    print("✅ Devolución registrada correctamente")
    
    cursor.close()
    desconectar_bd(conexion)

def ver_prestamos_activos():
    """Mostrar todos los préstamos que están activos"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Consulta para préstamos activos (sin fecha de devolución)
    sql = """
        SELECT p.id, h.nombre, per.nombre, p.fecha_prestamo
        FROM prestamos p
        JOIN herramientas h ON p.id_herramienta = h.id
        JOIN personas per ON p.id_persona = per.id
        WHERE p.fecha_devolucion IS NULL
    """
    cursor.execute(sql)
    prestamos = cursor.fetchall()
    
    print("\n--- PRÉSTAMOS ACTIVOS ---")
    print("ID  Herramienta          Persona               Fecha Préstamo")
    print("-" * 60)
    
    for prestamo in prestamos:
        print(f"{prestamo[0]:<3} {prestamo[1]:<20} {prestamo[2]:<20} {prestamo[3]}")
    
    cursor.close()
    desconectar_bd(conexion)

# =============================================
# PROGRAMA PRINCIPAL
# =============================================

def main():
    """Función principal que ejecuta el sistema"""
    print("🔧 SISTEMA DE GESTIÓN DE PAÑOL")
    print("Conectando a la base de datos...")
    
    # Probar la conexión
    try:
        conexion_prueba = conectar_bd()
        print("✅ Conexión exitosa a la base de datos")
        desconectar_bd(conexion_prueba)
    except:
        print("❌ Error: No se pudo conectar a la base de datos")
        print("Verifique la configuración en el código")
        return
    
    # Bucle principal del programa
    while True:
        # Mostrar menú
        mostrar_menu_principal()
        
        # Leer opción del usuario
        opcion = input("Seleccione una opción: ")
        
        # Ejecutar función según la opción seleccionada
        if opcion == "1":
            listar_herramientas()
        elif opcion == "2":
            agregar_herramienta()
        elif opcion == "3":
            actualizar_estado_herramienta()
        elif opcion == "4":
            eliminar_herramienta()
        elif opcion == "5":
            listar_personas()
        elif opcion == "6":
            agregar_persona()
        elif opcion == "7":
            registrar_prestamo()
        elif opcion == "8":
            registrar_devolucion()
        elif opcion == "9":
            ver_prestamos_activos()
        elif opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida, intente nuevamente")
        
        # Pausa antes de mostrar el menú again
        input("\nPresione Enter para continuar...")

# =============================================
# INICIAR EL PROGRAMA
# =============================================

# Este if asegura que el programa solo se ejecute cuando se llama directamente
if __name__ == "__main__":
    main()