import torch;
#Cargar los 60 frames, el cual cada frame tiene 543 puntos, con 3 coordenas x,y,z
secuencia_cargada = torch.load('secuencia_frames.pt')
print(secuencia_cargada.shape)  # Debe imprimir [60, 543, 3]
# Verifica los primeros elementos
print(secuencia_cargada[:5])  # Imprimir los primeros 5 elementos de la secuencia