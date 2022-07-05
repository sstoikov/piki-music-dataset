# Piki Music Dataset
We present the **Piki Music dataset** with the goal of enabling researchers and practitioners from the RecSys community to mitigate the *noisy feedback* and *self-selection biases* inherent in the data collected by existing music platforms. 

Noisy feedback biases often arise in implicit data sets collected by streaming apps. These apps collect user actions, such as plays, skips and additions to playlists, without recording the context of the user. For example, a song stream from a recommended playlist may be falsely interpreted as an indication that the song was enjoyed, when in fact it was played in the background. A song that is skipped may be falsely interpreted as an indication that the song was dislike, when in fact the user may not be in the mood for the song in their present context.

The Piki Music dataset currently consists of 2723 anonymized users, 66,532 anonymized songs and 500K binary ratings and the data collection is still on-going. The Piki Music app is available for download [here](https://piki.page.link/AcVj).

In this repo, we release the dataset(`data/piki_dataset.csv`) and the code for conducting the experiments in our paper ["Evaluating Music Recommendations with Binary Feedback for Multiple Stakeholders"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3919046)

If you're interested in a very quick intro, [here](https://www.youtube.com/watch?v=2f74yQjhCkk) is a 7 min video intro to the paper.

To get familiar with the dataset and reproduce the results in the paper, install the dependencies and start by running the python script:

```
python evaluate_stakeholders.py
```

We show that a matrix factorization algorithm trained on binary feedback performs significantly better compared to one trained only on likes for stakeholders such as consumers, well-known artists and lesser-known artists.


If you are interested using the dataset for you research, please kindly cite our paper. Contact @sstoikov if you have any feedback or questions on the dataset.
