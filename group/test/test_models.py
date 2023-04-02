from django.test import TestCase
from group.models import Group, Goods, Post, Category
from authuser.models import User

    
class CreateGroup(TestCase):

    def setUp(self):
        category = Category.objects.create(category_name = "Category 1")
        Group.objects.create(group_name="Group1", 
                                group_desc="Group 1 Desc",
                                group_photo_profile_link="drive.google.com/tempDummyLink", 
                                group_category = category)

    def test_group_details(self):
        group = Group.objects.get(group_name="Group1")
        self.assertEqual(group.group_desc, "Group 1 Desc")
        self.assertEqual(group.group_photo_profile_link, "drive.google.com/tempDummyLink")

class TestPost(TestCase):
    def setUp(self):
        user =  User.objects.create(name = "user", email = "user@gmail.com", password = "user", phone = "123456789")
        category = Category.objects.create(category_name = "Category 1")
        game_group = Group.objects.create(group_name = "Game", group_desc = "Forum untuk jual beli dan diskusi game", group_photo_profile_link = "drive.google.com/tempDummyLink", group_category = category)
        Post.objects.create(post_desc = "Test post description",
                             post_image_link = "drive.google.com/asdqwezxc", post_group_origin =game_group, post_user = user)
        
    def test_post_details(self):
        desc = Post.objects.get(post_desc = "Test post description")
        self.assertEqual(desc.post_image_link, "drive.google.com/asdqwezxc")
        
    def test_post_match_group(self):
        post = Post.objects.get(post_desc = "Test post description")
        game_group = Group.objects.get(group_name = "Game")
        self.assertEqual(post.post_group_origin.group_id, game_group.group_id)

class goods_test(TestCase):
    def setUp(self):
        user =  User.objects.create(name = "user", email = "user@gmail.com", password = "user", phone = "123456789")
        category = Category.objects.create(category_name = "Category 1")
        camera_group = Group.objects.create(group_name = "Kamera", group_desc = "Forum untuk jual beli kamera", group_photo_profile_link = "drive.google.com/tempDummyLink", group_category = category)

        Goods.objects.create(goods_name = "Kamera Nikon",
                             goods_price = 5000000,
                             goods_description = "Second like new",
                             goods_image_link = "drive.google.com/axwadawdaw",
                             goods_region = "Jakarta",
                             goods_group_origin = camera_group,
                             goods_seller = user)     
        Goods.objects.create(goods_name = "Kamera Canon",
                             goods_price = 10000000,
                             goods_description = "BNIB",
                             goods_image_link = "drive.google.com/fsefsefsesw",
                             goods_region = "Surabaya",
                             goods_group_origin = camera_group,
                             goods_seller = user)
    
    def test_goods_has_correct_details(self):
        nikon = Goods.objects.get(goods_name = "Kamera Nikon")
        self.assertEqual(nikon.goods_price, 5000000)
        self.assertEqual(nikon.goods_description, "Second like new")
        self.assertEqual(nikon.goods_image_link, "drive.google.com/axwadawdaw")
        self.assertEqual(nikon.goods_region, "Jakarta")

    def test_group_foreign_key_matches_real_id(self):
        nikon = Goods.objects.get(goods_name = "Kamera Nikon")
        camera_group = Group.objects.get(group_name = "Kamera")
        self.assertEqual(nikon.goods_group_origin.group_id, camera_group.group_id)

