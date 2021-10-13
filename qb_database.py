import pandas


df_qb = pandas.read_csv('NFL_QB_Search.csv')
print(df_qb)

df_qb_images = pandas.read_csv('NFL_QB_Search_Images.csv')
print(df_qb_images)

for i in df_qb.Player:
    for j in df_qb_images.Player:
        if i == j:
            df_merge = df_qb.merge(df_qb_images[['Player']])