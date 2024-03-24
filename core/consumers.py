# consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .ASLModel import ASLModel
import cv2
import numpy as np
import base64
from PIL import Image
import asyncio
from channels.exceptions import StopConsumer
import mediapipe as mp

RECTANGLE_SIZE = 20


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.prev_predicted_label = "Scanning"
        self.count = 0
        self.model = ASLModel()
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(max_num_hands=1)
        self.loop = asyncio.get_running_loop()
        await self.accept()

    async def disconnect(self, close_code):
        self.hands.close()
        self.stop = True
        raise StopConsumer()

    async def receive(self, bytes_data):
        if not (bytes_data):
            # self.hands.close()
            print("Closed connection")
            await self.close()
        else:
            letter_output = ""
            self.frame = await self.loop.run_in_executor(
                None,
                cv2.imdecode,
                np.frombuffer(bytes_data, dtype=np.uint8),
                cv2.IMREAD_COLOR,
            )
            # Flip the image horizontally
            self.frame = cv2.flip(self.frame, 1)

            h, w, c = self.frame.shape

            result = self.hands.process(self.frame)
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
                    if self.count > 10:
                        self.count = 0
                        try:
                            img_crop = self.frame[
                                       y_min - RECTANGLE_SIZE: y_max + RECTANGLE_SIZE,
                                       x_min - RECTANGLE_SIZE: x_max + RECTANGLE_SIZE,
                                       ]
                            img_crop = Image.fromarray(np.uint8(img_crop))
                            img_crop = img_crop.resize(
                                (self.model.IMAGE_RES, self.model.IMAGE_RES)
                            )
                            img_crop = np.array(img_crop)
                            img_crop = np.fliplr(img_crop)
                            img_crop = np.array(img_crop[:, :, ::-1], dtype="float32")
                            img_crop = img_crop / 255
                            img_crop = img_crop.reshape(
                                (1, self.model.IMAGE_RES, self.model.IMAGE_RES, 3)
                            )

                            predict_test = self.model.model.predict(img_crop)
                            predicted_label = np.argmax(predict_test)
                            self.prev_predicted_label = self.model.lookup[
                                str(predicted_label)
                            ]

                            letter_output = self.model.lookup[str(predicted_label)]
                            cv2.putText(
                                self.frame,
                                f"Label: {self.model.lookup[str(predicted_label)]}",
                                # f"Label: {model.lookup.values()}",
                                (20, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,
                                (36, 255, 12),
                                2,
                            )
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        letter_output = ""
                        cv2.putText(
                            self.frame,
                            f"Label: {self.prev_predicted_label}",
                            # f"Label: {model.lookup.values()}",
                            (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (36, 255, 12),
                            2,
                        )
                        self.count += 1

            self.buffer_img = await self.loop.run_in_executor(
                None, cv2.imencode, ".jpeg", self.frame
            )
            self.b64_img = base64.b64encode(self.buffer_img[1]).decode("utf-8")

            # sending data as a JSON for both the letter and the image
            data_to_send = {
                "letter": letter_output,
                "image": self.b64_img,
            }
            await self.send(json.dumps(data_to_send))