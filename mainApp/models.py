from django.db import models

class Recipe(models.Model):
    menu_title = models.CharField(max_length=100) #RCP_TTL
    menu_name = models.CharField(max_length=20) #CKG_NM
    cooking_method = models.CharField(max_length=10) #CKG_MTH_ACTO_NM
    main_ingredient_type = models.CharField(max_length=10) #CKG_MTRL_ACTO_NM
    cooking_kind = models.CharField(max_length=10) #CKG_KND_ACTO_NM
    ingredients = models.CharField(max_length=1000) #CKG_MTRL_CN
    cooking_volume = models.CharField(max_length=10) #CKG_INBUN_NM
    cooking_level = models.IntegerField() #CKG_DODF_NM
    cooking_time = models.IntegerField() #CKG_TIME_NM

    class Meta:
        db_table = 'recipe'

class IngredientsList(models.Model):
    list = models.CharField(max_length=1000)

class Result(models.Model):
    recipe_id = models.IntegerField()
    menu_title = models.CharField(max_length=100) #RCP_TTL
    menu_name = models.CharField(max_length=20) #CKG_NM
    ingredients = models.CharField(max_length=1000) #CKG_MTRL_CN
    cooking_volume = models.CharField(max_length=10) #CKG_INBUN_NM
    kind = models.TextField(max_length=1000)
    num = models.IntegerField()

class Rating(models.Model):
    user_id = models.IntegerField()
    recipe_id = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        db_table = 'rating'

# Create your models here.
