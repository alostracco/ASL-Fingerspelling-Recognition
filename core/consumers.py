# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from .ASLModel import ASLModel
import cv2
import numpy as np
import base64
from PIL import Image
import asyncio
from channels.exceptions import StopConsumer
import mediapipe as mp

RECTANGLE_SIZE = 30
model = ASLModel()
# model = model_base.load_model()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.loop = asyncio.get_running_loop()
        await self.accept()

    async def disconnect(self, close_code):
        self.stop = True
        raise StopConsumer()

    async def receive(self, bytes_data):
        if not (bytes_data):
            print("Closed connection")
            await self.close()
        else:
            self.frame = await self.loop.run_in_executor(
                None,
                cv2.imdecode,
                np.frombuffer(bytes_data, dtype=np.uint8),
                cv2.IMREAD_COLOR,
            )
            # Flip the image horizontally
            self.frame = cv2.flip(self.frame, 1)

            h, w, c = self.frame.shape

            result = hands.process(self.frame)
            hand_landmarks = result.multi_hand_landmarks

            if hand_landmarks:
                for handLMs in hand_landmarks:
                    x_max = 0
                    y_max = 0
                    x_min = w
                    y_min = h

                    for lm in handLMs.landmark:
                        x, y = int(lm.x * w), int(lm.y * h)

                        if x > x_max:
                            x_max = x
                        if x < x_min:
                            x_min = x
                        if y > y_max:
                            y_max = y
                        if y < y_min:
                            y_min = y

                    cv2.rectangle(
                        self.frame,
                        (x_min - RECTANGLE_SIZE, y_min - RECTANGLE_SIZE),
                        (x_max + RECTANGLE_SIZE, y_max + RECTANGLE_SIZE),
                        (0, 255, 0),
                        2,
                    )

                    try:
                        img_crop = self.frame[
                            y_min - RECTANGLE_SIZE : y_max + RECTANGLE_SIZE,
                            x_min - RECTANGLE_SIZE : x_max + RECTANGLE_SIZE,
                        ]
                        img_crop = Image.fromarray(np.uint8(img_crop))
                        img_crop = img_crop.resize((model.IMAGE_RES, model.IMAGE_RES))
                        img_crop = np.array(img_crop)
                        img_crop = np.fliplr(img_crop)
                        img_crop = np.array(img_crop[:, :, ::-1], dtype="float32")
                        img_crop = img_crop / 255
                        img_crop = img_crop.reshape(
                            (1, model.IMAGE_RES, model.IMAGE_RES, 3)
                        )

                        predict_test = model.model.predict(img_crop)
                        predicted_label = np.argmax(predict_test)

                        cv2.putText(
                            self.frame,
                            f"Label: {model.lookup[str(predicted_label)]}",
                            # f"Label: {model.lookup.values()}",
                            (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (36, 255, 12),
                            2,
                        )
                    except Exception as e:
                        print(f"Error: {e}")

            self.buffer_img = await self.loop.run_in_executor(
                None, cv2.imencode, ".jpeg", self.frame
            )
            self.b64_img = base64.b64encode(self.buffer_img[1]).decode("utf-8")
            # Send the base64 encoded image back to the client
            await asyncio.sleep(0.1)
            await self.send(self.b64_img)
