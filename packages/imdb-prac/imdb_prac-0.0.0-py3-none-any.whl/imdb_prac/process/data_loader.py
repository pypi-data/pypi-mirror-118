import os
import logging
import copy
import json
import torch
import spacy
import random
from collections import namedtuple
from utils import load_posTag

logger = logging.getLogger(__name__)
InputFeature=namedtuple("Example",['uid','sents','label'])
RnnFeature=namedtuple("RnnExample", ['sents','pos_sents','label'])


class textExtracter:
    def __init__(self, nlp_name,use_gpu,max_sents):
        if use_gpu:
            spacy.require_gpu()
        self.nlp_pipe = spacy.load(nlp_name)
        self.max_sents=max_sents
    @classmethod
    def _read_file(self, folder_path,data_num):
        lines = []
        for i,f_name in os.listdir(folder_path):
            with open(os.path.join(folder_path,f_name), 'r', encoding='utf-8') as f_r:
                for line in f_r:
                    line = line.strip()
                    lines.append(line)
            if i==data_num:
                break
        return lines

    def create_examples(self, set_type,input_text,label):
        examples = []
        for idx,text in enumerate(input_text):
            uid = '%s-%s' % (set_type, idx)
            # split text to sents
            doc=self.nlp_pipe(text.strip())
            sents=[sent.text for sent in doc.sents][:self.max_sents]           
            # add to examples
            examples.append(InputFeature(uid=uid, sents=sents,label=label))
        return examples

    def get_examples(self,data_dir,mode,data_num):
        '''
        Mode:train,test
        '''
        data_path = os.path.join(self.args.data_dir, mode)
        labels={'pos':1,'neg':0}
        #create sents for pos & neg data
        examples=[]
        for l in ['pos','neg']:
            f_path=os.path.join(data_dir,l)
            examples+=self.create_examples(mode,self._read_file(f_path,data_num),
                                           label=labels[l])
        examples=random.sample(examples)
        return examples

def convert_to_RnnFeatures(data, max_seqLen,
                           tokenizer,pos_tags):
    # 整理examples features
    examples = []
    for ex_id, example in enumerate(data):
        if ex_id % 5000 == 0:
            logger.info(f'Already convert {ex_id} examples!')
        #extract linguistic feature for ecah sent in one example
        sents_id=[]
        pos_sents=[]
        for s in data.sents:
            sent=self.nlp_pipe(s)
            p=[]
            s_ids=[]
            for t in sent:
                #using bpe tokenizer
                tok_ids=self.tokenizer.encode(t.text).ids
                pos_ids=len(tok_ids)*[pos_tags[t.pos_]]
                s_ids.extend(tok_ids)
                p.extend(pos_ids)
            #truncate value
            s_ids=s_ids[:max_seqLen]
            p=p[:max_seqLen]
            
            assert len(s_ids) == len(p) == max_seqLen
            #add into sents of doc
        sents_id.append(s_ids)
        pos_sents.append(p)

        if ex_id < 5:
            logger.info('****Display examples****')
            logger.info('Uid:{}'.format(example.guid))
            logger.info('token_ids:{}'.format(sents_id))
            logger.info('pos_ids:{}'.format(pos_sents))
            logger.info('label:{}'.format(example.label))

        examples.append(InputRnnFeatures(sents=sents_id,
                                         pos_sents=pos_sents,
                                         label=example.label))

    return examples


def load_and_cacheExampels(args, tokenizer, mode):
    # build extractor
    text_Etl=textExtracter(args.nlp_model,args.use_gpu,args.max_sent)
    pos_tags=load_posTag(args)
    # build load and save cached file path
    cached_file_path = os.path.join(args.data_dir, mode,
                                    'cached_{}_{}.zip'.format(
                                        mode,args.max_seqLen))

    if os.path.isfile(cached_file_path):
        # load features
        logger.info('loading data file from {}'.format(cached_file_path))
        features = torch.load(cached_file_path)
    else:
        # create examples
        if mode == 'train':
            examples = processer.get_examples(args.data_dir,mode,args.max_data_num)
        elif mode == 'test':
            examples = processer.get_examples(args.data_dir,mode,args.max_data_num)
        else:
            raise NameError('Mode args is not train,val,test!')

        if args.model_type.endswith('rnn'):
            features = convert_to_RnnFeatures(examples, args.max_seqLen, tokenizer, pos_tags)
        # save to cached file path
        torch.save(features, cached_file_path)
        logger.info(f'Save features to {cached_file_path}')


    # transform features into tensor
    dataset = TensorDataset(features)

    return dataset

    