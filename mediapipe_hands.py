#cv2 -> Permite el procesamiento de imágenes y visión por computadora
import cv2
#mediapipe -> Es una librería que permite obtener la información de los puntos de la mano
import mediapipe as mp

#Inicialización de herramientas de mediapipe
#Es lo que permitirá dibujar
mp_drawing=mp.solutions.drawing_utils
#Permite detectar la(s) mano(s)
mp_hands=mp.solutions.hands

#Se usa el with para cerrar el hands cuando se salga de ese bloque
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
) as hands:
    #Leer la imagen
    image=cv2.imread("img/imagen.jpg")
    #Obtener el alto, ancho y los canales de colores
    height, width, _ = image.shape
    #Invertir horizontalmente
    image = cv2.flip(image, 1)

    #Convertir de BGR a RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #Se obtendran 2 salidas
    results= hands.process(image_rgb)

    #HANDEDNESS (Mostrar la información general de la ubicación de los puntos)
    #print("Handedness: ", results.multi_handedness)
    
    #MULTI_HAND_LANDMARKS (Obtener la información de los 21 puntos de la mano)
    #print("MULTI_HAND_LANDMARKS: ", results.multi_hand_landmarks)

    if results.multi_hand_landmarks is not None:
        #Valores referenciales de los puntos de los dedos
        valores_referenciales = [4,8,12,16,20]

        #El hand_landmarks contiene los 21 puntos de las 2 manos, pero como tal el results.multi_hand_landmarks recorrerá 2 veces (por cada mano)
        for hand_landmarks in results.multi_hand_landmarks:
            #"i" de indice, y "ubicacion"{x,y,z} que se encuentra dentro del enumerate({lista}), el cual viene a ser la ubicación del punto en el espacio especifico
            for(i, ubicacion) in enumerate(hand_landmarks.landmark):
                #Recorremos todos los puntos hasta que el indice coincida con los "valores_referenciales", el cual es el numero el cual ubica los puntos superiores de los dedos.
                if i in valores_referenciales:
                    x = int(ubicacion.x*width)
                    y = int(ubicacion.y*height)
                    cv2.circle(image, (x,y), 3, (255,0,0), 3)

#Mostrar la imagen
cv2.imshow("Image", image)
#Si en caso se haga clic en alguna tecla se cierra la ventana
cv2.waitKey(0)
#Se cerrarán todas las ventanas abiertas de opencv
cv2.destroyAllWindows()