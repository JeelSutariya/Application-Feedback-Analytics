from google_play_scraper import app, Sort, reviews_all
from app_store_scraper import AppStore
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json, os, uuid

g_reviews = reviews_all(
        "in.zupay.app",
        sleep_milliseconds=0,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
    )
a_reviews = AppStore('in', 'zuai-1-self-study-app', '1609941536')
a_reviews.review()

g_df = pd.DataFrame(np.array(g_reviews),columns=['review'])
g_df2 = g_df.join(pd.DataFrame(g_df.pop('review').tolist()))

g_df2.drop(columns={'userImage', 'reviewCreatedVersion'},inplace = True)
g_df2.rename(columns= {'score': 'rating','userName': 'user_name', 'reviewId': 'review_id', 'content': 'review_description', 'at': 'review_date', 'replyContent': 'developer_response', 'repliedAt': 'developer_response_date', 'thumbsUpCount': 'thumbs_up'},inplace = True)
g_df2.insert(loc=0, column='source', value='Google Play')
g_df2.insert(loc=3, column='review_title', value=None)
g_df2['laguage_code'] = 'en'
g_df2['country_code'] = 'in'

a_df = pd.DataFrame(np.array(a_reviews.reviews),columns=['review'])
a_df2 = a_df.join(pd.DataFrame(a_df.pop('review').tolist()))

a_df2.drop(columns={'isEdited'},inplace = True)
a_df2.insert(loc=0, column='source', value='App Store')
a_df2['developer_response_date'] = None
a_df2['thumbs_up'] = None
a_df2['laguage_code'] = 'en'
a_df2['country_code'] = 'in'
a_df2.insert(loc=1, column='review_id', value=[uuid.uuid4() for _ in range(len(a_df2.index))])
a_df2.rename(columns= {'review': 'review_description','userName': 'user_name', 'date': 'review_date','title': 'review_title', 'developerResponse': 'developer_response'},inplace = True)
a_df2 = a_df2.where(pd.notnull(a_df2), None)

result = pd.concat([g_df2,a_df2])
result

result = result[~result['review_description'].str.contains('zuai', case=False)]

# 1. Donut Pie Chart
total_ratings = len(result)
rating_counts = result['rating'].value_counts().sort_index()
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red']
explode = (0.05, 0, 0, 0, 0)  # explode the 1-star slice

# Create the donut plot
fig, ax = plt.subplots()
ax.pie(rating_counts, radius=1.2, colors=colors, labels=[f"{star_rating} ({count})" for star_rating, count in rating_counts.items()], autopct='%1.1f%%',
       startangle=90, pctdistance=0.85, explode=explode)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title(f'Review Ratings (Total: {total_ratings})')
plt.legend(rating_counts.index, title='Star Ratings', loc='upper left', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()

# 2. Stacked Bar Chart
user_experience_keywords = ['crash', 'crashed', 'UI', 'UX']
subscription_keywords = ['premium', 'costly']
curriculum_keywords = ['lacking', 'my subject', 'maths']
ai_keywords = ['AI', 'bot', 'slow']

user_experience_reviews = result['review_description'].str.contains('|'.join(user_experience_keywords), case=False)
subscription_reviews = result['review_description'].str.contains('|'.join(subscription_keywords), case=False)
curriculum_reviews = result['review_description'].str.contains('|'.join(curriculum_keywords), case=False)
ai_reviews = result['review_description'].str.contains('|'.join(ai_keywords), case=False)

categories = pd.DataFrame({
    'User Experience': user_experience_reviews.groupby(result['rating']).sum(),
    'Subscription': subscription_reviews.groupby(result['rating']).sum(),
    'Curriculum': curriculum_reviews.groupby(result['rating']).sum(),
    'AI': ai_reviews.groupby(result['rating']).sum()
})

fig, ax = plt.subplots(figsize=(8, 6))
ax = categories.plot(kind='bar', stacked=True, ax=ax, color=['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'])
ax.set_xlabel('Star Rating')
ax.set_ylabel('Number of Reviews')
ax.set_title('Review Categories by Star Rating')
ax.legend(title='Categories', loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()
