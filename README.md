# Allrecipes Webscraper Data Pipeline

# Overview
This project details the steps for webscraping over 13,000+ recipes to analyze factors that could contribute to a higher star ratings from 1 to 5. Included in each recipe are 20 attributes such as star ratings, number of reviews, number of ratings number of photos, different types of cooking time, nutrition information, etc. After scraping data from allrecipes, we generated a csv file that is automatically uploaded to an AWS S3 bucket. We then generate a dataframe from the file using Spark and performed exploratory data analysis to understand distribution of different attributes.

# Introduction
Food recipe websites is a highly competitive space, where any data that could improve customer satisfaction could give an edge against competitors. In this project, we webscraped 13,000+ recipes to analyze factors that could contribute to a higher customer satisfaction measured by star ratings from 1 to 5. We pull various attributes and performed exploratory analysis. We found that customers were agnostic of nutrition information and are more favorable to websites with high reviews. We discuss shortcomings in this project and possible improvements.

# Methodology
We scraped Allrecipes with the possibility of scale at mind by doing the following:

Step 1: Obtain allrecipes attributes and load to a csv file

Step 2: Script uploads csv file to AWS S3 bucket 

Step 3: Exploratory Analysis with Spark refrecencing table

![image](https://user-images.githubusercontent.com/77939423/160414750-143e899d-f307-4a64-ae54-90b713e995be.png)

STEP 1: HTML to obtain attributes and load to a csv file Allrecipes recipes are found in urls such as www.allrecipes.com/recipe/. By using a loop to iterate through a set range of recipe_ids, we were able to gather data and save it to a csv file. Recipes are parsed far and can vary in html depending on if it has certain attributes.For example, html for recipes with ratings is different those without ratings, and we had to keep those edge cases in mind for scrapping. Some standardization was done to time attributes by changing weeks/hours to minutes. We handled each attribute and throw an exception to skip if the recipe has invalid contents. For each recipe, we appended attribute data to their own lists to be fed to a dataframe that was able to upload a csv directly to AWS S3.

STEP 2: Script uploads csv file to AWS S3 bucket. We created a AWS account and made a bucket with a landing destination path. We generated a AWS access key_id and AWS secret access key that our script references to give permissions for uploads. Note in a real production environment we would have these keys within a different config file.

STEP 3: Exploratory Analysis with Spark To perform analytics on our table, we connect Spark to our file. We create a dataframe and explore how attributes correlate to rating variable. The data collected had to be cleaned for proper analysis. We cleaned certain variables such as "number of ratings" by assigning null values to be 0 and checking for duplicate recipes. We conducted exploratory analysis by looking at the top reviewed recipes, top rated recipes, correlation between attributes and its star ratings, etc. 

# Findings
Based on our analysis, we found that recipes rated 4 and 4.5 stars made up 81% of all 13,522 recipes that we scraped, in which recipes rated 4.5 stars made up 52%. The top rated and most-reviewed recipes tend to belong to the desert category, such as chocolate chip cookies, pancakes, banana bread, muffins. In terms of total cooking time (which is an aggregation of preparation time, any additional time that is needed, and actual cook time), we saw that recipes rated 1 star tend to have longer cooking time, with an average of almost 6.5 hours. However, we can't conclude that a longer cooking time leads to a lower star rating, as the average cooking time of recipes rated 1.5 stars is around 1.5 hours, while recipes rated 4.5 and 5 stars have an average of around 2.5 hours. Nevertheless, it's possible that readers tend to gravitate towards recipes with an average cooking time of around 2-2.5 hours.

<img width="412" alt="Screen Shot 2022-03-30 at 7 37 48 PM" src="https://user-images.githubusercontent.com/77939423/160953357-f8f9f81a-9cdd-47c0-8c31-e2ef2f1025f1.png">

We also looked at the relationship between nutrition information and star ratings. However, no clear trends are detected, as recipes rated lowest (1.0 star) and highest (5.0 star) have similar amount of fat (in the range between 12-16 grams), protein (around 7.5 grams), carbs (between 35-39 grams), cholesterol, and calories (between 310-360 mg).

# Next Steps
To dive deeper into recipe analysis, the next step is to obtain broad categories (ie. Meat) and sub-categories (ie. Beef Recipes, Chicken Recipes) for each recipe in order to understand the common themes between sub-categories, as well as differences among broad categories and how consumers react to each. We could also scrape data related to customers' reviews and conduct sentimental analysis to understand their opinions for recipes.

# Challenges
We faced many types of challenges from our scraper as well as interprepting the data. There were many exceptions that we had to handle for different webpages for html changes, as well as handling recipes with missing attributes. We also realized limitations of basing customer satisfaction with star ratings. Star ratings may be boosted by Allrecipes continually promoting the recipe, hence explaining the high reviews to high ratings.

A possible improvement on this project is building a better data pipeline. For this project, we did our analysis from Spark to our csv file. A more stable pipeline could include creating a table within RedShift, cleaning the table in a staging area, and then feeding the table to Spark for analysis. This would lead to higher scalability than our adhoc analysis.
