from django.db import models
from authuser.models import User

# Create your models here.

class Category(models.Model) :
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

class Group(models.Model) :
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=30)
    group_desc = models.TextField(max_length=400)
    group_photo_profile_link = models.CharField(max_length=150)
    group_member = models.ManyToManyField(User)
    group_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    group_total_member = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    

class Tags(models.Model) :
    tags_id = models.AutoField(primary_key=True)
    tags_name = models.CharField(max_length=50)

class Post(models.Model) :
    post_id = models.AutoField(primary_key=True)
    post_desc = models.TextField(max_length=2000)
    post_image_link = models.CharField(max_length=500)
    post_date = models.DateTimeField(auto_now_add=True)
    post_likes = models.IntegerField(default=0)
    post_group_origin = models.ForeignKey(Group, on_delete=models.CASCADE)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_user_name = models.CharField(max_length=100, null=True)
    post_tags = models.ManyToManyField(Tags)

    def save(self, *args, **kwargs):
        self.post_user_name = self.post_user.name
        super(Post, self).save(*args, **kwargs)
    
class Goods(models.Model) :
    goods_id = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=70)
    goods_price = models.IntegerField()
    goods_description = models.TextField(max_length=1000)
    goods_image_link = models.CharField(max_length=500)
    goods_region = models.CharField(max_length=70)
    goods_group_origin = models.ForeignKey(Group, on_delete=models.CASCADE)
    goods_seller = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=100, null=True)
    stock = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        self.seller_name = self.goods_seller.name
        super(Goods, self).save(*args, **kwargs)

class Like(models.Model) :
    like_id = models.AutoField(primary_key=True)
    like_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model) :
    comment_id = models.AutoField(primary_key=True)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=400)
    user_username = models.CharField(max_length=400)
