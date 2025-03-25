import pandas as pd
import numpy as np
import random
import string
from itertools import permutations
import re
import os

# # Add path, language and config the code. After done configing, go to runner to run the code.

# LANG_SOURCE = 'Bahnaric'
# LANG_TARGET = 'Vietnamese'
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

class ReplaceWithSameThemes(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path, theme_file, output_path):
        super().__init__(lang_source, lang_target, input_path)
        self.theme_file = theme_file
        self.output_path = output_path

        # Load theme file and validate required columns
        self.df_theme = pd.read_excel(self.theme_file)
        required_columns = [self.lang_target, self.lang_source, 'pos']
        for col in required_columns:
            if col not in self.df_theme.columns:
                raise KeyError(f"Column '{col}' not found in the theme file.")

        # Create mapping dictionary from lang_target to lang_source
        self.theme_mapping = self.df_theme.set_index(self.lang_target)[self.lang_source].to_dict()

    def augment(self):
        # Load input CSV file
        df_input = pd.read_csv(self.input_path)

        # Validate input columns
        if self.lang_target not in df_input.columns or self.lang_source not in df_input.columns:
            raise KeyError(f"Columns '{self.lang_target}' or '{self.lang_source}' not found in the input file.")

        expanded_rows = []

        for _, row in df_input.iterrows():
            original_target = str(row[self.lang_target])
            original_source = str(row[self.lang_source])

            target_words_list = original_target.split(" ")
            source_words_list = original_source.split(" ")

            if len(source_words_list) < len(target_words_list):
                source_words_list += [""] * (len(target_words_list) - len(source_words_list))

            for i, word_target in enumerate(target_words_list):
                if word_target in self.theme_mapping:
                    replacement_source = self.theme_mapping[word_target]

                    new_target_words = target_words_list.copy()
                    new_source_words = source_words_list.copy()

                    new_target_words[i] = word_target  # Keep target word unchanged
                    new_source_words[i] = replacement_source  # Replace source word

                    new_target_sentence = " ".join(new_target_words)
                    new_source_sentence = " ".join(new_source_words)

                    expanded_rows.append({
                        self.lang_target: new_target_sentence,
                        self.lang_source: new_source_sentence
                    })

        expanded_df = pd.DataFrame(expanded_rows)
        result_df = pd.concat([df_input, expanded_df], ignore_index=True)
        print('Input size:', len(df_input))
        print('Output size:', len(result_df))
        return result_df

class ReplaceWithSameSynomyms(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path, theme_file, output_path):
        super().__init__(lang_source, lang_target, input_path)
        self.theme_file = theme_file
        self.output_path = output_path

        # Load theme file and validate required columns
        self.df_theme = pd.read_excel(self.theme_file)
        required_columns = [self.lang_target, self.lang_source, 'pos']
        for col in required_columns:
            if col not in self.df_theme.columns:
                raise KeyError(f"Column '{col}' not found in the theme file.")

        # Create mapping dictionary from lang_target to lang_source
        self.theme_mapping = self.df_theme.set_index(self.lang_target)[self.lang_source].to_dict()

    def augment(self):
        # Load input CSV file
        df_input = pd.read_csv(self.input_path)

        # Validate input columns
        if self.lang_target not in df_input.columns or self.lang_source not in df_input.columns:
            raise KeyError(f"Columns '{self.lang_target}' or '{self.lang_source}' not found in the input file.")

        expanded_rows = []

        for _, row in df_input.iterrows():
            original_target = str(row[self.lang_target])
            original_source = str(row[self.lang_source])

            target_words_list = original_target.split(" ")
            source_words_list = original_source.split(" ")

            if len(source_words_list) < len(target_words_list):
                source_words_list += [""] * (len(target_words_list) - len(source_words_list))

            for i, word_target in enumerate(target_words_list):
                if word_target in self.theme_mapping:
                    replacement_source = self.theme_mapping[word_target]

                    new_target_words = target_words_list.copy()
                    new_source_words = source_words_list.copy()

                    new_target_words[i] = word_target  # Keep target word unchanged
                    new_source_words[i] = replacement_source  # Replace source word

                    new_target_sentence = " ".join(new_target_words)
                    new_source_sentence = " ".join(new_source_words)

                    expanded_rows.append({
                        self.lang_target: new_target_sentence,
                        self.lang_source: new_source_sentence
                    })

        expanded_df = pd.DataFrame(expanded_rows)
        result_df = pd.concat([df_input, expanded_df], ignore_index=True)
        print('Input size:', len(df_input))
        print('Output size:', len(result_df))
        return result_df

class RandomInsertion(augmentmethods):
    def __init__(self, lang_source, lang_target, input_path: str, theme_file: str):
        super().__init__(lang_source, lang_target, input_path)

        # Load theme file and filter words by 'time' and 'place' themes
        df_theme = pd.read_excel(theme_file)
        required_columns = [self.lang_target, self.lang_source, 'pos']
        for col in required_columns:
            if col not in df_theme.columns:
                raise KeyError(f"Column '{col}' not found in theme file.")

        filtered = df_theme[df_theme['theme'].isin(['time', 'place'])]
        self.target_words = filtered[self.lang_target].dropna().tolist()
        self.source_words = filtered[self.lang_source].dropna().tolist()

    def augment(self):
        # Load input CSV file
        df = pd.read_csv(self.input_path)

        # Validate input columns
        if self.lang_target not in df.columns or self.lang_source not in df.columns:
            raise KeyError(f"Columns '{self.lang_target}' or '{self.lang_source}' not found in the input file.")

        def insert_random_word(paragraph, word_list):
            punctuation_pattern = r'([;,!?.])'
            if not word_list:
                return paragraph
            word = random.choice(word_list)
            return re.sub(punctuation_pattern, f' {word}\\1', str(paragraph))

        # Apply random insertion
        df[self.lang_target] = df[self.lang_target].apply(lambda x: insert_random_word(x, self.target_words))
        df[self.lang_source] = df[self.lang_source].apply(lambda x: insert_random_word(x, self.source_words))

        print('Input size:', len(self.data))
        print('Output size:', len(df))
        return df
    
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