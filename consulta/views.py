from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import pruebaForm
from .models import Consulta, Respuesta
import json
import requests as req
import base64

def inicio(request):
    form = pruebaForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/resp')
    return render(request,'inicio.html',{'form':form})
def respuesta(request):
    queryset = Consulta.objects.all()
    URL = "https://api.mercadolibre.com/sites/MCO/search?q=" + queryset[len(queryset)-1].nombre
    r = req.get(url=URL)
    contenido = str(r.content)
    contador = 0
    title = ""
    numero = queryset[len(queryset)-1].numero
    print(numero)
    cont = 0
    precio = ""
    vendidas = ""
    ship  =""
    lista = []
    for chunk in contenido:
        if (contador == 9 and chunk != '"'):
            title = title + chunk
        elif (chunk == '"' and contador == 0):
            contador = 1
        elif (chunk == "t" and contador == 1):
            contador = 2
        elif (contador == 2 and chunk == "i"):
            contador = 3
        elif (contador == 3 and chunk == "t"):
            contador = 4
        elif (contador == 4 and chunk == "l"):
            contador = 5
        elif (contador == 5 and chunk == "e"):
            contador = 6
        elif (contador == 6 and chunk == '"'):
            contador = 7
        elif (contador == 7 and chunk == ':'):
            contador = 8
        elif (contador == 8 and chunk == '"'):
            contador = 9
        elif (contador == 9 and chunk == '"'):
            contador = 0
            print(title)
        elif (contador == 8 and chunk != ','):
            precio = precio + chunk
        elif (chunk == '"' and contador == 0):
            contador = 1
        elif (contador == 1 and chunk == "p"):
            contador = 2
        elif (contador == 2 and chunk == "r"):
            contador = 3
        elif (contador == 3 and chunk == "i"):
            contador = 4
        elif (contador == 4 and chunk == "c"):
            contador = 5
        elif (contador == 5 and chunk == "e"):
            contador = 6
        elif (contador == 6 and chunk == '"'):
            contador = 7
        elif (contador == 7 and chunk == ":"):
            contador = 8
        elif (contador == 8 and chunk == ','):
            contador = 0
        elif (contador == 18 and chunk != ','):
            vendidas = vendidas + chunk
        elif (chunk == "s" and contador == 1):
            contador = 2
        elif (contador == 2 and chunk == "o"):
            contador = 3
        elif (contador == 3 and chunk == "l"):
            contador = 4
        elif (contador == 4 and chunk == "d"):
            contador = 5
        elif (contador == 5 and chunk == "_"):
            contador = 6
        elif (contador == 6 and chunk == "q"):
            contador = 7
        elif (contador == 7 and chunk == "u"):
            contador = 10
        elif (contador == 10 and chunk == "a"):
            contador = 11
        elif (contador == 11 and chunk == "n"):
            contador = 12
        elif (contador == 12 and chunk == "t"):
            contador = 13
        elif (contador == 13 and chunk == "i"):
            contador = 14
        elif (contador == 14 and chunk == "t"):
            contador = 15
        elif (contador == 15 and chunk == "y"):
            contador = 16
        elif (contador == 16 and chunk == '"'):
            contador = 17
        elif (contador == 17 and chunk == ":"):
            contador = 18
        elif (contador == 18 and chunk == ','):
            contador = 0
        elif (contador == 22 and chunk != ','):
            ship = ship + chunk
        elif (chunk == "f" and contador == 1):
            contador = 2
        elif (contador == 2 and chunk == "r"):
            contador = 3
        elif (contador == 3 and chunk == "e"):
            contador = 4
        elif (contador == 4 and chunk == "e"):
            contador = 5
        elif (contador == 5 and chunk == "_"):
            contador = 6
        elif (contador == 6 and chunk == "s"):
            contador = 7
        elif (contador == 7 and chunk == "h"):
            contador = 10
        elif (contador == 10 and chunk == "i"):
            contador = 11
        elif (contador == 11 and chunk == "p"):
            contador = 12
        elif (contador == 12 and chunk == "p"):
            contador = 13
        elif (contador == 13 and chunk == "i"):
            contador = 14
        elif (contador == 14 and chunk == "n"):
            contador = 15
        elif (contador == 15 and chunk == "g"):
            contador = 20
        elif (contador == 20 and chunk == '"'):
            contador = 21
        elif (contador == 21 and chunk == ":"):
            contador = 22
        elif (contador == 22 and chunk == ','):
            contador = 0
            if(ship=="true"):
                ship = "Gratis"
            else:
                ship = "No es gratis"
            obj = Respuesta(titulo=title, precio=float(precio), vendidas=float(vendidas), envio=ship)
            lista.append(obj)
            title = ""
            precio = ""
            vendidas = ""
            ship = ""
            cont+=1
        else:
            contador = 0

        if(cont >= numero):
            break
    context = {
        'productos_list': lista
    }
    return render(request, 'lista.html', context)