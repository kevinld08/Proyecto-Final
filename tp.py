import sqlite3
 
from datetime import datetime
def conectar():
    conexion = sqlite3.connect('admin_universidad.db')
    return conexion

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('''
     CREATE TABLE IF NOT EXISTS alumnos (
     id_alumno INTEGER PRIMARY KEY AUTOINCREMENT,
     nombre TEXT(15) NOT NULL,
     apellido TEXT(15) NOT NULL,
     dni TEXT(10) NOT NULL);''')
   
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS datos_de_alumnos (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_alumno INTEGER NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono TEXT(15) NOT NULL,
    domicilio TEXT(20) NOT NULL,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno) ON DELETE CASCADE
);
    ''')
    conexion.commit()
    conexion.close()
crear_tabla()

def agregar_alumno(nombre, apellido, dni, fecha_nacimiento, telefono, domicilio): 
    conexion = conectar() 
    cursor = conexion.cursor() 
     
    cursor.execute(''' INSERT INTO alumnos (nombre, apellido, dni) VALUES (?, ?, ?) ''',
    (nombre, apellido, dni)) 
    id_alumno = cursor.lastrowid  

    cursor.execute(''' INSERT INTO datos_de_alumnos (id_alumno, fecha_nacimiento, telefono, domicilio) VALUES (?, ?, ?, ?) ''',
    (id_alumno, fecha_nacimiento, telefono, domicilio)) 
    
    conexion.commit()
    conexion.close()

def pedir_datos():
     
    while True:
        nombre = input("Ingrese el nombre: \n").capitalize()
    
         
        if nombre.isalpha():
            break  
        else:
            print("El nombre no puede contenen numeros y tampoco se puede dejar espacio vacio.")
    while True:
        apellido = input("Ingrese el apellido\n").capitalize()
        if  apellido.isalpha():
            break  
        else:
            print("El apellido no puede contenen numeros y tampoco se puede dejar espacio vacio.")
    while True:
        dni = input("Ingrese el dni\n")
        cantidad=len(dni)

        if dni.isdigit() and cantidad==8:
            
            break
        else:
            print("El dni no puede contener letras y tiene que tener 8 numeros")
    while True:
  
        fecha_nacimiento = input("Ingrese fecha de nacimiento (dd/mm/aaaa): ")
        try:
             
            fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
            fecha_nacimiento= fecha_nacimiento_obj.strftime("%Y-%m-%d")

            
            fecha_actual = datetime.now()

         
            Edad_minima = datetime(fecha_actual.year - 18, fecha_actual.month, fecha_actual.day)
            Edad_maxima = datetime(fecha_actual.year - 100, fecha_actual.month, fecha_actual.day)

           
            if fecha_nacimiento_obj > fecha_actual:
                print("La fecha de nacimiento no puede ser posterior a la fecha de hoy. Intenta nuevamente.")
            
           
            elif fecha_nacimiento_obj > Edad_minima:
                print("La persona debe tener al menos 18 años.")
            
          
            elif fecha_nacimiento_obj < Edad_maxima:
                print("La persona no puede tener más de 100 años.")
            
            else:
                
                 
                break  

        except ValueError:
           
            print("Formato de fecha inválido. Asegúrese de usar dd/mm/aaaa.")
    while True:
        telefono = input("Ingrese numero de telefono\n")
        cantidad=len(telefono)
         
        if telefono.isdigit() and cantidad >= 8 and cantidad <= 12:
             
             break  
        elif not telefono.isdigit() or telefono == "":
             print("No puede contener letras y tampoco se puede dejar en blanco.")
        else:
            print("El número de teléfono ingresado tiene que tener entre 8 y 12 números.")
    
    while True:
        domicilio = input("Ingrese su dirección: ").capitalize()

        contiene_letra = False
        contiene_numero = False

       
        for c in domicilio:
            if c.isalpha(): 
                contiene_letra = True
            if c.isdigit():  
                contiene_numero = True

 
        if contiene_letra and contiene_numero:
             
            break  
        else:
            print("La direccion tiene que contener letras y numeros.")

    agregar_alumno(nombre, apellido, dni, fecha_nacimiento, telefono, domicilio)
    print("El alumno fue agregado")

def mostrar_datos():
    conexion = conectar()
    cursor = conexion.cursor()

     
    cursor.execute('''
    SELECT a.id_alumno, a.nombre, a.apellido, a.dni, d.fecha_nacimiento, d.telefono, d.domicilio
    FROM alumnos a
    INNER JOIN datos_de_alumnos d ON a.id_alumno = d.id_alumno
    ''')
    alumnos = cursor.fetchall()
    conexion.close()
    
   
    print(f"{'ID':<10}{'Nombre':<20}{'Apellido':<20}{'DNI':<15}{'Fecha de Nacimiento':<20}{'Teléfono':<15}{'Domicilio':<30}")
    print("="*115)  
    
  
    for alumno in alumnos:
       
        print(f"{alumno[0]:<10}{alumno[1]:<20}{alumno[2]:<20}{alumno[3]:<15}{alumno[4]:<20}{alumno[5]:<15}{alumno[6]:<30}")

def actualizar(dni):
    conexion = conectar()
    cursor = conexion.cursor()

    
    cursor.execute('''
    SELECT a.id_alumno, a.nombre, a.apellido, a.dni, d.fecha_nacimiento, d.telefono, d.domicilio
    FROM alumnos a
    INNER JOIN datos_de_alumnos d ON a.id_alumno = d.id_alumno
    WHERE a.dni = ?
    ''', (dni,))

    alumno = cursor.fetchone()

    if not alumno:
        print("No se encontró un alumno con ese DNI.")
        conexion.close()
        return

    print(f"Datos actuales del alumno con DNI {dni}:")
    print(f"Nombre: {alumno[1]}")
    print(f"Apellido: {alumno[2]}")
    print(f"Fecha de nacimiento: {alumno[4]}")
    print(f"Teléfono: {alumno[5]}")
    print(f"Domicilio: {alumno[6]}")


    
   
    while True:
        nombre = input(f"Ingrese el nuevo nombre o presione enter para dejar el que esta (actual: {alumno[1]}): ").capitalize() or alumno[1]
        if nombre.isalpha():
            break  
        else:
            print("El nombre no puede contener números.")

    while True:
        apellido = input(f"Ingrese el nuevo apellido o presione enter para dejar el que esta (actual: {alumno[2]}): ").capitalize() or alumno[2]
        if apellido.isalpha():
            break  
        else:
            print("El apellido no puede contener números.")
    
   
    

    while True:
     
        fecha_nacimiento = input(f"Ingrese la nueva fecha de nacimiento. Ingrese con este formato dd/mm/aaaa (actual: {alumno[4]}): ") or alumno[4]

      
        if fecha_nacimiento != alumno[4]:
            try:
               
                fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
                fecha_nacimiento = fecha_nacimiento_obj.strftime("%Y-%m-%d")

                fecha_actual = datetime.now()
                Edad_minima = datetime(fecha_actual.year - 18, fecha_actual.month, fecha_actual.day)
                Edad_maxima = datetime(fecha_actual.year - 100, fecha_actual.month, fecha_actual.day)

                
                if fecha_nacimiento_obj > fecha_actual:
                    print("La fecha de nacimiento no puede ser posterior a la fecha de hoy.")
                elif fecha_nacimiento_obj > Edad_minima:
                    print("La persona debe tener al menos 18 años.")
                elif fecha_nacimiento_obj < Edad_maxima:
                    print("La persona no puede tener más de 100 años.")
                else:
                    break   
            except ValueError:
                print("Formato de fecha inválido. Asegúrese de usar dd/mm/aaaa.")
        else:
            
            break

    
    
    while True:
        telefono = input(f"Ingrese el nuevo teléfono o presione enter para dejar el que esta (actual: {alumno[5]}): ") or alumno[5]
        if telefono.isdigit() and 8 <= len(telefono) <= 12:
            break
        else:
            print("El número de teléfono debe tener entre 8 y 12 dígitos y no puede contener letras.")
    
 
    while True:
        domicilio = input(f"Ingrese el nuevo domicilio o presione enter para dejar el que esta (actual: {alumno[6]}): ") or alumno[6]
        if any(c.isalpha() for c in domicilio) and any(c.isdigit() for c in domicilio):
            break
        else:
            print("El domicilio debe contener tanto letras como números.")

 
    dni_nuevo = input(f"Ingrese el nuevo DNI o presione enter para dejar el que está (actual: {alumno[3]}): ") or alumno[3]
    while not dni_nuevo.isdigit() or len(dni_nuevo) != 8:
        print("El DNI debe ser un número de 8 dígitos.")
        dni_nuevo = input(f"Ingrese el nuevo DNI o presione enter para dejar el que está (actual: {alumno[3]}): ") or alumno[3]

  
    if dni_nuevo != alumno[3]:
        cursor.execute('''
            UPDATE alumnos
            SET nombre = ?, apellido = ?, dni = ?
            WHERE dni = ?
        ''', (nombre, apellido, dni_nuevo, dni))

        cursor.execute('''
            UPDATE datos_de_alumnos
            SET fecha_nacimiento = ?, telefono = ?, domicilio = ?
            WHERE id_alumno = (SELECT id_alumno FROM alumnos WHERE dni = ?)
        ''', (fecha_nacimiento, telefono, domicilio, dni))

    else:
      
        cursor.execute('''
            UPDATE alumnos
            SET nombre = ?, apellido = ?
            WHERE dni = ?
        ''', (nombre, apellido, dni))

        cursor.execute('''
            UPDATE datos_de_alumnos
            SET fecha_nacimiento = ?, telefono = ?, domicilio = ?
            WHERE id_alumno = (SELECT id_alumno FROM alumnos WHERE dni = ?)
        ''', (fecha_nacimiento, telefono, domicilio, dni))

    conexion.commit()
    conexion.close()

    print("Los datos del alumno han sido actualizados.")


def ordenar_tabla(columna, direccion):
    conexion = conectar()
    cursor = conexion.cursor()

    
    if columna == 'apellido':
        order_by = 'a.apellido'
    elif columna == 'fecha':
        order_by = 'd.fecha_nacimiento'
    elif columna == 'id':
        order_by = 'a.id_alumno'
    else:
        print("Criterio de ordenación no válido.")
        conexion.close()
        return []

  
    cursor.execute(f'''
    SELECT a.id_alumno, a.nombre, a.apellido, a.dni, d.fecha_nacimiento, d.telefono, d.domicilio
    FROM alumnos a
    INNER JOIN datos_de_alumnos d ON a.id_alumno = d.id_alumno
    ORDER BY {order_by} {direccion}
    ''')

     
    alumnos = cursor.fetchall()
    conexion.close()

 
    print(f"{'ID':<10}{'Nombre':<20}{'Apellido':<20}{'DNI':<15}{'Fecha de Nacimiento':<20}{'Teléfono':<15}{'Domicilio':<30}")
    print("="*115)   

    
    for alumno in alumnos:
        
        print(f"{alumno[0]:<10}{alumno[1]:<20}{alumno[2]:<20}{alumno[3]:<15}{alumno[4]:<20}{alumno[5]:<15}{alumno[6]:<30}")
    return alumnos

def eliminar_alumno(dni):
    conexion = conectar()
    cursor = conexion.cursor()

   
    cursor.execute('''SELECT * FROM alumnos WHERE dni = ?''', (dni,))
    alumno = cursor.fetchone()

    if not alumno:
        print("No se encontró un alumno con ese DNI.")
        conexion.close()
        return  

 
    cursor.execute('''DELETE FROM datos_de_alumnos WHERE id_alumno = (SELECT id_alumno FROM alumnos WHERE dni = ?)''', (dni,))

 
    cursor.execute('''DELETE FROM alumnos WHERE dni = ?''', (dni,))

    conexion.commit()
    conexion.close()

    print("El alumno ha sido eliminado.")

while True:
   
    print("Menu\n")
    print("1_Agregar estudiante")
    print("2_Mostrar lista")
    print("3_Actualizar datos")
    print("4_Ordenar Tablas")
    print("5_Eliminar alumno")
    print("6_Salir")
     
    try:
        opcion = int(input("\nIngrese la opcion:\n")) 
    except ValueError:
        print("Ingrese solo numeros")  
        continue  
    
    if opcion == 1:
       pedir_datos()
    elif opcion == 2:
        mostrar_datos()
    elif opcion==3:
         while True:
            try:
             dni = int(input("Ingrese el DNI para actualizar :\n"))
             break   
            except ValueError:
             
                print("Error ingrese nuevamente el dni.")
                
         actualizar(dni)
    elif opcion==4:
        columna=input("Ingrese la columna por la cual quiera ordenar puede ordenar por,apellido,fecha,id\n")
        while columna!="apellido" and columna!="" and columna!="fecha" and columna!="id":
            columna=input("Error Solo puede ordenar por estas opciones apellido,fecha,id\n.Ingrese la columna por la cual quiera ordenar puede ordenar por,apellido,fecha,id\n")
       
        direccion=input("Ingrese ASC o DESC\n").upper()
        while direccion!="ASC" and direccion!="DESC":
            direccion=input("Ingrese ASC o DESC\n").upper()
        ordenar_tabla(columna,direccion)
    elif opcion==5:
        dni=input("Ingrese el dni para eliminar\n")
        eliminar_alumno(dni)
    elif opcion==6:
        print("Salio del programa")
        break
    else:
        print("Esa opción no existe")
  
