import json
from channels.generic.websocket import WebsocketConsumer
from iot_receiver.models import data as heart, acc, gyro


class LastAvailableData(WebsocketConsumer):

    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        heart_data = heart.objects.latest('created_on')
        acc_data = acc.objects.latest('created_on')
        gyro_data = gyro.objects.latest('created_on')

        payload = {
            'index': str(heart_data.id),
            'heart': heart_data.heart,
            'created_on': (heart_data.created_on).timestamp(),
            'acc': {
                'x': acc_data.acc_x,
                'y': acc_data.acc_y,
                'z': acc_data.acc_z,
            },
            'gyro': {
                'x': gyro_data.gyro_x,
                'y': gyro_data.gyro_y,
                'z': gyro_data.gyro_z,
            }
        }
        payload = json.dumps(payload)
        self.send(text_data=payload)
    
    def disconnect(self, code):
        pass

    
