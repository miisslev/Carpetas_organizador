import pygame
import sys
from pathlib import Path
import shutil
import pyperclip 

#logica 

DICCIONARIO_EXTENSIONES = {
    ".pdf": "Documentos", ".docx": "Documentos", ".txt": "Documentos", ".xlsx": "Documentos",
    ".jpg": "Imágenes", ".jpeg": "Imágenes", ".png": "Imágenes", ".gif": "Imágenes",
    ".mp4": "Videos", ".mkv": "Videos", ".zip": "Comprimidos", ".rar": "Comprimidos",
    ".exe": "Instaladores", ".dmg": "Instaladores", ".sql": "base de datos",
    ".c": "Código", ".cpp": "Código", ".py": "Código", ".back": "Respaldos"
}

def organizar_carpeta(ruta_carpeta):
    archivos_movidos = 0
    for elemento in ruta_carpeta.iterdir():
        if elemento.is_file():
            if "organizador" in elemento.name:
                continue
            extension = elemento.suffix.lower()
            if extension in DICCIONARIO_EXTENSIONES:
                nombre_carpeta_destino = DICCIONARIO_EXTENSIONES[extension]
            else:
                nombre_carpeta_destino = "Otros"
                
            carpeta_destino = ruta_carpeta / nombre_carpeta_destino
            carpeta_destino.mkdir(exist_ok=True)
            shutil.move(str(elemento), str(carpeta_destino / elemento.name))
            archivos_movidos += 1
    return archivos_movidos

#configuracion pygame
pygame.init()

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
fondo = pygame.transform.smoothscale(fondo_original, (600, 600))
btn_reposo = pygame.transform.smoothscale(btn_reposo_original, (160, 110))
btn_presionado = pygame.transform.smoothscale(btn_presionado_original, (160, 110))
hada_reposo = pygame.transform.smoothscale(hada1_original, (200, 260))
hada_presionado = pygame.transform.smoothscale(hada2_original, (200, 260))

#posicionamiento
btn_rect = btn_reposo.get_rect(center=(300, 350))
hada_rect = hada_reposo.get_rect()
hada_rect.centerx = btn_rect.centerx  
hada_rect.centery = btn_rect.centery - 40

textbox_rect = pygame.Rect(100, 430, 400, 35)
texto_input = "" 
fuente_input = pygame.font.SysFont("comicsansms", 18)
textbox_activo = False

mensaje_pantalla = "Organizar"
fuente = pygame.font.SysFont("comicsansms", 24, bold=True)

#bucle principal
while True:
    pos_mouse = pygame.mouse.get_pos()
    mouse_encima = btn_rect.collidepoint(pos_mouse)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        #detecta los clics del mouse
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if textbox_rect.collidepoint(evento.pos):
                textbox_activo = True
            else:
                textbox_activo = False
           
            if mouse_encima:
                mensaje_pantalla = "Limpiando desorden..."
                ventana.blit(fondo, (0, 0))
                ventana.blit(btn_presionado, btn_rect)
                ventana.blit(hada_presionado, hada_rect)
                pygame.display.flip()
                
                ruta_a_organizar = Path(texto_input)
                
                if ruta_a_organizar.exists() and ruta_a_organizar.is_dir():
                    total_archivos = organizar_carpeta(ruta_a_organizar)
                    if total_archivos > 0:
                        mensaje_pantalla = f"Exito, se movieron {total_archivos} archivos."
                    else:
                        mensaje_pantalla = "Carpeta limpia previamente"
                else:
                    mensaje_pantalla = "Error: La ruta escrita no es válida"

        #detecta entradas del tecladoo
        if evento.type == pygame.KEYDOWN:
            if textbox_activo:
                teclas_presionadas = pygame.key.get_pressed()
                ctrl_presionado = teclas_presionadas[pygame.K_LCTRL] or teclas_presionadas[pygame.K_RCTRL]
                             
                if ctrl_presionado and evento.key == pygame.K_v:                   
                    ruta_limpia = pyperclip.paste().replace("\\", "/").replace('"', '')
                    texto_input += ruta_limpia
                
                elif evento.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                
                else:
                    if evento.unicode.isprintable() and not ctrl_presionado:
                        caracter = evento.unicode.replace("\\", "/").replace('"', '')
                        texto_input += caracter

    #capas de dibujo
    ventana.blit(fondo, (0, 0))
    
    if mouse_encima:
        if pygame.mouse.get_pressed()[0]:
            ventana.blit(btn_presionado, btn_rect)
            ventana.blit(hada_presionado, hada_rect)
        else:
            btn_hover = pygame.transform.smoothscale(btn_reposo, (int(btn_rect.width * 1.08), int(btn_rect.height * 1.08)))
            ventana.blit(btn_hover, btn_hover.get_rect(center=btn_rect.center))
            ventana.blit(hada_reposo, hada_rect) 
    else:
        ventana.blit(btn_reposo, btn_rect)
        ventana.blit(hada_reposo, hada_rect)

    #dibujar  el textbox
    pygame.draw.rect(ventana, (120, 80, 150), textbox_rect, border_radius=5)
    pygame.draw.rect(ventana, (255, 255, 255), textbox_rect.inflate(-4, -4), border_radius=3)
    
    texto_surface_input = fuente_input.render(texto_input, True, (0, 0, 0))
    ventana.blit(texto_surface_input, (textbox_rect.x + 10, textbox_rect.y + 7))
        
    #dibuja el texto de estado
    texto_surface = fuente.render(mensaje_pantalla, True, (80, 50, 120)) 
    ventana.blit(texto_surface, texto_surface.get_rect(center=(300, 530)))

    pygame.display.flip()
    reloj.tick(60)