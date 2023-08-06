import os
from os import path
BASE_DIR=path.abspath(path.dirname(__file__))
#envirmonent settings
OUTPUT_DIR=os.environ.get("OUTPUT_MODELS_DIR",path.join(BASE_DIR,"outputs"))
DATA_DIR=os.environ.get("DATA_DIR",path.join(BASE_DIR,"Data"))

#training configs
MAX_VOCAB_SIZE=25000
SENTS_MAX_LEN=50
SENTS_NUMS=20
MIN_FREQ=2
SPECIAL_TOKENS=["[UNK]","[PAD]"]
ENTITY_MAPPINGS={"O":0,"GPE_B":1,"GPE_I":2,"LANGUAGE_B":3,"LANGUAGE_I":4,"LAW_B":5,"LAW_I":6,"LOC_B":7,
                  "LOC_I":8,"MONEY_B":9,"MONEY_I":10,"NORP_B":11,"NORP_I":12,"ORDINAL_B":13,"ORDINAL_I":14,
                  "ORG_B":15,"ORG_I":16,"PERCENT_B":17, "PERCENT_I":18,"PERSON_B":19, "PERSON_I":20,"PRODUCT_B":21,
                 "PRODUCT_I":22,"QUANTITY_B":23,"QUANTITY_I":24,"TIME_B":25,"TIME_I":26,"WORK_OF_ART_B":27,
                 "WORK_OF_ART_I":21}