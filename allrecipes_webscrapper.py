import urllib
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re
import numpy as np
from nltk import flatten
import s3fs
import boto3
import os

title_list = []
description_list = []
star_list = []
rating_list = []
review_list = []
photo_list = []
num_ingredient_list = []
ingredient_list = []
total_time_list = []
prep_time_list = []
cook_time_list = []
additional_time_list = []
serving_list = []
protein_list  = []
carb_list = []
fat_list = []
cholesterol_list = []
sodium_list = []
calorie_list = []
recipe_id_list = []

for i in range(20626,30000): #input any range of recipe URL, recipes are spaced far
    try:
        #getting all attributes
        r = urllib.request.urlopen("http://allrecipes.com/recipe/" + str(i))
        soup = BeautifulSoup(r, 'html.parser')
        name = soup.find('h1', class_ ='headline heading-content elementFont__display').getText()
        description = soup.find('p', class_ ='margin-0-auto').getText()
        star = soup.find('span', class_ ='review-star-text visually-hidden').getText()
        no_rating_no_reviews = soup.find('a', class_ ='ugc-ratings-link elementFont__detailsLink--underlined no-ratings')
        rating_exists = soup.find('span', class_ ='ugc-ratings-item elementFont__details')
        review = soup.find('a', class_ ='ugc-ratings-link elementFont__detailsLink--underlined ugc-reviews-link')
        photo = soup.find('a', class_ ='ugc-ratings-link elementFont__detailsLink--underlined ugc-photos-link')
        p_tags = soup.find_all('span', class_ ='ingredients-item-name elementFont__body')
        ingredients = []
        for each in p_tags:
            ingredients.append(str(each.getText()))
        cook_time_attributes = soup.find_all('div', class_ ='recipe-meta-item-header elementFont__subtitle--bold elementFont__transformCapitalize')
        attributes = []
        for each in cook_time_attributes:
            attributes.append(str(each.get_text()).lower())
        cook_time_values = soup.find_all('div', class_ ='recipe-meta-item-body elementFont__subtitle')
        raw_nutrition = soup.find('div', class_ ='recipeNutritionSectionBlock').getText()
        if ('Per Serving:' in raw_nutrition) and ('. Full Nutrition' in raw_nutrition):
            raw_nutrition = raw_nutrition[15:-18].lower()
            if 'calories' not in raw_nutrition:
                raise ValueError
            #raw_nutrition = raw_nutrition.split('Per Serving:')[1].split('. Full Nutrition')[0].strip()
        else:
            raise ValueError

        #Time variables
        cook_values = []
        for each in cook_time_values:
            cook_values.append(str(each.get_text()).lower())
        for a in range(len(cook_values)-1): #not converting yield bc excluding yield as attribute
            cook_values[a] = cook_values[a].strip()
            cook_values[a] = re.sub('[a-z]* weeks', '*24*60*7', cook_values[a])
            cook_values[a] = re.sub('[a-z]* week', '*24*60*7', cook_values[a])
            cook_values[a] = re.sub('[a-z]* days', '*24*60', cook_values[a])
            cook_values[a] = re.sub('[a-z]* day', '*24*60', cook_values[a])
            cook_values[a] = re.sub('[a-z]* hrs', '*60', cook_values[a])
            cook_values[a] = re.sub('[a-z]* hr', '*60', cook_values[a])
            cook_values[a] = re.sub('[a-z]* mins', '', cook_values[a])
            cook_values[a] = re.sub('[a-z]* min', '', cook_values[a])
            cook_values[a] = re.sub('[a-z]* ', '+', cook_values[a])
            cook_values[a] = eval(cook_values[a])
        additional_cook_info = dict(zip(attributes, cook_values))

        #title
        title_list.append(name)

        #description
        description_list.append(description)

        #star
        star = re.findall(r"[-+]?\d*\.\d+|\d+", star)
        if not star:
            star = None
        star_list.append(star)

        #rating
        if no_rating_no_reviews is not None and no_rating_no_reviews != []:
            rating = None
        elif rating_exists is not None and rating_exists != []:
            rating = int(rating_exists.getText().strip().replace(",","").split(' ')[0])
        else:
            rating = None
        rating_list.append(rating)

        #review
        if review is None:
            review = 0
            review_list.append(review)
        else:
            review = soup.find('a', class_ ='ugc-ratings-link elementFont__detailsLink--underlined ugc-reviews-link').getText().strip()
            review = int(review.replace(",","").split(' ')[0])
            review_list.append(review)



        #photos
        if photo:
            photo = int(photo.getText().strip().replace(",","").split(' ')[0])
            #photo = list(map(int, re.findall('\d+', photo)))
        elif not photo:
            photo = 0
        photo_list.append(photo)

        #ingredients
        total_ingredients = len(ingredients)
        ingredient_string = ','.join(ingredients)
        num_ingredient_list.append(total_ingredients)
        ingredient_list.append(ingredient_string)

        #Total cooking time
        total_time = additional_cook_info.get('total:', None)
        total_time_list.append(total_time)

        #Prepreation time
        prep_time = additional_cook_info.get('prep:', None)
        prep_time_list.append(prep_time)

        #Cook time
        cook_time = additional_cook_info.get('cook:', None)
        cook_time_list.append(cook_time)

        #Addtional cooking time
        additional_time = additional_cook_info.get('additional:', None)
        additional_time_list.append(additional_time)

        #Servings per dish
        servings = additional_cook_info.get('servings:', None)
        serving_list.append(servings)

        #Nutrition facts

        nutrition = []
        raw_nutrition = raw_nutrition.split(';')
        for item in raw_nutrition:
            item = item.strip().lower()
            nutrition.append(item)
        nutrition_dict = dict(j.split(' ') for j in nutrition)
        calorie_key = ''
        for k,v in nutrition_dict.items():
            if v == 'calories':
                calorie_key = k
        nutrition_dict['calories'] = nutrition_dict.pop(calorie_key, None)
        nutrition_dict['calories'] = calorie_key

        #Protein (g)
        protein = nutrition_dict.get('protein', None)
        if protein is not None:
            protein = re.findall(r"[-+]?\d*\.\d+|\d+", protein)
        protein_list.append(protein)

        #Carbs (g)
        carbohydrates = nutrition_dict.get('carbohydrates', None)
        if carbohydrates is not None:
            carbohydrates = re.findall(r"[-+]?\d*\.\d+|\d+", carbohydrates)
        carb_list.append(carbohydrates)

        #Fat (g)
        fat = nutrition_dict.get('fat', None)
        if fat is not None:
            fat = re.findall(r"[-+]?\d*\.\d+|\d+", fat)
        fat_list.append(fat)

        #Cholesterol (mg)
        cholesterol = nutrition_dict.get('cholesterol', None)
        if cholesterol is not None:
            cholesterol = re.findall(r"[-+]?\d*\.\d+|\d+", cholesterol)
        cholesterol_list.append(cholesterol)

        #Sodium (mg)
        sodium = nutrition_dict.get('sodium', None)
        if sodium is not None:
            sodium = re.findall(r"[-+]?\d*\.\d+|\d+", sodium)
        sodium_list.append(sodium)

        #calories
        calorie = nutrition_dict.get('calories', None)
        if calorie is not None:
            calorie = re.findall(r"[-+]?\d*\.\d+|\d+", calorie)
        calorie_list.append(calorie)

        #Recipe Number
        recipe_id = str(i)
        recipe_id_list.append(recipe_id)

    except:
        print("no recipe")

