import cv2;
import mediapipe as mp;
import numpy as np;
import torch;

mp_drawing = mp.solutions.drawing_utils;
mp_holistic = mp.solutions.holistic;

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW);
secuencia = []; #Guardar los keypoints de cada frame

with mp_holistic.Holistic(
    static_image_mode = False,
    model_complexity = 1) as holistic:
    #Leer la cámara web
    while True:
        ret, frame = cap.read();
        if ret == False:
            break;
      
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
        
        #Detección
        resultados = holistic.process(frame_rgb);
        #Obtener coordenadas
        keypoints = [];
        
        def extract_landmarks(landmarks, name):
            if landmarks:
                return [[lm.x, lm.y, lm.z] for lm in landmarks.landmark]
            else:
                if name == "face":
                    return [[0,0,0]]*468;
                elif name == "pose":
                    return [[0,0,0]]*33;
                elif name == "left" or name == "right":
                    return [[0,0,0]]*21;
                else:
                    return [];
        
        # Extraemos los landmarks de las distintas partes
        face = extract_landmarks(resultados.face_landmarks, "face")
        pose = extract_landmarks(resultados.pose_landmarks, "pose")
        left_hand = extract_landmarks(resultados.left_hand_landmarks, "left")
        right_hand = extract_landmarks(resultados.right_hand_landmarks, "right")
        
        #Array de 1629 puntos extraídos de MediaPipe
        keypoints = np.array(face + pose + left_hand + right_hand);
        
        #Dentro del loop que lee cada frame:
        keypoints_tensor = torch.tensor(keypoints, dtype=torch.float32);
        
        if keypoints_tensor.shape == (543, 3):  # Asegurar forma correcta
            secuencia.append(keypoints_tensor)

        # Cuando tengamos 60 frames acumulados:
        if len(secuencia) == 60:
            #Convierte la lista de 60 tensores [543, 3] en un solo tensor tridimensional
            secuencia_tensor = torch.stack(secuencia)  # [60, 543, 3]
            
            # Aquí podrías pasar la secuencia a un modelo o hacer análisis
            #print("Secuencia lista con shape:", secuencia_tensor.shape)
            
            # Guardamos la secuencia de 60 frames en un archivo .pt
            torch.save(secuencia_tensor, 'secuencia_frames.pt');
            print("Secuencia guardada con éxito!")
            secuencia = []  # Vaciar la lista para acumular nuevos 60 frames
        
        
        #cv2.imshow("Frame", frame)
        
        # Normalizar el tensor a un rango [0, 1]
        # keypoints_normalized = keypoints_tensor / keypoints_tensor.max();
        
        # #Verificar la forma del tensor
        # print(keypoints_tensor.shape)
        
        
        
        #Aqui se puede imprimir o guardar:
        #print(keypoints.shape) #Ejemplo: 1629 puntos
        
        if cv2.waitKey(1) & 0XFF == 27:
            break;
        
cap.release();
cv2.destroyAllWindows();
        