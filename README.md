# allrecipes

#H1 **Allrecipes Webscrapper Datapipeline**
#H2 **Overview**
This project details the steps for webscrapping over 10,000+ recipes to analyze factors that could contribute to a higher star ratings from 1 to 5. Included in each recipe are 20 attributes such as  star ratings, number of reviews, number of photos, cooking time, nutrition information, etc. After scrapping data from allrecipes, we generated a csv file that is automatically uploaded to a S3 bucket. We then generate a dataframe from the file using Spark and create visualizations to see how different factors contribute to star ratings.
