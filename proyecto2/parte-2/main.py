from tkinter import Label, Button, Tk, StringVar, IntVar, Radiobutton, CENTER
# from PIL import ImageTk, Image
import os, json, tkinter
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime

class Ventas:

    def __init__(self, window):
        self.wind = window
        self.wind.title('Sistema de Ventas')
        # self.wind.iconbitmap(os.getcwd()+'/favicon.ico')
        # self.wind.geometry('500x500')
        # root.grid_columnconfigure(0, weight=1)
        # self.wind.grid_columnconfigure(1, weight=1)
        self.wind.grid_columnconfigure(0, weight=1)


        # Listado vehiculos
        self.vehiculos = [
            {
                'id': 1,
                'tipo': 'Motocicleta',
                'precio_servicio': 15.00
            },
            {
                'id': 2,
                'tipo': 'Automovil',
                'precio_servicio': 30.00
            },
            {
                'id': 3,
                'tipo': 'Camioneta',
                'precio_servicio': 50.00
            }
        ]

        # Tipos de clientes
        self.clientes = [
            {
                'id': 1,
                'tipo_cliente': 'Estandar'
            },
            {
                'id': 2,
                'tipo_cliente': 'Miembro'
            }
        ]

        # Ventas
        self.ventas = []
        self.total_ventas_dia = 0
        self.importe_total_dia = 0
        self.mensaje_alerta = StringVar()
        self.mensaje_exito = StringVar()
        self.id_venta = 0
        
        # Label Bienvenida
        Label(self.wind, text="*****BIENVENIDO*****").pack()

        Label(text='', textvariable=self.mensaje_alerta, fg='red').pack()
        Label(text='', textvariable=self.mensaje_exito, fg='green').pack()

        # Label solicitar tipo de vehiculo
        Label(self.wind, text="Tipo de vehículo:").pack()

        self.selector_vehiculo = IntVar()

        # Listan los botones
        for vehiculo in self.vehiculos:

            texto = '{}) {} (Q.{})'.format(vehiculo['id'], vehiculo['tipo'], vehiculo['precio_servicio'])

            Radiobutton(self.wind, text=texto, variable=self.selector_vehiculo, value=vehiculo['id']).pack()

        # Label solicitar tipo de Cliente
        Label(self.wind, text="Tipo de cliente:").pack()

        self.selector_cliente = IntVar()

        # Listan los botones
        for cliente in self.clientes:

            texto = '{}) {}'.format(cliente['id'], cliente['tipo_cliente'])

            Radiobutton(self.wind, text=texto, variable=self.selector_cliente, value=cliente['id']).pack()

        # Label solicitar si es fin de semana o no
        self.selector_fin_semana = IntVar()

        Label(self.wind, text="Fin de semana:").pack()

        Radiobutton(self.wind, text='1) Si', variable=self.selector_fin_semana, value=1).pack()

        Radiobutton(self.wind, text='2) No', variable=self.selector_fin_semana, value=2).pack()

        # Boton guardar venta
        self.btn_guardar = Button(self.wind, command=self.guardar, text='Guardar')
        self.btn_guardar.pack()
        
        # Boton abrir archivo
        self.btn_abrir = Button(self.wind, command=self.abrir, text='Abrir')
        self.btn_abrir.pack()

        # Boton exportar archivo
        self.btn_exportar = Button(self.wind, command=self.exportar, text='Exportar')
        self.btn_exportar.pack()

        # Label Ventas del dia
        self.mensaje_ventas_dia = StringVar()
        self.mensaje_ventas_dia.set('VENTAS DEL DIA: {}'.format(self.total_ventas_dia))
        Label( self.wind, textvariable=self.mensaje_ventas_dia, text='').pack()

        # Label Importe total
        self.mensaje_importe = StringVar()
        self.mensaje_importe.set('IMPORTE TOTAL: {}'.format(self.importe_total_dia))
        Label( self.wind, textvariable=self.mensaje_importe, text='', fg='green').pack()

        

        # Inicializar tabla
        self.tree = ttk.Treeview()
        self.tree['columns'] = ('id','tipo','precio','cliente','fin_de_semana', 'descuento', 'total')
        self.tree.column('id', anchor=CENTER)
        self.tree.column('tipo', anchor=CENTER)
        self.tree.column('precio', anchor=CENTER)
        self.tree.column('cliente', anchor=CENTER)
        self.tree.column('fin_de_semana', anchor=CENTER)
        self.tree.column('descuento', anchor=CENTER)
        self.tree.column('total', anchor=CENTER)

        self.tree.heading('#0', text="ID", anchor=CENTER)
        self.tree.heading('#1', text="TIPO", anchor=CENTER)
        self.tree.heading('#2', text="PRECIO", anchor=CENTER)
        self.tree.heading('#3', text="CLIENTE", anchor=CENTER)
        self.tree.heading('#4', text="FIN DE SEMANA", anchor=CENTER)
        self.tree.heading('#5', text="DESCUENTO", anchor=CENTER)
        self.tree.heading('#6', text="TOTAL", anchor=CENTER)
        self.tree.pack()
        
        
       
    def procesar(self):

        if(  (self.selector_vehiculo.get() == 0) or (self.selector_cliente.get() == 0) or (self.selector_fin_semana.get() == 0) ) :
      
            self.mensaje_exito.set('')
            self.mensaje_alerta.set('Todos los campos son requeridos.')

        else:
            # Reiniciar Labels
            self.mensaje_alerta.set('')
            self.mensaje_exito.set('Venta guardada correctamente.')

            # Inicializar variables
            self.precio = 0
            self.tipo_vehiculo = ''
            self.tipo_cliente = ''
            self.descuento = 0
            self.total_precio = 0
            self.id_venta = self.id_venta + 1
            self.fin_de_semana = ''
            self.importe_total_dia = 0
            
            # Obtener precio, tipo vehiculo
            for vehiculo in self.vehiculos:
                if(vehiculo['id'] == self.selector_vehiculo.get()):
                    self.precio = vehiculo['precio_servicio']
                    self.tipo_vehiculo = vehiculo['tipo']

            # obtener tipo cliente
            for cliente in self.clientes:
                if(cliente['id'] == self.selector_cliente.get()):
                    self.tipo_cliente = cliente['tipo_cliente']

            
            # Validar si es fin de semana y calcular los datos
            if( self.selector_fin_semana.get() == 1):
                self.fin_de_semana = True
                if(self.tipo_cliente == 'Miembro'):
                    self.descuento = self.precio * (10/100)
                    self.total_precio = self.precio - self.descuento
                    
                else:
                    self.descuento = 0
                    self.total_precio = self.precio
                    
            else:
                self.fin_de_semana = False
                if(self.tipo_cliente == 'Miembro'):
                    self.descuento = self.precio * (20/100)
                    self.total_precio = self.precio - self.descuento
                    
                else:
                    self.descuento = self.precio * (10/100)
                    self.total_precio = self.precio - self.descuento
                    
            # Guardar venta en una lista
            self.guardar_venta(self.id_venta, self.tipo_vehiculo, self.precio, self.tipo_cliente, self.fin_de_semana, self.descuento, self.total_precio)

            # Mostrar en pantalla el total de ventas
            self.total_ventas_dia = len(self.ventas)
            self.mensaje_ventas_dia.set('VENTAS DEL DIA: {}'.format(self.total_ventas_dia))

            # Obtener importe total
            for venta in self.ventas:
                self.importe_total_dia = venta['total'] + self.importe_total_dia

            # Mostrar en pantalla importe total
            self.mensaje_importe.set('IMPORTE TOTAL: {}'.format(self.importe_total_dia))

            # Limpia los imputs
            self.limpiar_selecciones()

            # Muestra los datos en la tabla
            self.mostrar_en_tabla(self.ventas)
            print(self.ventas)
        

    def guardar(self):
        self.procesar()

    def abrir(self):
        ruta_json = tkinter.filedialog.askopenfilename()

        if(ruta_json):
            leer = json.loads(open(ruta_json).read())

            # Mostrar en pantalla el total de ventas
            self.mensaje_ventas_dia.set('VENTAS {}: ({})'.format(ruta_json, len(leer)))

            # Obtener importe total
            total = 0
            for item in leer:
                total = total + item['total']

            # Mostrar en pantalla importe total
            self.mensaje_importe.set('IMPORTE TOTAL: {}'.format(total))

            # Muestra mensaje en pantalla
            self.mensaje_exito.set('Archivo {} abierto correctamente.'.format(ruta_json))

            self.mostrar_en_tabla(leer)
        else:
            self.mensaje_exito.set('')
            self.mensaje_alerta.set('Abre un archivo .json que este programa exporte.')

    def exportar(self):

        ruta_directorio = tkinter.filedialog.askdirectory()

        if(ruta_directorio):
            
            # Obtenemos el tiempo para ponerle al archivo JSON
            tiempo = datetime.now()

            dia = str(tiempo.day)
            mes = str(tiempo.month)
            anio = str(tiempo.year)
            hora = str(tiempo.hour)
            minuto = str(tiempo.minute)
            segundo = str(tiempo.second)

            fecha_id = dia+mes+anio+hora+minuto+segundo

            # Nombre del archivo JSON
            nombre_archivo_json = ruta_directorio+'/'+'ventas'+'_'+fecha_id+'.json'

            # Muestra mensaje en pantalla
            self.mensaje_exito.set('Exportado correctamente, verifica el archivo: {}'.format(nombre_archivo_json))
            print("Verifica el archivo: " + nombre_archivo_json)

            # Pasamos la lista con los diccionarios a formato JSON
            registro_json = json.dumps(self.ventas)
            
            # Creamos el fichero
            fichero = open(nombre_archivo_json, 'wt')
            fichero.write(registro_json)
            fichero.close()

            # Resetar totales
            self.resetear_exportar()

            # Limpiar la tabla
            self.mostrar_en_tabla(self.ventas)



    def guardar_venta(self, id, tipo, precio, cliente, fin_de_semana, descuento, total):
        self.ventas.append({
            'id': id,
            'tipo': tipo,
            'precio': precio,
            'cliente': cliente,
            'fin_de_semana': fin_de_semana,
            'descuento': descuento,
            'total': total
        })

    def limpiar_selecciones(self):
        self.selector_vehiculo.set(0)
        self.selector_cliente.set(0)
        self.selector_fin_semana.set(0)

    def resetear_exportar(self):
        self.ventas = []
        self.total_ventas_dia = 0
        self.importe_total_dia = 0

        # Mostrar en pantalla el total de ventas
        self.mensaje_ventas_dia.set('VENTAS DEL DIA: {}'.format(self.total_ventas_dia))

        # Mostrar en pantalla importe total
        self.mensaje_importe.set('IMPORTE TOTAL: {}'.format(self.importe_total_dia))

    def mostrar_en_tabla(self, lista):
        # Cleaning table
        records = self.tree.get_children()

        for element in records:
            self.tree.delete(element)
        
        for venta in lista:
            self.tree.insert('', 0, text= venta['id'], values = (
                venta['tipo'], 
                venta['precio'], 
                venta['cliente'], 
                venta['fin_de_semana'], 
                venta['descuento'], 
                venta['total']
                )
            )
           
        



if __name__ == '__main__':
    window = Tk()
    aplication = Ventas(window)
    window.mainloop()