title_list = flatten(title_list)
description_list = flatten(description_list)
star_list = flatten(star_list)
rating_list = flatten(rating_list)
review_list = flatten(review_list)
photo_list = flatten(photo_list)
num_ingredient_list = flatten(num_ingredient_list)
ingredient_list = flatten(ingredient_list)
total_time_list = flatten(total_time_list)
prep_time_list = flatten(prep_time_list)
cook_time_list = flatten(cook_time_list)
additional_time_list = flatten(additional_time_list)
serving_list = flatten(serving_list)
protein_list = flatten(protein_list)
carb_list = flatten(carb_list)
fat_list = flatten(fat_list)
cholesterol_list = flatten(cholesterol_list)
sodium_list = flatten(sodium_list)
calorie_list = flatten(calorie_list)
recipe_id_list = flatten(recipe_id_list)


df =pd.DataFrame(list(zip(recipe_id_list, title_list, description_list,rating_list, review_list, photo_list, ingredient_list, num_ingredient_list,prep_time_list,
                          cook_time_list, additional_time_list, total_time_list, serving_list,
                          protein_list, carb_list, fat_list, cholesterol_list, sodium_list, calorie_list,star_list)),
                 columns=['Recipe ID','Recipe', 'Description', 'Total Ratings', 'Total Reviews', 'Number of Photos',
                          'Ingredients', 'Number of Ingredients',
                          'Prep Time (mins)', 'Cook Time (mins)', 'Additional Time (mins)', 'Total Time (mins)',
                          'Servings', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Cholesterol (mg)',
                          'Sodium (mg)','Calories', 'Rated Star'])

#input credentials through separate config file
AWS_ACCESS_KEY_ID = 'x'
AWS_SECRET_ACCESS_KEY = 'y'
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

#saving csv file to s3 bucket location
aws_credentials = { "key": AWS_ACCESS_KEY_ID, "secret": AWS_SECRET_ACCESS_KEY, "token": AWS_SESSION_TOKEN }
df.to_csv("s3://<bucketname>/<path>/all_recipes_webscrapping.csv", index=False, storage_options=aws_credentials)
