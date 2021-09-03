import numpy as np
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics

from warnings import simplefilter 
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

from util import preprocessing,load_dataset
from wrmf import train_weighted_model


def pop_stakeholder_metric(test_set):
    # define thresholds 
    pop_median = np.median(test_set["popularity"])
    rec_mask = test_set["popularity"] >= pop_median
    rec_set = test_set[rec_mask]
    head_mask = rec_set["popularity"] >= pop_median
    tail_mask = rec_set["popularity"] < pop_median
    head_set = rec_set[head_mask]
    tail_set = rec_set[tail_mask]
    
    print("Pop: User - Recommendation Precision:", np.mean(rec_set["liked"]))
    print("Pop: Head - Recommendation Precision:", np.nanmean(head_set["liked"]))
    
    
    rec_mask = test_set["popularity"] < pop_median
    rec_set = test_set[rec_mask]
    head_mask = rec_set["popularity"] >= pop_median
    tail_mask = rec_set["popularity"] < pop_median
    head_set = rec_set[head_mask]
    tail_set = rec_set[tail_mask]
    print("Antipop: User - Recommendation Precision:", np.mean(rec_set["liked"]))
    print("Antipop: Tail - Recommendation Precision:", np.nanmean(tail_set["liked"]))



def stakeholder_metric(model, test_set):
    pred_scores = model.serve(test_set[["user_id", "item_id"]])["outputs"][0]    
    # define thresholds 
    pred_th = np.median(pred_scores)
    pop_median = np.median(test_set["popularity"])
    
    pred_labels = np.array([1.0 if score > pred_th else 0.0 for score in pred_scores])
    rec_mask = np.array([True if score > pred_th else False for score in pred_scores])
    rec_set = test_set[rec_mask]
    head_mask = rec_set["popularity"] >= pop_median
    tail_mask = rec_set["popularity"] < pop_median
    head_set = rec_set[head_mask]
    tail_set = rec_set[tail_mask]
    
    print("User - Recommendation Precision:", np.mean(rec_set["liked"]))
    print("Head - Recommendation Precision:", np.mean(head_set["liked"]))
    print("Tail - Recommendation Precision:", np.mean(tail_set["liked"]))
    
    print("Overall Accuracy:", metrics.accuracy_score(test_set["liked"], pred_labels))
    print("Head - Recommendation Percentage:", np.mean(head_mask))
    print("Tail - Recommendation Percentage:", np.mean(tail_mask))
    
    
if __name__ == '__main__':
  
    clean_df = preprocessing(dataset_dir='./data/piki_dataset.csv')
    print(len(clean_df))
    
    # split into training and testing
    train_df, test_df = train_test_split(clean_df,
                                         stratify=clean_df['user_id'], 
                                         test_size=0.2)
    print('# interactions on Train set: %d' % len(train_df))
    print('# interactions on Test set: %d' % len(test_df))


    data, user_id_map, item_id_map = load_dataset(train_df.drop(columns="timestamp"), test_df.drop(columns="timestamp"))

    print("Popularity baselines:")
    pop_stakeholder_metric(data["test"])

    # WRMF with Likes: 
    # corresponding to alpha=0.5, beta=0, gamma=0.5 in eq.3 in the paper.
    model_sample_ratios={
        'like-head': 0.25,
        'like-tail': 0.25,
        'dislike-head': 0.0,
        'dislike-tail': 0.0
    }


    wrmf_implicit_model = train_weighted_model(data, 
                                          group_sample_ratios = model_sample_ratios,
                                          test_set=data["test"],
                                          total_iter=3000,
                                          eval_iter=1000,
                                          batch_size=1000,
                                          dim=20,
                                          num_negatives=100)


    stakeholder_metric(wrmf_implicit_model, data["test"])

    # WRMF with Likes and Dislikes: 
    # corresponding to alpha=0.5, beta=0.5, gamma=0 in eq.3 in the paper.
    model_sample_ratios={
        'like-head': 0.25,
        'like-tail': 0.25,
        'dislike-head': 0.25,
        'dislike-tail': 0.25
    }


    wrmf_binary_weighted_model = train_weighted_model(data, 
                                          group_sample_ratios = model_sample_ratios,
                                          test_set=data["test"],
                                          total_iter=3000,
                                          eval_iter=1000,
                                          batch_size=1000,
                                          dim=20,
                                          num_negatives=100)


    stakeholder_metric(wrmf_binary_weighted_model, data["test"])
