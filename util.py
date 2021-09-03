import pandas as pd
import numpy as np
import sklearn.metrics as metrics


def preprocessing(dataset_dir):
    df=pd.read_csv(dataset_dir)
    # treat super like as like (2 --> 1)
    df["liked"] = [i if i < 2 else 1 for i in df["liked"]]
    print(len(df))

    # data cleaning parameters
    user_treshold=20 # at least 20 song ratings per user
    song_threshold=20 # at least 20 user ratings per song
    like_ratio_threshold=0.9 # filter users who have super high like ratios

    hot_users=df.groupby(['user_id']).count()[df.groupby(['user_id']).count()['liked']>user_treshold].index
    user_liked_ratio=df.groupby(['user_id']).mean()['liked']
    good_users=user_liked_ratio[(user_liked_ratio!=0) & (user_liked_ratio<like_ratio_threshold)].index
    song_liked_ratio=df.groupby(['song_id']).mean()['liked']
    good_songs=song_liked_ratio[(song_liked_ratio!=0) & (song_liked_ratio!=1)].index
    clean_df=df[df['user_id'].isin(good_users) 
                     & df['user_id'].isin(hot_users)
                     & df['song_id'].isin(good_songs)]
    hot_songs=clean_df.groupby(['song_id']).count()[clean_df.groupby(['song_id']).count()['liked']>song_threshold].index

    # songs must be over the cold start
    clean_df=clean_df[clean_df['song_id'].isin(hot_songs)]
    return clean_df


def load_dataset(train_df, test_df):
    train_structured_arr = np.zeros(len(train_df), dtype=[('user_id', np.int32), ('item_id', np.int32), ('liked', np.bool), 
                                                          ('label', np.float32), ('personalized', np.bool), ('popularity', np.float32)])
    test_structured_arr = np.zeros(len(test_df), dtype=[('user_id', np.int32), ('item_id', np.int32), ('liked', np.bool), 
                                                        ('label', np.float32), ('personalized', np.bool), ('popularity', np.float32)])

    map_to_item_id = dict()  # Map item id from 0 to len(items)-1
    map_to_user_id = dict()
    next_user_id = 0
    next_item_id = 0
    train_interaction_id = 0
    test_interaction_id = 0

    for record in train_df.values:
        user, item, liked, personalized, pop = record
        if user not in map_to_user_id:
            map_to_user_id[user] = next_user_id
            next_user_id += 1
        if item not in map_to_item_id:
            map_to_item_id[item] = next_item_id
            next_item_id += 1
        train_structured_arr[train_interaction_id] = (map_to_user_id[user], map_to_item_id[item], liked, liked, personalized, pop)
        train_interaction_id += 1

    for record in test_df.values:
        user, item, liked, personalized, pop = record
        if user not in map_to_user_id:
            map_to_user_id[user] = next_user_id
            next_user_id += 1
        if item not in map_to_item_id:
            map_to_item_id[item] = next_item_id
            next_item_id += 1
        test_structured_arr[test_interaction_id] = (map_to_user_id[user], map_to_item_id[item], liked, liked, personalized, pop)
        test_interaction_id += 1
        
    raw_data = dict()
    raw_data['total_users'] = next_user_id
    raw_data['total_items'] = next_item_id
    raw_data['train'] = train_structured_arr
    raw_data['test'] = test_structured_arr
    return raw_data, map_to_user_id, map_to_item_id 
