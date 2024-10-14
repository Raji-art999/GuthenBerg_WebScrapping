# # -*- coding: utf-8 -*-
# from nltk.tag.stanford import StanfordNERTagger
# from nltk.tokenize import word_tokenize
# from nltk import pos_tag
# import nltk

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# # Set the paths to the Stanford NER model and JAR file
# stanford_ner_model = '/Users/sundaramrajashree/PycharmProjects/Webscraping/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'
# stanford_ner_jar = '/Users/sundaramrajashree/PycharmProjects/Webscraping/stanford-ner-2020-11-17/stanford-ner.jar'

# # Initialize Stanford NER Tagger
# ner_tagger = StanfordNERTagger(stanford_ner_model, stanford_ner_jar, encoding='utf-8')

# text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'

# # Tokenize the text
# tokenized_text = word_tokenize(text)

# # Perform NER tagging
# ner_results = ner_tagger.tag(tokenized_text)

# # Perform POS tagging
# pos_results = pos_tag(tokenized_text)

# print('NER Classification:', ner_results)
# print('POS Tagging:', pos_results)




import os
from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk
import csv

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Set the paths to the Stanford NER model and JAR file
stanford_ner_model = '/Users/sundaramrajashree/PycharmProjects/Webscraping/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'
stanford_ner_jar = '/Users/sundaramrajashree/PycharmProjects/Webscraping/stanford-ner-2020-11-17/stanford-ner.jar'

# Initialize Stanford NER Tagger
ner_tagger = StanfordNERTagger(stanford_ner_model, stanford_ner_jar, encoding='utf-8')

# Specify the input and output folder paths
input_folder_path = '/Users/sundaramrajashree/PycharmProjects/Webscraping/sent_split_data'
output_folder_path = '/Users/sundaramrajashree/PycharmProjects/Webscraping/standfordNLP_tagger_result'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Process files in the specified input folder and save tagged information to the output folder
for root, dirs, files in os.walk(input_folder_path):
    for file in files:
        if file.endswith('.txt'):
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_folder_path, file.replace('.txt', '_tagged.csv'))

            # Read text from the input file
            with open(input_file_path, 'r') as file:
                text = file.read()

            # Tokenize the text
            tokenized_text = word_tokenize(text)

            # Perform NER tagging
            ner_results = ner_tagger.tag(tokenized_text)

            # Perform POS tagging
            pos_results = pos_tag(tokenized_text)

            # Save results to CSV
            with open(output_file_path, 'w', newline='') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(['Word', 'NER Tag', 'POS Tag'])
                for word, ner_tag in zip(tokenized_text, ner_results):
                    csv_writer.writerow([word, ner_tag[1], pos_results[tokenized_text.index(word)][1]])

            print(f'Tagged information saved to {output_file_path}')

