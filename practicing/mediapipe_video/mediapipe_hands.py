import cv2
import mediapipe as mp

#Inicialización
mp_drawing=mp.solutions.drawing_utils
mp_hands=mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5
) as hands:
    
    while True:
        ret, frame = cap.read()
        #Si hay una falla al no detectar bien un frame (como la desconexión de la cámara)
        if ret == False:
            break
        
        #Se obtienen las dimensiones del frame
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Mediapipe internamente necesita la imagen en formato RGB para analizarlo de la mejor manera
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            #Obtener los 21 puntos por cada mano detectada
            for hand_landmarks in results.multi_hand_landmarks:
                #Dibujar los puntos y conexiones
                #Aqui no es necesario usar el frame_rgb ya que solo se toma como lienzo
                #El primer parámetro define el lienzo a dibujar
                #El segundo parámetro dibuja los puntitos
                #El tercer parámetro dibuja las conexiones
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


        cv2.imshow("Frame", frame)
        #Si se presiona la tecla escape se sale de la camara
        if cv2.waitKey(1) & 0xFF == 27:
            break
#Desconecta la cámara (buena práctica)
cap.release()
cv2.destroyAllWindows()