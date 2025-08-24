# Recuperación de Datos

No necesitas hacer todo de una, si logras entrar a la BIOS, al menos puedes estar segura de que la lap esta funcional. Lo mismo aplica para la otra PC. Igual y no necesitas la USB para la primera parte que es configurar la BIOS. En una lap como del 2015 tenía una BIOS similar a la de las imágenes, en el mejor de los escenarios, también será tu caso.

> ***La idea de hacerlo así es porqué 1. Puppy Linux es super ligero, 2. Los virus de Windows no afectan a distros Linux.***

## 1. Preparación

> ***Teclado y mouse hacen todo más fácil.*** 

Ten a la mano la USB de Puppy Linux en la lap, asi como la USB para extraer los datos, si esta última no tiene mucha memoria, sería estar vaciando lo que vayas rescatando en la otra lap varias veces.

### 1.1. Consideraciones 

> ***Te recomiendo que tengas la otra lap a la mano por si necesitas ver algun vídeo o este intento de guía.***

Honestamente, no te recomiendo extraer ***ningún .exe, .scr, o .lib de la lap***. Si alguno de estos archivos está infectado, podrías estar copiando el ***malware*** a cualquier PC. **Solo copia documentos, imágenes, música, código o videos.** Además, **no puedes salvar** programas(`MatLab.exe`, `LabView.exe`, etc.) como tal, lo que sí se puede rescatar son archivos o scripts(`.mat`, `.py`, etc.).

## 2. Configurar la prioridad de arranque en la BIOS

La BIOS es donde puedes cambiar la configuración del orden de arranque.

### 2.1. Enciende la lap y espera por el mensaje de configuración de la BIOS.

> ***La pantalla de carga es donde sale la marca "Dell", "Gateway" u otra marca, casi siempre ahí indica que tecla es la buena.***

![Mensaje de Configuración de la BIOS](img/load_screen.jpg)

- Ahora, en mi experiencia, siempre me ha tocado que sea F11 o F8 para entrar a la BIOS.
- **Inmediatamente** comienza a pulsar la tecla para entrar en la BIOS (en algunos otros casos puede ser F2, F7, Del).
- **Presiónala varias veces, puedes probar varias a la vez.**

### 2.2. Accede a la utilidad de configuración de la BIOS

> ***Si de plano se ve confusa tu BIOS, busca un video en YouTube con el modelo de tu lap y "BIOS"***

![Menu Principal](img/bios_menu.jpg)

- Luego de presionar el comando correcto del paso previo en el teclado, accederás a la utilidad de configuración de la BIOS. Los cambios en el orden de arranque son realizados en el menú Boot.

### 2.3. Localizar las opciones de orden de arranque en la BIOS

> ***¡Recuerda, tu BIOS puede presentar instrucciones diferentes!***

![Orden de Arranque](img/boot_order.jpg)

- Para seleccionar qué dispositivo arrancará primero, sigue las instrucciones en la pantalla de la utilidad de setup la BIOS para cambiar el orden de arranque. En este ejemplo de BIOS, el orden de arranque puede ser modificado utilizando las teclas + y -. A veces es con Arriba / Abajo.

## 2.4 Haz cambios en el orden de arranque

> ***La idea es llevar CD/USB como 1ra opción y Disco duro como 2da opción.***

![Nuevo Orden de Arranque](img/new_order.jpg)

- La BIOS ahora buscará primero la USB booteable conectada en algún puerto, antes de intentar arrancar desde el disco duro.

## 2.5 Guardar los cambios

![Guardar Cambios](img/save_changes.jpg)

- Sigue las instrucciones de la BIOS para navegar hacia el menú de ***“Exit” o “Save and Exit”***.

## 2.6 Confirma los cambios

> ***Asegúrate de confirmar los cambios antes de reiniciar. Si piensas seguir con la extracción de datos, ya puedes conectar ambas USBs.***

![Confirmar Cambios](img/confirm_changes.jpg)

- Lee el mensaje cuidadosamente para asegurarte que te encuentras efectivamente guardando tus cambios y no saliendo sin guardarlos. A veces sale medio raro ese mensaje.

## 2.7 Inicia la lap con el nuevo orden de arranque

![Iniciar desde USB](img/start_from_usb.jpg)

## 3. Recuperar tus datos

> ***Algo así verás al iniciar el Puppy Linux. No hagas lo de la instalación o puedes perder tus datos, con que llegues al escritorio esta bien. [Video del 3:25 al 3:40](https://youtu.be/phZt9YA3ny8?si=6DWvteb1QmAIlwvF&t=206)***

Verás una interfaz gráfica completa similar a lo que normalmente llamas "escritorio".

### 3a. Transferir archivos

> ***Si abres la unidad de almacenamiento incorrecta, simplemente cierra con X en la esquina superior derecha de la ventana***

1. En la parte inferior izquierda de tu escritorio hay una lista de todos los discos duros/particiones y unidades USB con un icono de disco duro.
2. Abre tu antiguo disco duro (probablemente `sda1`)
3. Luego, abre tu otra USB (probablemente `sdc` o `sdb1`)
4. Desde tu antiguo disco duro, arrastra y suelta los archivos/carpetas que desees transferir a la ventana de tu unidad USB.

> ***Si algún error te llega a salir, solo tómale foto, y ya lo vemos después.***

*La ruta común a tus carpetas de imágenes, música, vídeo y documentos es:* 
```bash
Documents and Settings >> All Users >> Documents >> Ahora verás My Music, My Pictures y My Videos.
```

Una vez que arrastres y sueltes tu primera carpeta, aparecerá un pequeño menú con opciones para mover o copiar. Elige ***COPIAR*** cada vez que arrastres y sueltes.

## ¿Todo listo?

Para apagar la lap, simplemente haz clic en *Menu >> Pasa el ratón sobre Shutdown >> Reboot/Turn Off Computer*. Después de extraer los datos, asegúrate de conectar tu unidad USB a otra máquina Windows funcionando para verificar que todos los datos están allí y se transfirieron sin corrupción.

## Insisto

> ***NO copies archivos ejecutables (`.exe`, `.scr`, etc.).***
