# Piki Music Dataset

We collect binary data while incentivizing users to provide feedback in a way that is aligned with their individual tastes. The columns of the dataset are as following: 

- timestamp: a datetime variable
- user_id: an anonymized user id
- song_id: an anonymized song id
- liked: this is the binary indicator, 1 if the song is liked, or 0 if the song is disliked. Note that the feedback consists of 39\% likes and 61\% dislikes. The superlike indicator, labeled 2, is included in the data, though we treat it as a like in our experiments.
- personalized: this is 1 if the song was recommended based on their previous choices or 0 if the song was selected randomly. Note that the songs recommended are 66\% personalized and 34\% random songs. We have included this flag in the dataset, to allow mitigation of the recommendation bias of the data, though this question is not within the scope of our study.
- spotify_popularity: this is the song's artist's popularity, a value between 0 and 100, with 100 being the most popular. It is published by Spotify for each artist, through their publicly-available API(https://developer.spotify.com/documentation/web-api/reference/#category-artists). The average value of the Spotify popularity in our data set is 52, so we classify songs as coming from well-known artists if the value is above this mean and as a lesser-known artist if it is below the mean. Note that this threshold corresponds to artists that have approximately 350,000 monthly listeners, which on average generates around \$2000 per month, assuming this is a solo artist without a label.
- treatment_group: the amount of time needed to unlock the like button. 1 if the timer is 3 seconds, 2 if the timer is 6 seconds, 3 if the timer is 9 seconds.

In an effort to mitigate ratings inflation and incentivize ratings in line with a user's true opinions, Piki implemented a set of timers on each of the ratings options on February 21, 2021. Since then, users have not been able to \textit{immediately} rate a song after it begins playing. Instead, each of the dislike,'' like'' and ``super-like'' buttons appear sequentially in that order, several seconds after the song begins playing or the previous button appears.

During the period of August 19, 2022 to December 5, 2022, a randomized controlled trial was performed, where the amount of time needed to unlock the like button was changed. Treatment groups had timers of 3, 6, and 9 seconds.
