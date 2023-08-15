import csv
import json
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view

from ultralytics import YOLO
import cv2
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from .models import Recipe, IngredientsList, Result, Rating
from .serializers import RecipeSerializer, IngredientSerializer, ResultSerializer

data = None
file_dir = './mainApp/'

def read_data(table_name):
    with open(file_dir + f'{table_name}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        global data
        data = list(reader)
    return

def footer(table_name, class_name, bulk_list):
    class_name.objects.all().delete()
    class_name.objects.bulk_create(bulk_list)

def add_recipe(request):
    read_data('TB_RECIPE_SEARCH-220701')
    if not data:
        return HttpResponse('Nothing to update')

    arr = []
    num = 0
    for row in data:
        if (row[1] != '') & (row[2] != '') & (row[8] != '') & (row[9] != '') & (row[10] != '') & (row[11] != '') & (row[13] != '') & (row[14] != '') & (row[15] != '') & (row[16] != ''):
            num = num + 1
            if row[16] == '5분이내':
                row[16] = 5
            elif row[16] == '10분이내':
                row[16] = 10
            elif row[16] == '15분이내':
                row[16] = 15
            elif row[16] == '30분이내':
                row[16] = 30
            elif row[16] == '60분이내':
                row[16] = 60
            elif row[16] == '90분이내':
                row[16] = 90
            elif row[16] == '2시간이내':
                row[16] = 120
            elif row[16] == '2시간이상':
                row[16] = 130
            if row[15] == '초급':
                row[15] = 0
            elif (row[15] == '중급') | (row[15] == '아무나'):
                row[15] = 1
            elif row[15] == '고급':
                row[15] = 2
            elif row[15] == '신의경지':
                row[15] = 3
            arr.append(Recipe(
                id = num,
                menu_title = row[1],
                menu_name = row[2],
                cooking_method = row[8],
                main_ingredient_type = row[10],
                cooking_kind = row[11],
                ingredients = row[13],
                cooking_volume = row[14],
                cooking_level = row[15],
                cooking_time = row[16]
            ))

    footer('TB_RECIPE_SEARCH-220701', Recipe, arr)

    return HttpResponse('recipe table updated')

def add_rating(request):
    read_data('all_tables')
    if not data:
        return HttpResponse('Nothing to update')

    arr = []
    num = 0
    for row in data:
        num = num + 1
        arr.append(Rating(
            id = num,
            user_id = row[0],
            recipe_id = row[1],
            rating = row[2]
        ))

    footer('all_tables', Rating, arr)

    return HttpResponse('rating table updated')

@api_view(['GET'])
def add_info(request):
    add_recipe(request)
    add_rating(request)
    return Response('success')

@api_view(['GET','POST'])
def realtime_reg(request):
    if request.method == 'GET':
        ingredients = IngredientsList.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        video = None
        video = request.FILES['cameraData'].read()
        with open('video.mp4', 'wb') as f:
            f.write(video)

        IngredientsList.objects.all().delete()
        ingredients_list=set()
        model=YOLO(file_dir + 'best.pt')
        vid=cv2.VideoCapture('video.mp4')

        while True:
            ret,frame=vid.read()
            if ret:
                results=model(frame)
                names=model.names
                annoted_frame=results[0].plot()
        
                for r in results:
                    for b in r.boxes:
                        if b.conf>=0.35:
                            ingredients_list.add(names[int(b.cls)])
                
                cv2.imshow("YOLOv8 Interface",annoted_frame)
            else:
                break
            if cv2.waitKey(1) & 0xFF ==ord('q'): #종료코드 나중에 생각해야될듯?
                break
    
        vid.release()
        cv2.destroyAllWindows()
        ingredients = []
        for i in ingredients_list:
            ingredients.append({
                'list' : i
            })
        serializer = IngredientSerializer(data=ingredients, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response('success')
        return Response(serializer.errors)

def filtering(essential, kind, level, time):
    if (essential == '') & (kind == '') & (level == -1) & (time == 0):
        recipe_list = list(Recipe.objects.all().values())
    elif (essential == '') & (kind == '') & (level == -1):
        recipe_list = list(Recipe.objects.filter(cooking_time__lte = time).values())
    elif (essential == '') & (kind == '') & (time == 0):
        recipe_list = list(Recipe.objects.filter(cooking_level__lte = level).values())
    elif (essential == '') & (level == -1) & (time == 0):
        recipe_list = list(Recipe.objects.filter(cooking_kind = kind).values())
    elif (kind == '') & (level == -1) & (time == 0):
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential).values())
    elif (essential == '') & (kind == ''):
        recipe_list = list(Recipe.objects.filter(cooking_level__lte = level, cooking_time__lte = time).values())
    elif (essential == '') & (level == -1):
        recipe_list = list(Recipe.objects.filter(cooking_kind = kind, cooking_time__lte = time).values())
    elif (kind == '') & (level == -1):
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential, cooking_time__lte = time).values())
    elif (essential == '') & (time == 0):
        recipe_list = list(Recipe.objects.filter(cooking_kind = kind, cooking_level__lte = level).values())
    elif (kind == '') & (time == 0):
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential, cooking_level__lte = level).values())
    elif (level == -1) & (time == 0):
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential, cooking_kind = kind).values())
    elif (time == 0):
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential, cooking_kind = kind, cooking_level__lte = level).values())
    elif (level == -1):
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential, cooking_kind = kind, cooking_time__lte = time).values())
    elif (kind == ''):
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential, cooking_level__lte = level, cooking_time__lte = time).values())
    elif (essential == ''):
        recipe_list = list(Recipe.objects.filter(cooking_kind = kind, cooking_level__lte = level, cooking_time__lte = time).values())
    else:
        recipe_list = list(Recipe.objects.filter(ingredients__contains = essential, cooking_kind = kind, cooking_level__lte = level, cooking_time__lte = time).values())
    arr = []
    for i in recipe_list:
        arr.append([i['id'], i['menu_title'], i['menu_name'], i['ingredients'], i['cooking_volume']])
    return arr

