from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from  PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='img', default="default.png", blank=True, null=True)
    friends = models.ManyToManyField('Friend', related_name='my_friends')


    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     '''
    #     Get current image and reduce its width and height if
    #     any is greater than 300.

    #     NB: A more practical approach is to store these images in s3 buckets or cloudinary
    #     '''
    #     img = Image.open(self.pic.path)
        
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.pic.path)


 
class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


    @property
    def num_of_messages(self):
        chats = ChatMessage.objects.filer(msg_sender=self.profile, seen=False)
        return chats.count

        
    def __str__(self):
        return self.profile.name


class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body

     