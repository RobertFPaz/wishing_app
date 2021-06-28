from django.db import models

class WishManager(models.Manager):
    def wish_validation(self, postData):
        errors={}
        if len(postData['item']) == 0:
            errors['item_required']="Item name is required."
        elif len(postData['item']) < 3:
            errors['item_length']="Item name should be minimum 3 characters."
        if len(postData['description'])== 0:
            errors['description_required']="Description is required."
        elif len(postData['description']) < 3:
            errors['content_length'] ="Description should be minimum 3 characters."
        return errors

class Wish(models.Model):
    item=models.CharField(max_length=80)
    description=models.TextField()
    user = models.ForeignKey("login_app.User", related_name="wishes", on_delete=models.CASCADE)
    granted=models.DateField(null=True)
    likes=models.ManyToManyField("login_app.User", related_name="user_likes")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=WishManager()
