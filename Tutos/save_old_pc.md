# Recuperación de Datos

## 1. Preparación

Coloca la USB de Puppy Linux en la lap, asi como la USB para extraer los datos, si esta última no tiene mucha memoria, sería hacer el procedimiento varias veces y estar vaciando lo que vayas rescatando en la otra lap.

> *Teclado y mouse hacen todo más fácil.* 

## 1a. Consideraciones

Honestamente, no te recomiendo sacar **ningún .exe, .scr, o .lib de la lap**. Si alguno de estos archivos está infectado, podrías estar copiando el malware a cualquier PC. **Solo copia documentos, imágenes, música, código o videos.** Además, no puedes salvar programas(`MatLab.exe`, `LabView.exe`, etc.) como tal, lo que sí se puede rescatar son archivos o programas(`.mat`, etc.).

> *Te recomiendo que tengas la otra lap a la mano por si necesitas ver algun viídeo o esta guía.*

## 2. Configurar la prioridad de arranque en la BIOS

La utilidad de configuración de la BIOS es donde puedes cambiar la configuración del orden de arranque.

1. Enciende la lap.
2. **Inmediatamente** comienza a pulsar la tecla para entrar en la BIOS (puede ser F2, Del, a mi siempre me ha tocado que sea F11 o F8). **Presiónalo varias veces.**
   > *La lap te dice cuál durante la pantalla de inicio "Dell", "Gateway" u otra marca*
3. Una vez en la BIOS, busca las opciones avanzadas y cambia la prioridad de arranque a:
   - CD-ROM/USB como **1ra opción**
   - Disco duro como 2da opción
4. Presiona F10 para guardar y salir. Si no igual en tu BIOS te indica que hace cada tecla.
   > *Si de plano se ve confusa tu BIOS, busca un video en YouTube con el modelo de tu lap y "BIOS"*
5. Confirma con "Enter" para continuar
6. Tu lap se reiniciará y arrancará desde el Live USB de Puppy Linux
7. Video por si te pierdes. [3:25 al 3:40](https://youtu.be/phZt9YA3ny8?si=6DWvteb1QmAIlwvF&t=206)

[Imagen de BIOS]()

## 3. Recuperar tus datos

Verás una interfaz gráfica completa similar a lo que normalmente llamas "escritorio". 

### 3a. Transferir archivos

1. En la parte inferior izquierda de tu escritorio hay una lista de todos los discos duros/particiones y unidades USB con un icono familiar de disco duro.
2. Abre tu antiguo disco duro (probablemente `sda1`)
3. Luego, abre tu otra USB (por ejemplo, `sdc` o `sdb1`)
   > *Si abres la unidad incorrecta, simplemente cierra con X en la esquina superior derecha de la ventana*
4. Desde tu antiguo disco duro, arrastra y suelta los archivos/carpetas que desees transferir a la ventana de tu unidad USB.
5. **Si algún error te llega a salir, solo tómale foto, apaga la lap, y ya lo vemos después.**

*La ruta común a tus carpetas de imágenes, música, vídeo y documentos es:* 
```
Documents and Settings >> All Users >> Documents >> Ahora verás My Music, My Pictures y My Videos.
```

Una vez que arrastres y sueltes tu primera carpeta, aparecerá un pequeño menú con opciones para mover o copiar. Elige **COPIAR** cada vez que arrastres y sueltes.

## ¿Lista?

Para apagar la lap, simplemente haz clic en Menu >> Pasa el ratón sobre Shutdown >> Reboot/Turn Off Computer. Asegúrate de conectar tu unidad USB a otra máquina Windows funcionando para verificar que todos los datos están allí y se transfirieron sin corrupción.

## Insisto

**NO copies archivos ejecutables** *(`.exe`, `.scr`, etc.).*
