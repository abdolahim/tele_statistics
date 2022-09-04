import json
from collections import Counter
from pathlib import Path
from typing import Union

import arabic_reshaper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    def __init__(self, chat_json: Union[str, Path]):
        #Load Chat Data
        logger.info(f"Loading chat data from {chat_json} ")
        with open(Path(chat_json)) as f:
            self.chat_data = json.load(f)
            self.normalizer = Normalizer()

        #Load Stopwords
        logger.info(f"Loading chat data from {DATA_DIR/'stop_words.txt'} ")
        stop_words = open(DATA_DIR/'stop_words.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize, stop_words))

    def generate_word_cloud(self, output_dir:Union[str, Path], width=2000, height=2000):
        logger.info(f"Generating word cloud in {output_dir} ")
        text_content = ''
        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item : item not in self.stop_words, tokens))        
                text_content += f" {' '.join(tokens)}"
            elif type(msg['text']) is list:
                for sub_msg in msg['text']:
                    if type(sub_msg) is str:
                        tokens = word_tokenize(sub_msg)
                        tokens = list(filter(lambda item : item not in self.stop_words, tokens))
                        text_content += f" {' '.join(tokens)}"   
        text_content = arabic_reshaper.reshape(text_content)
        # text_content = get_display(text_content)
        logger.info(f"Generating word cloud")
        wordcloud = WordCloud(
            width=2000,
            height=2000,
            font_path=str(DATA_DIR/'B Homa.ttf'),
            background_color='white',
            ).generate(text_content)
        logger.info(f"Saving word cloud in {output_dir}")    
        wordcloud.to_file(str(Path(output_dir)/'wordcloud.png'))
      

if __name__ == "__main__":
    chat_stats = ChatStatistics(chat_json=DATA_DIR/'result.json')
    chat_stats.generate_word_cloud(output_dir=DATA_DIR)
    print('done!')
    