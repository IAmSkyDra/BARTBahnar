import pandas as pd
import numpy as np
import random
import string
from itertools import permutations
import re 

# # Add path, language and config the code. After done configing, go to runner to run the code.

# LANG_SOURCE = 'tiếng bana'
# LANG_TARGET = 'tiếng việt'
# INPUT_PATH = 'augment/test.csv' # Path to the input file (csv has 2 cols: LANG_SOURCE, LANG_TARGET)
# DICTIONARY_PATH = 'augment/dictionary.csv' # Path to the dictionary file (csv has 3 cols: LANG_SOURCE, LANG_TARGET, TYPE)

# ## CONFIG ##
# ### Replace with same type:
# LIMIT_NEW_SENTENCES = 10
# ### Combine:
# BATCH_SIZE = 10
# ### Random Insertion:
# NUM_INSERTIONS = 1
# MAX_LINES_GENERATED = 10
# ### Random Deletion:
# NUM_DELETIONS = 1
# ### Sliding Windows:
# WINDOW_SIZE = 2


class augmentmethods:
    def __init__(self, lang_source, lang_target, input_path):
        self.data = pd.read_csv(input_path, encoding='utf-8')
        self.lang_source = lang_source
        self.lang_target = lang_target
    
    def augment(self, data):
        data = self.data
        print('Input size:', len(data))
        print('Output size:', len(data))
        return data
    
    def dataToCSV(self, data, output_path):
        data.to_csv(output_path, index=False, encoding='utf-8')
        print('Data saved to', output_path)
        

class Combine(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path, batch_size):
        super().__init__(lang_source, lang_target, input_path)
        self.batch_size = batch_size
    
    def augment(self, data):
        data = self.data
        data = data.values
        combined_data = []
        for i in range(0, len(data), self.batch_size):
            batch = data[i:i + self.batch_size]
            for a, b in permutations(batch, 2):
                combined_data.append([f"{a[0]} {b[0]}", f"{a[1]} {b[1]}"])
        combined_data = pd.DataFrame(combined_data, columns=[self.lang_source, self.lang_target])
        print('Input size:', len(self.data))
        print('Output size:', len(combined_data))
        return combined_data

class SwapSentences(augmentmethods):
    def __init__ (self, lang_source, lang_target, input_path):
        super().__init__(lang_source, lang_target, input_path)
    
    def augment(self, data):
        data = self.data
        data = data.values
        swapped_data = []
        delimiters = ".;?!"
        for a, b in data:
            sentences_a = [sentence.strip() for sentence in re.split(f'[{delimiters}]', a) if sentence]
            sentences_b = [sentence.strip() for sentence in re.split(f'[{delimiters}]', b) if sentence]
            if len(sentences_a) == len(sentences_b):  # Ensure both sides have the same number of sentences
                for perm in permutations(range(len(sentences_a))):
                    perm_a = [sentences_a[i] for i in perm]
                    perm_b = [sentences_b[i] for i in perm]
                    swapped_data.append(['. '.join(perm_a) + '.', '. '.join(perm_b) + '.'])
        swapped_data = pd.DataFrame(swapped_data, columns=[self.lang_source, self.lang_target])
        print('Input size:', len(self.data))
        print('Output size:', len(swapped_data))
        return swapped_data
    
class ReplaceWithSameType(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path, dictionary_path, limit_new_sentences):
        super().__init__(lang_source, lang_target, input_path)
        self.dictionary = pd.read_csv(dictionary_path, encoding='utf-8')
        self.limit_new_sentences = limit_new_sentences
    
    def augment(self, data):
        data = self.data
        dictionary = self.dictionary
        data = data.values
        replaced_data = []
        for a, b in data:
            words_a = a.split()
            words_b = b.split()
            new_sentences = set()
            for i, word in enumerate(words_a):
                word_type = dictionary[(dictionary[self.lang_source].str.len() == len(word)) & (dictionary[self.lang_source] != word)][self.lang_target].values
                if len(word_type) > 0:
                    for _ in range(min(self.limit_new_sentences, len(word_type))):
                        new_word = random.choice(word_type)
                        new_sentence = words_a[:i] + [new_word] + words_a[i+1:]
                        new_sentences.add(' '.join(new_sentence))
            for i, word in enumerate(words_b):
                word_type = dictionary[(dictionary[self.lang_target].str.len() == len(word)) & (dictionary[self.lang_target] != word)][self.lang_source].values
                if len(word_type) > 0:
                    for _ in range(min(self.limit_new_sentences, len(word_type))):
                        new_word = random.choice(word_type)
                        new_sentence = words_b[:i] + [new_word] + words_b[i+1:]
                        new_sentences.add(' '.join(new_sentence))
            for sentence in new_sentences:
                replaced_data.append([sentence, ' '.join(words_b)])
        replaced_data = pd.DataFrame(replaced_data, columns=[self.lang_source, self.lang_target])
        print('Input size:', len(self.data))
        print('Output size:', len(replaced_data))
        return replaced_data
    
