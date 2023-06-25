import requests
from tkinter import *
from tkinter import messagebox
class Aplicacion():
    __ventana=None

    def __init__(self):
        self.__ventana = Tk()
        self.__ventana.title('Ejercicio 5')
        self.__ventana.geometry('300x200')
        scrollbar = Scrollbar(self.__ventana)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.__ventana, width=50, height=20)
        self.listbox.pack()
        self.listbox.config(yscrollcommand=scrollbar.set)  # Configurar el comando de desplazamiento del Listbox
        scrollbar.config(command=self.listbox.yview)
        self.datos()
        self.listbox.bind("<<ListboxSelect>>", self.mostrarDatos)

    def datos(self):
        r=requests.get("https://api.themoviedb.org/3/discover/movie?api_key=829f8e554232f2a6d76f36f13590cb24")
        # Obtener los datos de la respuesta JSON
        datos = r.json()
        peliculas = datos['results']
        # Agregar los títulos de las películas al ListBox
        for pelicula in peliculas:
            titulo = pelicula['title']
            self.listbox.insert(END, titulo)

    def mostrarDatos(self, event):
        seleccion = self.listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            r = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=829f8e554232f2a6d76f36f13590cb24")
            if r.status_code == 200:
                datos = r.json()
                peliculas = datos['results']
                pelicula_seleccionada = peliculas[indice]
                titulo = pelicula_seleccionada['title']
                resumen = pelicula_seleccionada['overview']
                lenguaje_original = pelicula_seleccionada['original_language']
                fecha_lanzamiento = pelicula_seleccionada['release_date']
                generos = pelicula_seleccionada['genre_ids']

                # Obtener nombres de géneros utilizando una segunda llamada a la API
                generos_nombres = []
                for genero_id in generos:
                    genero = self.obtener_nombre_genero(genero_id)
                    generos_nombres.append(genero)

                # Crear el mensaje a mostrar con todos los datos
                mensaje = f"Título: {titulo}\n\nResumen: {resumen}\n\nLenguaje Original: {lenguaje_original}\n\nFecha de Lanzamiento: {fecha_lanzamiento}\n\nGéneros: {', '.join(generos_nombres)}"

                messagebox.showinfo("Detalles de la Película", mensaje)

    def obtener_nombre_genero(self, genero_id):
        r = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=829f8e554232f2a6d76f36f13590cb24")
        if r.status_code == 200:
            datos = r.json()
            generos = datos['genres']
            for genero in generos:
                if genero['id'] == genero_id:
                    return genero['name']
        return "Desconocido"

    def ejecutar(self):
        self.__ventana.mainloop()

if __name__ == '__main__':
    app=Aplicacion()
    app.ejecutar()