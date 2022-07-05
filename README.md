# Piki Music Dataset
We present the **Piki Music dataset** with the goal of enabling researchers and practitioners from the RecSys community to mitigate the **noisy feedback** and **self-selection biases** inherent in the data collected by existing music platforms. 

**Noisy feedback** biases arise in implicit data sets collected by streaming apps. Such apps collect user actions without recording the context of the user and without the knowledge that they are being surveyed. Consequently, a song stream from a recommended playlist may be falsely interpreted as an indication that the song was enjoyed, when in fact it was played in the background. A skipped song may be falsely interpreted as an indication that the song was dislike, when in fact the user may not be in the mood for the song in their present context. **Self-selection** biases arise in explicit data sets collected by apps that ask users to give ratings. Since rating is optional, the users most incentivized to rate are users who are very happy or very unhappy about their experience with the rated item.

The Piki Music dataset currently consists of 6696 anonymized users, 181,663 anonymized songs and 1,017,947 binary ratings and the data collection is still on-going. The Piki Music app is available for download [here](https://piki.page.link/AcVj).

The columns of the dataset are as following:
• timestamp: a datetime variable
• user_id: an anonymized user id
• song_id: an anonymized song id
• liked: this is the feedback indicator, 2 if the song is superliked, 1 if the song is liked, or 0 if the song is disliked. Note that the feedback consists
of 39% likes and 61% dislikes. Before January 3rd 2021, users could rate a song as soon as the music video was launched. After January 3rd 2021, the dislike button is enabled after 3 seconds, the like button is enabled after 6 seconds and the superlike button is enabled after 12 seconds. Superliked songs are saved to a playlist.
• personalized: this is 1 if the song was recommended based on their previous choices or 0 if the song was selected
randomly. Note that the songs recommended are 66% personalized and 34% random songs. We have included
this flag in the dataset, to allow mitigation of the recommendation bias of the data, though this question is not
within the scope of our study.
• spotify_popularity: this is the song’s artist’s popularity, a value between 0 and 100, with 100 being the most
popular. It is published by Spotify for each artist, through their publicly-available API

In this repo, we release the dataset(`data/piki_dataset.csv`) and the code for conducting the experiments in our paper ["Evaluating Music Recommendations with Binary Feedback for Multiple Stakeholders"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3919046)

If you're interested in a very quick intro, [here](https://www.youtube.com/watch?v=2f74yQjhCkk) is a 7 min video intro to the paper.

To get familiar with the dataset and reproduce the results in the paper, install the dependencies and start by running the python script:

```
python evaluate_stakeholders.py
```

We show that a matrix factorization algorithm trained on binary feedback performs significantly better compared to one trained only on likes for stakeholders such as consumers, well-known artists and lesser-known artists.


If you are interested using the dataset for you research, please kindly cite our paper. Contact @sstoikov if you have any feedback or questions on the dataset.
