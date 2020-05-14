# Importación de módulo para utilizar comandos del sistema
import os

# Importación de módulo para utilizar colas
from collections import deque

# Obtener los archivos del directorio
url_files = os.path.dirname(os.path.abspath(__file__))
files = [ f for f in os.listdir( url_files ) if os.path.isfile( os.path.join( url_files, f ) ) ]
current_file_name =  os.path.basename( os.path.abspath(__file__) )

# Remover el archivo actual
files.remove( current_file_name )

# Declaracón cola de impresión
cola = deque()

# Controlador del menú
principal_menu = True

#Menú principal
def menu():
    print('*********************************************')
    print('-> ¿Qué desea hacer?')
    print('1) Agregar un elemento a la cola de impresión')
    print('2) Imprimir')
    print('3) Salir')

# Obtener todos los archivos
def getFilesCurrentDirectory():
    if( files ):
        print(' \n-> Se encontraron los siguientes archivos en la carpeta actual.')
        print('-> Ingrese el número de archivo que desea agregar a la cola impresión:\n')
        # Mostrar los archivos y filtrarlos
        for ( count, file ) in enumerate( files ):
            print( '[{}] {}'.format( ( count + 1 ), file ) )

        print('[0] Cancelar')
    else:
        print('\n-> No se encontraron archivos para imprimir.\n')

# Obtener los elementos de la cola de impresión
def getCola():
    if( len( cola ) > 0 ):
        print('\n-> La cola de impresión es:\n')
        for ( count, item ) in enumerate( cola ):
            print('[{}] {}'.format( (count + 1), item ))
    else:
        print('\n-> La cola de impresión está vacía.\n')

# Agregar elemento a la cola de impresión
def addCola( select ):
    cola.append( files[ ( select - 1 ) ] )

# Obtener un archivo por selección del usuario
def getFileSelect( select ):
    return files[ ( select - 1 ) ] 

# Imprimir elemento en la cola de impresión
def imprimir():
    
    if( len( cola ) > 0 ):
        # Extraer el primer elemento en la cola de impresión
        first_element = cola.popleft()
        print("\n-> Se imprimió el archivo '{}'.\n".format( first_element ))
    else:
        print('\n-> No se han encontrado archivos para imprimir.')


# Inicialización del programa
while principal_menu:
    menu()
    select_principal_menu = input()

    # Validar las distintas opciones del menú 
    if( select_principal_menu == '1' ):

        getFilesCurrentDirectory()
        select_file = input()

        # Validar que el usuario ingrese numeros
        try:
            select_file = int( select_file )

            # Validar que el usuario ingrese numeros válidos para el listado de archivos
            if( select_file > 0 and select_file <= len( files )  ):

                # Agregar el archivo a la cola de impresión
                addCola( select_file )
                # Obtener toda la cola de impresión
                getCola()
                # Mensaje
                print("\n-> El archivo '{}' se ha agregado a la cola de impresión.\n".format( getFileSelect( select_file ) ))

            elif select_file == 0:
                print('\n-> Impresión cancelada.\n')
            else:
                print('\n-> Por favor seleccione un número de archivo válido.\n')
            
            
        except ValueError:
            try:
                val = float( select_file )
                print("\n-> Por favor seleccione un número entero.\n")
            except ValueError:
                print("\n-> Por favor seleccione un número, no una letra.\n")

    # Usuario imprimir
    elif select_principal_menu == '2':
        # Imprimir el primer archivo en cola de impresión
        imprimir()
        # Obtener toda la cola de impresión
        getCola()
        
    elif select_principal_menu == '3':

        print('\n-> Nos vemos pronto! (=')
        principal_menu = False
        break

    else:
        print('\n-> Por favor seleccione una de las opciones validas.\n')
    

