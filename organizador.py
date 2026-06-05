import pygame
import sys
from pathlib import Path
import shutil

#logica del organizador

#aqui se pone la ruta de la carpeta que se organizara
carpeta_descargas = Path(r"C:\respaldo")  

DICCIONARIO_EXTENSIONES = {
    ".pdf": "Documentos", ".docx": "Documentos", ".txt": "Documentos", ".xlsx": "Documentos",
    ".jpg": "Imágenes", ".jpeg": "Imágenes", ".png": "Imágenes", ".gif": "Imágenes",
    ".mp4": "Videos", ".mkv": "Videos", ".zip": "Comprimidos", ".rar": "Comprimidos",
    ".exe": "Instaladores", ".dmg": "Instaladores", ".sql": "base de datos",
    ".c": "Código", ".cpp": "Código", ".py": "Código", ".back": "Respaldos"
}

def organizar_carpeta():
    archivos_movidos = 0
    for elemento in carpeta_descargas.iterdir():
        if elemento.is_file():
            if "organizador" in elemento.name:
                continue
            extension = elemento.suffix.lower()
            if extension in DICCIONARIO_EXTENSIONES:
                nombre_carpeta_destino = DICCIONARIO_EXTENSIONES[extension]
            else:
                nombre_carpeta_destino = "Otros"
                
            carpeta_destino = carpeta_descargas / nombre_carpeta_destino
            carpeta_destino.mkdir(exist_ok=True)
            shutil.move(str(elemento), str(carpeta_destino / elemento.name))
            archivos_movidos += 1
    return archivos_movidos

#conf de pygame
pygame.init()

#reduce la ventana a 600x600 para que quepa en el monitor
ventana = pygame.display.set_mode((600, 600)) 
pygame.display.set_caption("Organizador Visual Personalizado")
reloj = pygame.time.Clock()

#carga de imagenes 
fondo_original = pygame.image.load("fondo.png.PNG").convert()
btn_reposo_original = pygame.image.load("boton_reposo.PNG").convert_alpha()
btn_presionado_original = pygame.image.load("boton_presionado.PNG").convert_alpha()
hada1_original = pygame.image.load("hada1.PNG").convert_alpha()
hada2_original = pygame.image.load("hada2.PNG").convert_alpha()

#escalado general
#fondo adaptable
fondo = pygame.transform.smoothscale(fondo_original, (600, 600))
#nubes pequeñas para que luzcan bien 
btn_reposo = pygame.transform.smoothscale(btn_reposo_original, (160, 110))
btn_presionado = pygame.transform.smoothscale(btn_presionado_original, (160, 110))
hada_reposo = pygame.transform.smoothscale(hada1_original, (200, 260))
hada_presionado = pygame.transform.smoothscale(hada2_original, (200, 260))

#posicionamiento

# Ubicamos la nube en X=300  y Y=430 
btn_rect = btn_reposo.get_rect(center=(300, 430))
hada_rect = hada_reposo.get_rect()
hada_rect.centerx = btn_rect.centerx  # Centrada horizontalmente con la nube
hada_rect.centery = btn_rect.centery - 40
mensaje_pantalla = "Organizar"
fuente = pygame.font.SysFont("Helvetica", 24, bold=True)

#bucle principal
while True:
    pos_mouse = pygame.mouse.get_pos()
    mouse_encima = btn_rect.collidepoint(pos_mouse)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if mouse_encima:
                mensaje_pantalla = "Limpiando desorden..."
                ventana.blit(fondo, (0, 0))
                ventana.blit(btn_presionado, btn_rect)
                ventana.blit(hada_presionado, hada_rect)
                pygame.display.flip()
                
                total_archivos = organizar_carpeta()
                
                if total_archivos > 0:
                    mensaje_pantalla = f"Exito, se movieron {total_archivos} archivos."
                else:
                    mensaje_pantalla = "Carpeta limpia previamente"

    #dibuja el fondo reescalado
    ventana.blit(fondo, (0, 0))
    
    #dibujamos el boton animado
    if mouse_encima:
        if pygame.mouse.get_pressed()[0]:
            ventana.blit(btn_presionado, btn_rect)
            ventana.blit(hada_presionado, hada_rect) # Dibuja hada con ojos abiertos al dar clic
        else:
            # efecto al pasar el mouse por encima
            btn_hover = pygame.transform.smoothscale(btn_reposo, (int(btn_rect.width * 1.08), int(btn_rect.height * 1.08)))
            ventana.blit(btn_hover, btn_hover.get_rect(center=btn_rect.center))
            ventana.blit(hada_reposo, hada_rect) 
    else:
        ventana.blit(btn_reposo, btn_rect)
        ventana.blit(hada_reposo, hada_rect)
        
    #dibujamos el texto abajo del botón en la coordenada Y=530 
    texto_surface = fuente.render(mensaje_pantalla, True, (80, 50, 120)) 
    ventana.blit(texto_surface, texto_surface.get_rect(center=(300, 530)))

    pygame.display.flip()
    reloj.tick(60)