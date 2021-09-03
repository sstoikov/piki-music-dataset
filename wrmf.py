from openrec.tf1.model_trainer import ModelTrainer
from openrec.tf1.utils import Dataset
from openrec.tf1.recommenders import PMF
from openrec.tf1.utils.evaluators import AUC, Recall
from openrec.tf1.utils.samplers import StratifiedPointwiseSampler
from openrec.tf1.utils.samplers import EvaluationSampler
from openrec.tf1.utils.samplers import Sampler
import numpy as np
import random
from collections import defaultdict

  
def WeightedPointwiseSampler(batch_size, 
                             dataset, 
                             group_sample_ratios,
                             num_process=5,
                             th=52,
                             seed=100):
    
    random.seed(seed)
    def batch(dataset=dataset, batch_size=batch_size, seed=seed):
        
        group_samples = {k: int(batch_size * v) for k, v in group_sample_ratios.items()}
        target_sample_num = sum(list(group_samples.values()))
        
        while True:
            
            input_npy = np.zeros(batch_size, dtype=[('user_id', np.int32),
                                                    ('item_id', np.int32),
                                                    ('label', np.float32)])
            
            ind = 0
            group_counts = defaultdict(int)
            
            while ind < target_sample_num:
                entry = dataset.next_random_record()
                #print("sampled count: ", ind, "target count:" , target_sample_num, "\n")
                # Case: Like-Head
                if entry['liked'] and (entry['popularity'] >= th):
                    group = 'like-head'
                    if group_counts[group] < group_samples[group]:
                        input_npy[ind] = (entry['user_id'], entry['item_id'], 1.0)
                        group_counts[group] += 1
                        ind += 1
                
                # Case: Like-Tail
                elif entry['liked'] and (entry['popularity'] < th):
                    group = 'like-tail'
                    if group_counts[group] < group_samples[group]:
                        input_npy[ind] = (entry['user_id'], entry['item_id'], 1.0)
                        group_counts[group] += 1
                        ind += 1
                
                # Case: Dislike-Head
                elif (not entry['liked']) and (entry['popularity'] >= th):
                    group = 'dislike-head'
                    if group_counts[group] < group_samples[group]:
                        input_npy[ind] = (entry['user_id'], entry['item_id'], 0.0)
                        group_counts[group] += 1
                        ind += 1
                
                # Case: Dislike-Head
                elif (not entry['liked']) and (entry['popularity'] < th):
                    group = 'dislike-tail'
                    if group_counts[group] < group_samples[group]:
                        input_npy[ind] = (entry['user_id'], entry['item_id'], 0.0)
                        group_counts[group] += 1
                        ind += 1
                else:
                    print("Unrecognized groups!")

            for i in range(batch_size - target_sample_num):
                user_id = random.randint(0, dataset.total_users()-1)
                item_id = random.randint(0, dataset.total_items()-1)
                while dataset.is_positive(user_id, item_id):
                    user_id = random.randint(0, dataset.total_users()-1)
                    item_id = random.randint(0, dataset.total_items()-1)
                input_npy[ind+i] = (user_id, item_id, 0.0)
            
            yield input_npy
        
    
    s = Sampler(dataset=dataset, generate_batch=batch, num_process=num_process)
    
    return s

  
def train_weighted_model(data,
                test_set,
                group_sample_ratios,
                batch_size=1000,
                total_iter=2000, 
                eval_iter=2000,
                dim=20,
                num_negatives=None,
                eval_explicit=False,
):
    ### embeding ### 
    dim_user_embed = dim     # dimension of user embedding
    dim_item_embed = dim     # dimension of item embedding

    l2_reg=0.0001

    
    # prepare train, val, test sets and samplers
    train_dataset = Dataset(data['train'], data['total_users'], data['total_items'], name='Train')    
    
    
    train_sampler = WeightedPointwiseSampler(batch_size=batch_size, 
                                             dataset=train_dataset, 
                                             group_sample_ratios=group_sample_ratios,
                                             num_process=4)

    test_dataset = Dataset(test_set,  data['total_users'], data['total_items'], 
                           implicit_negative=not eval_explicit, name='Test', num_negatives=num_negatives)
    test_sampler = EvaluationSampler(batch_size=batch_size, dataset=test_dataset)
    eval_samplers = [test_sampler]

    # set evaluators
    evaluators = []


    # set model parameters
    model = PMF(l2_reg=l2_reg, 
                batch_size=batch_size, 
                total_users=train_dataset.total_users(), 
                total_items=train_dataset.total_items(), 
                dim_user_embed=dim_user_embed, 
                dim_item_embed=dim_item_embed, 
                train=True, 
                serve=True)


    # set model trainer
    model_trainer = ModelTrainer(model=model)  
    model_trainer.train(total_iter=total_iter, 
                        eval_iter=eval_iter, 
                        save_iter=eval_iter, 
                        train_sampler=train_sampler, 
                        eval_samplers=eval_samplers, 
                        evaluators=evaluators)
    return model
