# **Allrecipes Webscrapper Data Pipeline**
# **Overview**
This project details the steps for webscrapping over 10,000+ recipes to analyze factors that could contribute to a higher star ratings from 1 to 5. Included in each recipe are 20 attributes such as  star ratings, number of reviews, number of photos, cooking time, nutrition information, etc. After scrapping data from allrecipes, we generated a csv file that is automatically uploaded to an AWS S3 bucket. We then generate a dataframe from the file using Spark and performed exploratory data analysis to understand distribution of different attributes.
## **Introduction** ##
Food recipe websites is a highly competitive space, where any data that could improve customer satisfaction could give an edge against competitors. In this project, we webscrapped 10,000+ recipes to analyze factors that could contribute to a higher customer satisfaction measured by star ratings from 1 to 5. We pull various attributes and did exploratory analysis against them. We found that customers were agnostic of nutrition info and are more favorable to websites with high reviews. We discuss shortcomings in this project and possible improvements.
  
  
## **Methdology** ##
We scraped Allrecipes with the possibility of scale at mind by doing the following:
  
Step 1: Obtain allrecipes attributes and load to a csv file

Step 2: Script uploads csv file to AWS S3 bucket to Athena table

Step 3: Exploratory Analysis with Spark refrecencing table
 
![image](https://user-images.githubusercontent.com/51719335/160030113-4430f842-5d36-4214-baa7-33242a0f77bd.png)
 

**STEP 1: HTML to obtain attributes and load to a csv file**
Allrecipes recipes are found in urls such as www.allrecipes.com/recipe/<recipe id>. By using a loop to iterate through a set range of recipe_ids, we were able to gather data and save it to a csv file. Recipes are parsed far and can vary in html depending on if it has certain attributes.For example, html for recipes with ratings is different those without ratings, and we had to keep those edge cases in mind for scrapping. Some standardization was done to time attributes by changing weeks/hours to minutes. We handled each attribute and throw an exception to skip if the recipe has invalid contents. For each recipe, we appended attribute data to their own lists to be fed to a dataframe that was able to upload a csv directly to AWS S3.
  
**STEP 2: Script uploads csv file to AWS S3 bucket**
We created a AWS account and made a bucket with a landing destination path. We generated a AWS access key_id and AWS secret access key that our script references to give permissions for uploads. Note in a real production environment we would have these keys within a different config file. 
  
**STEP 3: Exploratory Analysis with Spark**
To perform analytics on our table, we connect Spark to our file. We create a dataframe and explore how attributes correlate to rating variable. The data collected had to be cleaned for proper analysis. We cleaned certain variables such as "number of ratings" by assigning null values to be 0 and checking for duplicate recipes. We conducted exploratory analysis by looking at the top reviewed recipes, top rated recipes, correlation between attributes and its star ratings, etc. Finally, we conducted predictive analytics for star ratings by building machine learning models.

## **Recommendations** ##

## **Challenges** ##
We faced many types of challenges from our scrapper as well as interprepting the data. There were many exceptions that we had to handle for different webpages for html changes, as well as handling recipes with missing attributes. We also realized limitations of basing customer satisfaction with star ratings. Star ratings may be boosted by Allrecipes continually promoting the recipe, hence explaining the high reviews to high ratings. 
  
Possible improvements on this project include increased segmentation of recipes and improving our data pipeline. First, we may have gotten different results from segmenting the recipes in their respective categories. Recipes can be compared against one another to provide additional context besides purely rating. Secondly, we did our analysis from Spark to our csv file. A more stable pipeline could include creating a table within RedShift, cleaning the table in a staging area, and then feeding the table to Spark for analysis. This would lead to higher scalability than our adhoc analysis.
  
  
  
  
