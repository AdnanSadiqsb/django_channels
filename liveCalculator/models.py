from django.db import models
from django.contrib.auth.models import User
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=500)
    is_see = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Notifications, self).save(
            *args, **kwargs)  # Save the model first

        # After saving the model, trigger the WebSocket notification
        channel_layer = get_channel_layer()
        notifications = Notifications.objects.filter(is_see=False).count()
        data = {'count': notifications, 'current_user': self.user.username,
                'current_notification': self.notification}
        print("data", data)
        # Trigger the send_notification method in the WebSocket consumer
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group_name',  # Use the correct group name
            {
                'type': 'send_notification',
                # Ensure data is serialized as JSON
                'value': json.dumps({"stat": "called"}),
            }
        )
        print("send notification happy ending")
