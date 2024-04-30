# Application-Feedback-Analytics
Here's a README file for your Git repository containing the code for generating the donut pie chart and stacked bar chart:

**ZuAI App Reviews Visualization**
This repository contains Python code for visualizing the reviews of the ZuAI app from the Google Play Store and App Store. The code generates two plots:

A donut pie chart that categorizes reviews based on their star rating (1 to 5 stars).
A stacked bar chart that segregates reviews based on keywords related to user experience, subscription, curriculum, and AI.

**Requirements**
Python 3.x
pandas
matplotlib
numpy
google_play_scraper 1.2.6
app_store_scraper 0.3.5

**Data**
The review data is assumed to be stored in a pandas DataFrame named result. The DataFrame should have the following columns:

review_description: The text of the review.
rating: The star rating of the review (1 to 5).

If you have the review data in a different format, you'll need to modify the code accordingly.

**Customization**
You can customize the code to change the keywords used for categorizing reviews or modify the plot styles and labels. The relevant sections are clearly commented in the code.