class RandomInsertion(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path, dictionary_path, num_insertions, max_lines_generated):
        super().__init__(lang_source, lang_target, input_path)
        self.dictionary = pd.read_csv(dictionary_path, encoding='utf-8')
        self.num_insertions = num_insertions
        self.max_lines_generated = max_lines_generated
        
    def augment(self, data):
        data = self.data
        dictionary = self.dictionary
        data = data.values
        inserted_data = []
        for a, b in data:
            words_a = a.split()
            words_b = b.split()
            for _ in range(self.max_lines_generated):
                new_words_a = words_a[:]
                new_words_b = words_b[:]
                for _ in range(self.num_insertions):
                    pos_a = random.randint(0, len(new_words_a)) if len(new_words_a) > 0 else 0
                    pos_b = random.randint(0, len(new_words_b)) if len(new_words_b) > 0 else 0
                    insert_word_a = random.choice(dictionary[self.lang_source].dropna().values)
                    insert_word_b = random.choice(dictionary[self.lang_target].dropna().values)
                    new_words_a.insert(pos_a, insert_word_a)
                    new_words_b.insert(pos_b, insert_word_b)
                inserted_data.append([' '.join(new_words_a), ' '.join(new_words_b)])
        inserted_data = pd.DataFrame(inserted_data, columns=[self.lang_source, self.lang_target])
        print('Input size:', len(self.data))
        print('Output size:', len(inserted_data))
        return inserted_data
    
class RandomDeletion(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path, num_deletions):
        super().__init__(lang_source, lang_target, input_path)
        self.num_deletions = num_deletions
    
    def augment(self, data):
        data = self.data
        data = data.values
        deleted_data = []
        for a, b in data:
            words_a = a.split()
            words_b = b.split()
            for _ in range(self.num_deletions):
                for i in range(len(words_a)):
                    if len(words_a) > 1 and len(words_b) > 1:
                        new_words_a = words_a[:]
                        new_words_b = words_b[:]
                        index_a = i if i < len(new_words_a) else len(new_words_a) - 1
                        index_b = i if i < len(new_words_b) else len(new_words_b) - 1
                        new_words_a.pop(index_a)
                        new_words_b.pop(index_b)
                        deleted_data.append([' '.join(new_words_a), ' '.join(new_words_b)])
        deleted_data = pd.DataFrame(deleted_data, columns=[self.lang_source, self.lang_target])
        print('Input size:', len(self.data))
        print('Output size:', len(deleted_data))
        return deleted_data
    
class SlidingWindows(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path, window_size):
        super().__init__(lang_source, lang_target, input_path)
        self.window_size = window_size
    
    def augment(self, data):
        data = self.data
        data = data.values
        window_data = []
        for a, b in data:
            words_a = a.split()
            words_b = b.split()
            if len(words_a) < self.window_size or len(words_b) < self.window_size:
                continue
            for i in range(len(words_a) - self.window_size + 1):
                if i + self.window_size > len(words_b):
                    break
                window_data.append([' '.join(words_a[i:i + self.window_size]), ' '.join(words_b[i:i + self.window_size])])
        window_data = pd.DataFrame(window_data, columns=[self.lang_source, self.lang_target])
        print('Input size:', len(self.data))
        print('Output size:', len(window_data))
        return window_data