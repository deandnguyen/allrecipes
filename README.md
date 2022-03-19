# **Allrecipes Webscrapper Data Pipeline**
## **Overview**
This project details the steps for webscrapping over 10,000+ recipes to analyze factors that could contribute to a higher star ratings from 1 to 5. Included in each recipe are 20 attributes such as  star ratings, number of reviews, number of photos, cooking time, nutrition information, etc. After scrapping data from allrecipes, we generated a csv file that is automatically uploaded to an AWS S3 bucket. We then generate a dataframe from the file using Spark and performed exploratory data analysis to understand distribution of different attributes.

#**Using Python to Scrape Allrecipes and Handle Exceptions**
Allrecipes recipes are found in urls such as www.allrecipes.com/recipe/<recipe id>. By using a for loop to iterate through a set range of recipe_ids, we were able to gather data and save it to a csv file. Recipes are parsed far and can vary in html depending on if it has certain attributes (for example, recipes with ratings vs those without ratings). Some standardization was done to time attributes by changing weeks/hours to minutes. We handled each attribute and throw an exception to skip if the recipe has invalid contents. Afterwards, the csv file is uploaded to our S3 bucket location to perform additional analysis.
  
#**Spark to Derive Insights**
The data collected had to be cleaned for proper analysis. We cleaned certain variables such as "number of ratings" by assigning null values to be 0 and checking for duplicate recipes. We conducted exploratory analysis by looking at the top reviewed recipes, top rated recipes, correlation between attributes and its star ratings, etc. Finally, we conducted predictive analytics for star ratings by building machine learning models.
  
