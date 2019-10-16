import errno
import shutil
import os

CARPETA_PRINCIPAL = '02-Publicado'
CARPETA_ARCHIVO = '04-Archivo'
CARPETA_SELECCIONADA = '03-PlanosConstructivos'

cambiarCarpeta = input('Desea cambiar la carpeta '+CARPETA_SELECCIONADA+' ?(y/n) ')

if(cambiarCarpeta.lower() == 'y'):
    CARPETA_SELECCIONADA = input('Nueva Carpeta: ')

    

def pathListToString(path):
    bufferString = ''
    for element in path:
        bufferString = bufferString+element+'\\'

    bufferString = bufferString[:-1]
    return bufferString

def deleteLowVersion(file1,file2):
    
    file1Version = int(file1.split('\\')[-1].split('.')[0].split('-')[-1][1:])
    file2Version = int(file2.split('\\')[-1].split('.')[0].split('-')[-1][1:])
    
    if(file1Version > file2Version and file1.split('\\')[1] == CARPETA_SELECCIONADA):
        
        try:
            dest = '..\\'+CARPETA_ARCHIVO+file2[1:]
            offset = len(dest.split('\\')[-1])
            destFolder = dest[:-offset]
            #print(destFolder)
            #print(os.path.exists(destFolder))
            if not os.path.exists(destFolder):
                print(os.makedirs(destFolder))
            try:
                
                shutil.copy2(file2,dest)
                os.remove(file2)
            except:
                print('Error en el archivo: '+file2)
        except:
            pass

    '''
    elif(file2Version > file1Version):
        try:
            dest = '..\\'+CARPETA_ARCHIVO+file1[1:]
            try:
                shutil.copy2(file1,dest)
                os.remove(file1)
            except:
                print('Error en el archivo: '+file1)
        except:
            pass
    '''
    return ''

def compareFiles(file1,file2):

    sameFile = False

    file1Version = file1.split('\\')[-1].split('.')[0].split('-')[-1]
    file1Extension = file1.split('\\')[-1].split('.')[1]

    file2Version = file2.split('\\')[-1].split('.')[0].split('-')[-1]
    file2Extension = file2.split('\\')[-1].split('.')[1]

    phase1 = len(file1Version)+len(file1Extension)+2
    phase2 = len(file2Version)+len(file2Extension)+2

    file1Name = file1[:-phase1]
    file2Name = file2[:-phase2]

    if(file1Name == file2Name and file1Extension != 'py' and file1Extension != 'bat'):
        sameFile = True


    return sameFile

def cleanOlds(actualPath,pathList):

    for path in pathList:
        if(compareFiles(actualPath,path) == True):
            deleteLowVersion(actualPath,path)

    return


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)



#copy('..\\'+CARPETA_PRINCIPAL, '..\\'+CARPETA_ARCHIVO)


filesPathPrincipal = []
filesPathBackup = []

for (dirpath, dirnames, filenames) in os.walk('.'):
    for f in filenames:
        if(os.path.join(dirpath, f).split('\\')[1] == CARPETA_PRINCIPAL):
            
            #filesPathBackup.append(os.path.join(dirpath, f).split('\\'))
            filesPathBackup.append(os.path.join(dirpath, f))
        else:
            
            #filesPathPrincipal.append(os.path.join(dirpath, f).split('\\'))
            filesPathPrincipal.append(os.path.join(dirpath, f))



for path in filesPathPrincipal:
    cleanOlds(path,filesPathPrincipal)
