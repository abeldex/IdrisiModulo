# -*- coding: utf-8 -*-
import win32com.client                                          #importamos la libreria para poder acceder a la dll donde se encuentra el SDK de Idrisi
import csv
idrisi32 = win32com.client.Dispatch('IDRISI32.IdrisiAPIServer') #creamos una referencia al SDK de idrisi
from Tkinter import *
import tkMessageBox

window = Tk()                                                   #objeto para la interfaz
window.geometry('450x350')                                      #tamaño de la ventana
window.title("Facultad de Ciencias de la Tierra y el Espacio")  #titulo de la ventana

WORKFOLDER = idrisi32.GetWorkingDir()                           #obtenemos el directorio de trabajo

"""eventos de los botones"""
def img1_click():
    img_sel = idrisi32.CallPick(1, "*.rst", 1, 1, "")
    lbl_img1.configure(text=str(img_sel))

def img2_click():
    img_sel = idrisi32.CallPick(1, "*.rst", 1, 1, "")
    lbl_img2.configure(text=str(img_sel))

def mascara_click():
    img_sel = idrisi32.CallPick(1, "*.rst", 1, 1, "")
    lbl_mascara.configure(text=str(img_sel))

def btn_procesar():
    """calcular el crosstab de los mapas"""
    try:
        CrossTabMacro = "1*" + lbl_img1['text'] + "*" + lbl_img2['text'] + "*NONE*" + lbl_mascara['text'] + "*3*" + txt_new.get() + "*N"
        #tkMessageBox.showinfo("Macro", CrossTabMacro)
        ProcID = idrisi32.AllocateProcess()
        idrisi32.Set_Process_ModuleName(ProcID, "CROSSTAB")
        idrisi32.RunModule("CROSSTAB", CrossTabMacro, 1, "CROSS SINALOA", "", "", "", 1)
        idrisi32.NotifyWorking(ProcID)
        idrisi32.ProcessFinished(ProcID)
        idrisi32.FreeProcess(ProcID)
        # CALCULAR        EL        AREA         DEL        CROSS
        AreaMacro = idrisi32.GetWorkingDir() + txt_new.get() + "*3*1*area" + txt_new.get() + ".txt"
        ProcID2 = idrisi32.AllocateProcess()
        idrisi32.Set_Process_ModuleName(ProcID, "AREA")
        idrisi32.RunModule("AREA", AreaMacro, 1, "AREA CROSS", "", "", "", 1)
        idrisi32.NotifyWorking(ProcID2)
        idrisi32.ProcessFinished(ProcID2)
        idrisi32.FreeProcess(ProcID2)
        #mostrar el raster que resulto como resultado
        idrisi32.DisplayFile(idrisi32.GetWorkingDir() + txt_new.get() + '.rst', 'qual')

        #guardamos el archivo temporal de las areas como csv
        areafile = WORKFOLDER + "area1" + ".id$"
        with open(areafile, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            with open("new"+txt_new.get(), 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerows(lines)
    except:
        tkMessageBox.showerror("Error", "ops algo salio mal")

"""Elementos de la primer imagen"""
lbl = Label(window, text="Seleccionar la primer imagen:")
lbl.grid(column=0, row=0)

btn_img1 = Button(window, text="...", command=img1_click)
btn_img1.grid(column=1, row=0)

lbl_img1 = Label(window, text="-")
lbl_img1.grid(column=0, row=1)

"""elemtnos para seleccionar la segunda imagen"""
lbl2 = Label(window, text="Seleccionar la segunda imagen:")
lbl2.grid(column=0, row=3)

btn_img2 = Button(window, text="...", command=img2_click)
btn_img2.grid(column=1, row=3)

lbl_img2 = Label(window, text="-")
lbl_img2.grid(column=0, row=4)

"""elemtnos para seleccionar la mascara"""
lbl3 = Label(window, text="Seleccionar la mascara:")
lbl3.grid(column=0, row=5)

btn_mascara = Button(window, text="...", command=mascara_click)
btn_mascara.grid(column=1, row=5)

lbl_mascara = Label(window, text="-")
lbl_mascara.grid(column=0, row=6)

"""Elementos para poner un nombre a la imagen generada"""
lbl4 = Label(window, text="Nombre del nuevo archivo:")
lbl4.grid(column=0, row=8)

txt_new = Entry(window, width=50)

txt_new.grid(column=0, row=9)

"""Boton para procesar el crosstab"""
btn_img1 = Button(window, text="Procesar", command=btn_procesar,  width=50)
btn_img1.grid(column=0, row=12)


window.mainloop()                                               #mostramos la ventana


