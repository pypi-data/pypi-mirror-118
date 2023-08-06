# TakeBlipPosTagging Package
_Data & Analytics Research_

## Overview

NER (Named Entity Recognition) is an NLP problem that aims to locate and classify entities in a text. 
This implementation uses BiLSTM-CRF for solving the NER task utilizing PyTorch framework for training a supervised model and predicting in CPU. 
For training, it receives a pre-trained FastText Gensim embedding and a .csv file. It outputs three pickle files: model, word vocabulary and label vocabulary. 
Example of classes that can be trained:

- Financial [FIN]
- Generic [GEN]
- Company [COMP]
- Number [NUMBER]
- Document [DOC]
- Location [LOC]
- Person [PERS]
- Phone [PHONE]
- Address [ADDR]
- Email [EMAIL]
- Date [DATE]
- Week Day [WD]
- Money [MONEY]
- Relatives [REL]
- Vocatives [VOC]

Some additional information is used to identify where the recognized entity begins and ends.

- The letter B indicates the beginning of the CLASS class entity;
- The letter I indicates that the respective token is a continuation of the class with the name CLASS started;
- The letter O indicates that no entity related to the token was found;

For example, the sentence "ligar internet a cabo!" would be classified as "O O B-GEN I-GEN I-GEN O", 
where B-GEN represents the beginning of the GEN entity (token "internet") and the next two tokens are 
the continuation of the entity (tokens "a cabo"). In this way, the entity found in the sentence would be 
"internet a cabo" of the GEN class.

Here are presented these content:

* [Installation](#installation)
* [File Format](#fileformat)
* [Configure](#configure)
* [Run](#run)


## Installation

This version works in:

* PyTorch: 1.7.1
* Python: 3.6

## Conda env ##

In order to create a local environment to run the project, it's needed to create a conda environment
- In Windows OS:

``` conda env create -f files\conda_env\ner-predict-windows.yml```

- In Linux OS:

``` conda env create -f files/conda_env/ner-linux-windows.yml```

## Training ##

Prepare data first. Data must be supplied in one csv file where the first column contain the sentences and the second one the respective labels for that sentence. File might be prepared as follows:

    (sample.csv)
	MessageProcessed,		    Tags
    Ativar o meu cartão,	    O O O B-FIN
    Ligar a internet de cabo!,  	    O O B-GEN I-GEN I-GEN O
    ...,				    ...
    
Then the above input is provided to `train.py` using `--input-path` and the column name for the sentences and the labels using `--sentence_column` and `--label_column`.

    python local_train.py --input-path *.csv --sentence_column MessageProcessed --label_column Tags ...

You might need to setup several more parameters in order to make it work. 

A few parameters available on training are:

* `--batch-size`: number of sentences in each batch.
* `--epochs`: number of epochs
* `--learning_rate`: learning rate parameter value

And parameters for validation and early stopping. 

## Our Training ##
For local execution run command:

	python local_train.py --postag_model_path *.pkl --postag_label_path *.pkl --input-path *.csv --separator ,   --sentence_column MessageProcessed --label_column Tags --save-dir * --wordembed-path *.kv --epochs 5

	python local_train.py --postag_model_path *.pkl --postag_label_path *.pkl --input-path *.csv --separator , --sentence_column MessageProcessed --label_column Tags --save-dir * --wordembed-path f*.kv --epochs 5 --val --val-path *.csv --bidirectional --val-period 1e
    
    python local_train.py --postag_model_path *.pkl --postag_label_path *.pkl --input-path *.csv --separator , --sentence_column MessageProcessed --label_column Tags --save-dir * --wordembed-path *.kv --epochs 5 --val --val-path *.csv --bidirectional --val-period 10i --max-decay-num 2 --max-patience 2 --learning-rate-decay 0.1 --patience-threshold 0.98
 
## Prediction ##
For local execution run command for one line predict:

	python local_predict.py --model-path *.pkl --ner-label-vocab *.pkl --postag-model-path *.pkl --postag-label-path *.pkl --input-sentence "eu quero prever essa frase" --label-vocab *.pkl --save-dir *.csv --wordembed-path *.kv

For local execution run command for batch predict:

	python local_predict.py --model-path *.pkl --ner-label-vocab *.pkl --postag-model-path *.pkl --postag-label-path *.pkl --input-path *.csv --sentence_column MessageProcessed --label-vocab *.pkl --save-dir *.csv --wordembed-path *.kv
	
	python local_predict.py --model-path *.pkl --ner-label-vocab *.pkl --postag-model-path *.pkl --postag-label-path *.pkl --input-path *.csv --sentence_column MessageProcessed --label-vocab *.pkl --save-dir *.csv --wordembed-path *.kv --use-lstm-output

Data must be supplied in one csv file with one column which contain the sentences. File might be prepared as follows:

    (sample.csv)
	MessageProcessed
    Ativar o meu cartão
    Ligar a internet de cabo!
    ...,	
