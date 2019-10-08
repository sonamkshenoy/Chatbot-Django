from django.db import models

class Conversation(models.Model):
    user_conv = models.TextField()
    bot_conv = models.TextField()

    def __str__(self):
        return self.user_conv
