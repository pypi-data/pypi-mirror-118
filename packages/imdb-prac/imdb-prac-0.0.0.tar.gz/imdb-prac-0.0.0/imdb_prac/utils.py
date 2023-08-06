import os
import logging
import json
import random
import torch
import numpy as np
from tokenizers import Tokenizer
MODEL_CLASSES={
    'h_rnn':(Tokenizer,),
}
MODEL_PATH={
    "h_rnn":".\saved_models\\rnn_model\\",
}

def load_posTag(args):
    with open(os.path.join(args.data_dir,'pos_vocab.json'),'r',encoding='utf-8') as f_r:
        pos_tags=json.load(f_r)
    
    return pos_tags

# set random seed
def set_randomSeed(args):
    random.seed(args.random_seed)
    np.random.seed(args.random_seed)
    torch.random.manual_seed(args.random_seed)
    torch.cuda.manual_seed_all(args.random_seed)


# set logger logging message
def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        datefmt=r'%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)
