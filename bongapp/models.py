from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image

REVIEW_CHOICES = (
    ("1 star", "1 star"),
    ("2 star", "2 star"),
    ("3 star", "3 star"),
    ("4 star", "4 star"),
    )
SEAT_CHOICES = (
    ("2","2"),
    ("4", "4"),
    ("10", "10"),
    ("20", "20"),
    ("30+(buffet)", "30+(buffet)"),
    )

# Create your models here. DJANGO already comes with a built in user model 
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image= models.ImageField(default='default1.jpg',upload_to='profile_pics') 
    phone=models.BigIntegerField(default=0000)
    review=models.TextField(default='No review',max_length=525)
    address = models.CharField(max_length=300,default='No address')
    state=models.CharField(max_length=111,default='No state')
    def __str__(self):
        return f'{self.user.username}Profile'
    
    def save(self,*args, **kwargs):
        super(Profile,self).save(*args,**kwargs)
    
        img=Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=100)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=70,default="spe")
    price=models.IntegerField(default=0)
    oldprice=models.IntegerField(default=330)
    image=models.ImageField(upload_to="shop",default="demo.jpg") # store image
    description=models.CharField(max_length=500)
    pub_date=models.DateField()
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_product_id=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
       return self.product_name

class OrderModel(models.Model):
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready'),
        (3, 'Delivered')
    )
    created_on=models.DateTimeField(auto_now_add=True)
    price=models.IntegerField(default=0)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,default=0)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,default=0)
    quantity = models.IntegerField(default=1)
    phone = models.CharField(max_length=50, default='', blank=True)
    status = models.IntegerField(choices = status_choices, default=1)
    payment_status = models.BooleanField(default=False)
    stripe_checkout_sessionid=models.CharField(max_length=255, blank=True, null=True)
    


    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'


class Booking(models.Model):
      name=models.TextField(default="no name")
      day = models.DateField(default=datetime.today())
      email=models.EmailField(default='ridhimansin@gmail.com')
      description=models.CharField(max_length=250,default='no special request')
      seats= models.CharField(max_length=100, choices=SEAT_CHOICES, default="2")
      phone=models.IntegerField(default=0)
     


      def __str__(self) :
          return self.name
import shortuuid      
class ChatGroup(models.Model):
    groupname=models.CharField(max_length=100,unique=True,blank=True,default=shortuuid.uuid)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    def __str__(self):
        return self.groupname
    
class Groupmessage(models.Model):
    group=models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)  
    body=models.CharField(max_length=500,null=True)
    created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering=['-created']