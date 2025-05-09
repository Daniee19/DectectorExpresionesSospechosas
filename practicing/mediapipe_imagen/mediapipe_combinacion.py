import cv2;
import mediapipe as mp;

#Dibujar líneas, puntos
mp_drawing = mp.solutions.drawing_utils;

#Configuracion total (de los 3: manos, cuerpo, rostro)
mp_holistic = mp.solutions.holistic;

#print(dir(mp_holistic))

with mp_holistic.Holistic(
    static_image_mode = True,
    model_complexity = 2
) as holistic:
    #Obtener la imagen
    image = cv2.imread("./static/img/imagen.jpg");
    imagen_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB);

    #Para realizar las detecciones usaremos holistic
    resultados = holistic.process(imagen_rgb);

    #ROSTRO
    mp_drawing.draw_landmarks(image, resultados.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                              mp_drawing.DrawingSpec(color=(0,255,255), thickness=1, circle_radius=1), # -> Puntos
                              mp_drawing.DrawingSpec(color=(0,128,255), thickness=1)  ## -> Líneas
                              );

    #Mano izquierda
    mp_drawing.draw_landmarks(image, resultados.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(255,255,0), thickness=1, circle_radius=1), # -> Puntos
                              mp_drawing.DrawingSpec(color=(255,0,0), thickness=1)  ## -> Líneas
                              );

    #Mano derecha
    mp_drawing.draw_landmarks(image, resultados.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(255,255,0), thickness=1, circle_radius=1), # -> Puntos
                              mp_drawing.DrawingSpec(color=(255,0,0), thickness=1)  ## -> Líneas
                              );

    #Cuerpo
    mp_drawing.draw_landmarks(image, resultados.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(128,0,255), thickness=1, circle_radius=1), # -> Puntos
                              mp_drawing.DrawingSpec(color=(255,255,255), thickness=1)  ## -> Líneas
                              );
    #Mostrar imagen
    cv2.imshow("Imagen", image);
    cv2.waitKey(0);
cv2.destroyAllWindows();