def find_ingredients(ingredients, recipe_list):
    include = []
    result = []
    result.append(recipe_list)
    num = 0
    if len(ingredients) == 0:
        result.append(include)
        result.append(num)
    else:
        for i in ingredients:
            if recipe_list[3].find(i) != -1:
                num = num + 1
                include.append(i)
        if num != 0:
            result.append(include)
            result.append(num)
    return result
        
def rating(recipe_list):
    rating_data=list(Rating.objects.all().values())
    data=[]
    for i in rating_data:
        data.append([i['user_id'],i['recipe_id'],i['rating']])
    df=pd.DataFrame(data,columns=['user_id','recipe_id','rating'])
    rating_matrix=df.pivot_table(index='user_id',columns='recipe_id',values='rating')

    matrix_dummy = rating_matrix.copy().fillna(0)
    user_similarity = cosine_similarity(matrix_dummy, matrix_dummy)
    user_similarity = pd.DataFrame(user_similarity, index=rating_matrix.index, columns=rating_matrix.index)

    rating_mean = rating_matrix.mean(axis=1)
    rating_bias = (rating_matrix.T - rating_mean).T
    def CF_knn_bias(user_id, recipe_id, my_refridge, neighbor_size=0):    
        if recipe_id in rating_bias:
        # 현 user와 다른 사용자 간의 유사도 가져오기
            sim_scores = user_similarity[user_id].copy()# 현 recipe의 평점편차 가져오기
            recipe_ratings = rating_bias[recipe_id].copy()
            # 현 recipe에 대한 rating이 없는 사용자 삭제
            none_rating_idx = recipe_ratings[recipe_ratings.isnull()].index
            recipe_ratings = recipe_ratings.drop(none_rating_idx)
            sim_scores = sim_scores.drop(none_rating_idx)
    ##### (2) Neighbor size가 지정되지 않은 경우  
            if sim_scores.sum()!=0:   
                if neighbor_size == 0:
                    # 편차로 예측값(편차 예측값) 계산
                    prediction = np.dot(sim_scores, recipe_ratings) / sim_scores.sum()
                    # 편차 예측값에 현 사용자의 평균 더하기
                    prediction = prediction + rating_mean[user_id]
        ##### (3) Neighbor size가 지정된 경우
                else:
                    # 해당 영화를 평가한 사용자가 최소 2명이 되는 경우에만 계산            
                    if len(sim_scores) > 1:
                        # 지정된 neighbor size 값과 해당 영화를 평가한 총사용자 수 중 작은 것으로 결정
                        neighbor_size = min(neighbor_size, len(sim_scores))
                        # array로 바꾸기 (argsort를 사용하기 위함)
                        sim_scores = np.array(sim_scores)
                        recipe_ratings = np.array(recipe_ratings)
                        # 유사도를 순서대로 정렬
                        user_idx = np.argsort(sim_scores)
                        # 유사도와 rating을 neighbor size만큼 받기
                        sim_scores = sim_scores[user_idx][-neighbor_size:]
                        recipe_ratings = recipe_ratings[user_idx][-neighbor_size:]
                        # 편차로 예측치 계산
                        prediction = np.dot(sim_scores, recipe_ratings) / sim_scores.sum()
                        # 예측값에 현 사용자의 평균 더하기
                        prediction = prediction + rating_mean[user_id]
                    else:
                        prediction = rating_mean[user_id]
            else:
                prediction=0
        else:
            prediction = rating_mean[user_id]
        prediction=prediction*0.3 + my_refridge*3.5 #냉장고 내 재료 개수*3.5(==만점 약 5점*70%) + 유사한 레시피를 소비한 사람에 대한 점수(만점 약 5점*30%) 
        return prediction
    
    userid=1
    for i in recipe_list:
        i.append(i[0][0])
    ratingid={}
    recipe_result=[]

    for recipe_id in recipe_list:
        ratingid[recipe_id[3]]=CF_knn_bias(userid,recipe_id[3], recipe_id[2])
    ratingid=sorted(ratingid.items(),key=lambda x:x[1],reverse=True)

    num = 0
    for i in ratingid:
        if num == 10:
            break
        for j in recipe_list:
            if j[3] == i[0]:
                recipe_result.append([j[0], j[1], j[2]])
        num += 1
    return recipe_result

#받아온 값을 이용해서 sql에 검색
@api_view(['GET', 'POST'])
def search_recipe(request):
    if request.method == 'GET':
        result = Result.objects.all()
        serializer = ResultSerializer(result, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        Result.objects.all().delete()
        filter_info = request.data.get('filter_info', False)
        ingredients = request.data.get('ingredients', False)
        print(ingredients)
        result=[]
        recipe_list = filtering(filter_info[0], filter_info[1], filter_info[2], filter_info[3])
        
        for i in recipe_list:
            is_find = find_ingredients(ingredients, i)
            if len(is_find) == 3:
                result.append(is_find)

        rating_result = rating(result)
        result_list = []
        for i in rating_result:
            result_list.append({
                'recipe_id' : i[0][0],
                'menu_title' : i[0][1],
                'menu_name' : i[0][2],
                'ingredients' : i[0][3],
                'cooking_volume' : i[0][4],
                'kind' : json.dumps(i[1]),
                'num' : i[2]
            })
        
        serializer = ResultSerializer(data=result_list, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response('success')
        return Response(serializer.data)
# Create your views here.
