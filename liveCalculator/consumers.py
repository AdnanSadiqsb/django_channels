import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class Calculator(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer_name"
        self.room_group_name = "test_consumer_group_name"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.room_name
        )
        self.accept()
        self.send(text_data=json.dumps({"Status": "connected"}))

    def send_notification(self, event):
        print("send notification", event)
        self.send(text_data=event['value'])

    def disconnect(self, close_code):

        self.send(json.dumps({"Status": "dis connected"}))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        expression = text_data_json['expression']
        try:
            result = eval(expression)
        except Exception as e:
            result = "Invalid Expression"
        self.send(text_data=json.dumps({
            'result': result
        }))
