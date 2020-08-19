# -*- coding: utf-8 -*-
####################################################################################################
# Romerator - Criador de imagens bregas.
#
# José Alexandre Nalon
####################################################################################################


####################################################################################################
# Importa as bibliotecas necessárias
import numpy as np                             # Para processar matrizes;
import numpy.random as rnd
import os                                      # Para percorrer um diretório;
import os.path as path                         # Para lidar com os nomes de pastas e arquivos;
import cv2                                     # Para carregar e salvar as imagens;


####################################################################################################
# Definições:
N_regions = 100                                        # Número de regiões da imagem;
structuring_element = np.uint8(255 * np.array([        # Elemento estruturante para alargamento
    [ 0, 1, 0 ],                                       #   morfológico da borda;
    [ 1, 1, 1 ],
    [ 0, 1, 0 ] ]))
texture_saturation = 162                               # Saturação constante das cores das texturas;
texture_value = 255                                    # Valor constante das cores das texturas;


####################################################################################################
# Diretórios:
IMAGEDIR = 'imagens'                           # Diretório com as imagens originais;
ROMERODIR = 'romerizadas'                      # Imagens romerizadas;
TEXTUREDIR = 'texturas'                        # Diretório com imagens de texturas;


####################################################################################################
# Funções auxiliares:
def tile_texture(texture, rows, cols):
    """
    Recebe uma textura e replica-a para que fique do tamanho da imagem sobre a qual será imposta.

    :Parameters:
      texture
        Arranjo bidimensional de um único canal com a textura em níveis de cinza. A textura será
        colorida posteriromente;
      rows, cols
        Número de linhas e colunas, respectivamente, da imagem a ser imposta.

    :Returns:
      A textura replicada lado a lado em uma imagem com o tamanho especificado.
    """
    texture_rows, texture_cols = texture.shape
    repeat_rows = int(np.ceil(rows/texture_rows))
    repeat_cols = int(np.ceil(cols/texture_cols))
    tiled = np.tile(texture, (repeat_rows, repeat_cols))
    tiled = tiled[:rows, :cols]
    return tiled


####################################################################################################
# Programa principal:
if __name__ == "__main__":

    # Preparando o feedback para o processamento:
    ni = 1                                                     # Número de imagens processadas;
    dirlist = sorted(os.listdir(IMAGEDIR))
    filecount = len(dirlist)

    # Início do laço:
    for filename in dirlist:

        name, ext = path.splitext(filename)
        if ext == '.png':

            # Carrega a imagem:
            print("Processando arquivo %3d/%d: %s..." % (ni, filecount, filename))
            img = cv2.imread(path.join(IMAGEDIR, name+ext))
            rows, cols, _ = img.shape                           # Número de linhas e colunas;

            # Quantiza a imagem para reduzir o número de níveis de cinza e facilitar a indicação de
            # regiões sobre as quais as texturas serão impostas:
            quantized = np.uint8(np.floor(img/64)*64)

            # As bordas são calculadas para servirem de contorno para a imagem final:
            borders = cv2.Canny(img, 100, 200)
            borders = cv2.dilate(np.uint8(borders), structuring_element, iterations=1)

            # Determina a região sobre a qual cada textura será válida a partir de um algoritmo
            # simples de watersheding. Os marcadores iniciais são determinados aleatoriamente:
            markers = np.where(rnd.random((rows, cols)) < N_regions/(rows*cols), 255, 0)
            _, markers = cv2.connectedComponents(np.uint8(markers))
            regions = cv2.watershed(quantized, cv2.UMat(markers))
            regions = cv2.UMat.get(regions)

            # As bordas das regiões servem como um contorno mais simples e fino para marcar a
            # fronteira entre cada região:
            weak_borders = np.uint8(np.where(regions==-1, 255, 0))
            #weak_borders = cv2.dilate(weak_borders, structuring_element)

            # Aplicação das texturas nas regiões. Para cada região, a textura é escolhida
            # aleatoriamente a partir de imagens em um diretório, e depois colorida com um tom
            # também aleatório:
            file_list = os.listdir(TEXTURE_DIR)
            texture_image = np.zeros((rows, cols, 3), dtype=int)
            region_min = np.amin(regions)
            region_max = np.amax(regions)

            for i in range(region_min, region_max+1):

                if rnd.rand() < 0.5:
                    texture = 255 * np.ones((rows, cols))
                else:
                    file_name = rnd.choice(file_list)
                    texture = cv2.imread(path.join('texturas', file_name), cv2.IMREAD_GRAYSCALE)
                    texture = tile_texture(texture, rows, cols)

                value = rnd.rand()
                texture_image[:,:,0] = np.where(regions==i, value*texture, texture_image[:,:,0])
                texture_image[:,:,1] = np.where(regions==i, 162, texture_image[:,:,1])
                texture_image[:,:,2] = np.where(regions==i, 255, texture_image[:,:,2])

            # A imagem gerada está no espaço de cores HSV, converte para RGB:
            texture_image = cv2.cvtColor(np.uint8(texture_image), cv2.COLOR_HSV2RGB)

            # Aplica um contorno negro impondo as bordas à imagem:
            final = np.zeros((rows, cols, 3))
            bdr = (255-borders)*(255-weak_borders)
            final[:,:,0] = bdr * texture_image[:,:,0]
            final[:,:,1] = bdr * texture_image[:,:,1]
            final[:,:,2] = bdr * texture_image[:,:,2]

            # Guardando as imagens:
            cv2.imwrite(path.join(ROMERODIR, name+'.png'), final)

            # Atualiza o número de imagens processadas:
            ni = ni + 1
