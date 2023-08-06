from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.normalizers import Sequence,Lowercase,StripAccents
import logging
import argparse
import os

from imdb_prac.settings import *
from imdb_prac.process.text import strip_html,en_nlp
import pandas as pd
#get module name to log message
logger=logging.getLogger(__name__)

def generate_bpe(data_iter,min_freq,max_size):

    save_path=os.path.join(OUTPUT_DIR,"tokenizers")

    #build init tokenizer
    tokenizer=Tokenizer(BPE(unk_token="[UNK]",continuing_subword_prefix="##",
                            end_of_word_suffix="##"))
    trainer=BpeTrainer(special_tokens=["[PAD]","[UNK]"],min_frequency=min_freq,
                       vocab_size=max_size)

    #insert text clean process
    norm_pipe=Sequence([StripAccents(),Lowercase()])
    tokenizer.normalizer=norm_pipe
    tokenizer.pre_tokenizer=Whitespace()
    
    
    tokenizer.train_from_iterator(data_iter,trainer)

    #save trained tokenizer
    if os.path.isdir(save_path):
        logger.info("The model dir has already exists!")
    else:
        os.mkdir(save_path)
        logger.info(f"Create new folder in {save_path}")
    tokenizer.save(os.path.join(save_path,'tokenizer-imdb.json'))

def fetch_raw_data(folder_path,label,data_num):
    i=0
    for i,f_name in os.listdir(folder_path):
        data=[]
        
        with open(os.path.join(folder_path,f_name),"r",encoding='utf-8') as f_r:
            for line in f_r:
                doc=en_nlp(strip_html(line.strip()))
                #seprate line and add symbol for split
                doc="\n".join(list(doc.sents))
                data.append(doc)
        #add label
        data.append(label)
        if i>data_num:
            break
        yield data
        

def create_csv(src_path,dest_path,data_num):
    logger.info(f"------Start to get data from folder:{src_path}-------")
    datas=list(d for l in ['pos','neg'] for d in fetch_raw_data(src_path,l,data_num))
    df=pd.DataFrame(datas,columns=['text','label'])
    df=df.sample(frac=1)
    df.to_csv(dest_path,index=False,encoding="utf-8")


def main(args):
    if args.subparser_name=="data":
        load_path=os.path.join(args.src,args.type)
        create_csv(load_path,args.dst)

    elif args.subparser_name=="token":
        df=pd.read_csv(args.src)
        data_iter=list(sent for r_v in df["text"] for sent in r_v.split("\n") if sent )
        generate_bpe(data_iter,args.min_freq,args.max_size)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    subparsers=parser.add_subparsers(title="subcommand",dest="subparser_name",
                                     description="data: used for produce data and tokenizer",
                                    help="addition help")
    parser_data=subparsers.add_parser("data",help="data help")
    parser_data.add_argument("src",type=str,default=os.path.join(BASE_DIR,"aclImdb"),help="")
    parser_data.add_argument("dst",type=str,help="")
    parser_data.add_argument("-n","--num",type=int,help="")
    parser_data.add_argument("--type",type=str,choices=["train","test"],
                             help="convert spec data that used for train or testing.")

    #subcommand for training bpe tokenizer
    parser_token=subparsers.add_parser("token",help="token help")
    parser_token.add_argument("src",type=str)
    parser_token.add_argument('-mf',"--minfreq",type=int,default=1)
    parser_token.add_argument("-ms","--max_size",type=int,default=25000)
    
    args=parser.parse_args()
    main(args)

                 
                



