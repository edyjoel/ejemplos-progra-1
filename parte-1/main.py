from tkinter import ttk
from tkinter import filedialog
from tkinter import LabelFrame, Label, Entry, Button, Tk, CENTER, W, E
import os
import glob
import json
from datetime import datetime


class Renombrar:

    # Metodo main
    def __init__(self, window):
        self.wind = window
        self.wind.resizable(False, False)
        self.wind.title('Renombrar Archivos')
        

        # Creamos un Frame Container
        frame = LabelFrame(self.wind, text='Completa los campos')
        frame.grid(row=0, column=0, columnspan=3, pady=10)

        # Input Nuevo Nombre
        Label(frame, text='Nombre nuevo: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Input Extension
        Label(frame, text='Extension archivos: ').grid(row=2, column=0)
        self.extension = Entry(frame)
        self.extension.grid(row=2, column=1)

        # Button buscar carpeta
        Label(frame, text="Carpeta: ").grid(row=3, column=0)
        ttk.Button(frame, command=self.get_path_directory, text='Buscar carpeta').grid(row=3, column=1)

        # Button renombrar
        ttk.Button(frame, command=self.renombrar_archivos, text='Renombrar archivos').grid(row=4, columnspan=3, sticky=W + E)

        # Label path de la carpeta
        self.message_path_directory = Label(text='', wraplength=400, fg='red')
        self.message_path_directory.grid(
            row=4, column=0, columnspan=3, sticky=W + E)
        
        # Label aviso para renombrar
        self.message_renombrar = Label(text='', wraplength=400, fg='red')
        self.message_renombrar.grid(
            row=5, column=0, columnspan=3, sticky=W + E)

        # Tabla
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=6, column=0, columnspan=2)
        self.tree.heading('#0', text="Archivos carpeta", anchor=CENTER)
        self.tree.heading('#1', text="Archivos a renombrar", anchor=CENTER)

        # Inicializar path
        self.path_directory = ''

    # Obtenemos todos los archivos de la carpeta
    def get_files(self, directorio, extension):
        files = os.listdir(self.path_directory)
        filtro_archivos_url_absoluta = glob.glob(directorio+"/*.{}".format(extension))
        records = self.tree.get_children()

        # Reseteamos la tabla
        for element in records:
            self.tree.delete(element)

        # Llenamos la tabla 
        for (contador, file) in enumerate(files):
            if( contador < len(filtro_archivos_url_absoluta)):
                original_nombre = os.path.basename(filtro_archivos_url_absoluta[contador])
                self.tree.insert('', 1, text=file, values = original_nombre)
            else:
                self.tree.insert('', 1, text= file, values ='')


    # Obtenemos el path de la carpeta
    def get_path_directory(self):
        path_directory = filedialog.askdirectory(title="Seleccionar carpeta")
        self.path_directory = path_directory

        # Resetear mensaje
        self.message_renombrar['text'] = ''

        # Mostramos mensajes en la vista
        if(path_directory and self.name.get() and self.extension.get()):
            self.message_path_directory['fg'] = 'green'
            self.message_path_directory['text'] = path_directory
            self.get_files(path_directory, self.extension.get())
        else:
            self.message_path_directory['fg'] = 'red'
            self.message_path_directory['text'] = 'Por favor asegurate de ingresar el *Nuevo nombre* y la *Extension* de los archivos antes de escoger la carpeta.'

    # Funcion que realiza los cambios de nombre
    def renombrar_archivos(self):
        # Obtenemos los parametros
        directorio = self.path_directory
        extension = self.extension.get()
        nombre_nuevo = self.name.get()
        
        # Validamos el directorio
        if(directorio): 
            self.get_files(directorio, extension)
        else:
            self.message_path_directory['text'] = 'Por seleccione una carpeta.'
            
        # Filtra por la extension
        filtro_archivos_url_absoluta = glob.glob(directorio+"/*.{}".format(extension))

        # Inicializa la lista para guardar los cambios
        registros = []

        # Verifica si hay archivos para renombrar
        if(filtro_archivos_url_absoluta):
            print("***ARCHIVOS CAMBIANDO DE NOMBRE***\n")
            for (contador, archivo_original_url_absoluta) in enumerate(filtro_archivos_url_absoluta):

                # Obtenemos el nombre del archivo y la path completo del mismo
                nuevo_nombre = '{}_{}.{}'.format(nombre_nuevo, (contador+1), extension)
                nuevo_nombre_url_absoluta = directorio+'/'+nuevo_nombre

                original_nombre = os.path.basename(archivo_original_url_absoluta)

                # Ejecuta el cambio de nombre
                os.rename(archivo_original_url_absoluta, nuevo_nombre_url_absoluta)

                # Registro
                registros.append({
                    "id": contador,
                    "original": original_nombre,
                    "nuevo": nuevo_nombre
                })

                print("{}. Nombre original: {} Nombre nuevo: {}\n".format(
                    (contador+1), original_nombre, nuevo_nombre))

            print('***TERMINADO***')

            # Obtenemos el tiempo para ponerle al archivo JSON
            tiempo = datetime.now()

            dia = str(tiempo.day)
            mes = str(tiempo.month)
            anio = str(tiempo.year)
            hora = str(tiempo.hour)
            minuto = str(tiempo.minute)
            segundo = str(tiempo.second)

            fecha_id = dia+mes+anio+hora+minuto+segundo

            # Validamos si existe la carpeta o si no la crea
            if(not os.path.isdir(os.getcwd()+'/registros')):
                os.mkdir(os.getcwd()+'/registros')

            # Nombre del archivo JSON
            nombre_archivo_json = os.getcwd()+'/registros/'+nombre_nuevo+'_'+fecha_id+'.json'

            print("Verifica el archivo: " + nombre_archivo_json)

            # Pasamos la lista con los diccionarios a formato JSON
            registro_json = json.dumps(registros)
            
            # Creamos el fichero
            fichero = open(nombre_archivo_json, 'wt')
            fichero.write(registro_json)
            fichero.close()
            
            # Alertas en la vista
            self.message_renombrar['fg'] = 'green'
            self.message_renombrar['text'] = 'Archivos renombrados correctamente. ({})'.format(len(filtro_archivos_url_absoluta))

        else:
            # Se ejecuta si no hay archivos para renombrar
            print("No se encontraron archivos. Por favor verifica la extesion o si en el directorio se encuentran los archivos con la extesion ingresada. No olvides ingresar el Nuevo nombre.")
            self.message_renombrar['text'] = 'No se encontraron archivos. Por favor verifica la extesion o si en el directorio se encuentran los archivos con la extesion ingresada. No olvides ingresar el Nuevo nombre.'

# Inicializamos la clase
if __name__ == '__main__':
    window = Tk()
    aplication = Renombrar(window)
    window.mainloop()
