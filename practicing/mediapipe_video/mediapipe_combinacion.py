import cv2;
import mediapipe as mp;

mp_drawing = mp.solutions.drawing_utils;
mp_holistic = mp.solutions.holistic;

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW);

with mp_holistic.Holistic(
    static_image_mode = False,
    model_complexity = 1) as holistic:
    #Leer la cámara web
    while True:
        ret, frame = cap.read();
        if ret == False:
            break;
        
        #Realizar la detección de las lineas
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
        #para poder visualizar
        resultados = holistic.process(frame_rgb);
        
         #ROSTRO
        mp_drawing.draw_landmarks(frame, resultados.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                mp_drawing.DrawingSpec(color=(0,255,255), thickness=1, circle_radius=1), # -> Puntos
                                mp_drawing.DrawingSpec(color=(0,128,255), thickness=1)  ## -> Líneas
                                );

        #Mano izquierda
        mp_drawing.draw_landmarks(frame, resultados.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255,255,0), thickness=1, circle_radius=1), # -> Puntos
                                mp_drawing.DrawingSpec(color=(255,0,0), thickness=1)  ## -> Líneas
                                );

        #Mano derecha
        mp_drawing.draw_landmarks(frame, resultados.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255,255,0), thickness=1, circle_radius=1), # -> Puntos
                                mp_drawing.DrawingSpec(color=(255,0,0), thickness=1)  ## -> Líneas
                                );

        #Cuerpo
        mp_drawing.draw_landmarks(frame, resultados.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(128,0,255), thickness=1, circle_radius=1), # -> Puntos
                                mp_drawing.DrawingSpec(color=(255,255,255), thickness=1)  ## -> Líneas
                                );
        
        
        frame = cv2.flip(frame, 1);
        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0XFF == 27:
            break;
        
cap.release();
cv2.destroyAllWindows();
        