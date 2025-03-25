import pandas as pd
import numpy as np
import random
import string
from itertools import permutations
import re 

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
    def __init__(self, input_file: str, theme_file: str, output_file: str):
        self.input_file = input_file
        self.theme_file = theme_file
        self.output_file = output_file

        # Load theme file and validate required columns
        self.df_theme = pd.read_excel(self.theme_file)
        required_columns = ['Vietnamese', 'Bahnaric', 'pos']
        for col in required_columns:
            if col not in self.df_theme.columns:
                raise KeyError(f"Column '{col}' not found in the theme file.")

        # Create mapping dictionary from Vietnamese to Bahnaric
        self.theme_mapping = self.df_theme.set_index('Vietnamese')['Bahnaric'].to_dict()

    def augment(self):
        # Load input CSV file
        df_input = pd.read_csv(self.input_file)

        # Validate input columns
        if 'Vietnamese' not in df_input.columns or 'Bahnaric' not in df_input.columns:
            raise KeyError("Columns 'Vietnamese' or 'Bahnaric' not found in the input file.")

        expanded_rows = []

        for _, row in df_input.iterrows():
            original_viet = str(row['Vietnamese'])
            original_bana = str(row['Bahnaric'])

            viet_words_list = original_viet.split(" ")
            bana_words_list = original_bana.split(" ")

            if len(bana_words_list) < len(viet_words_list):
                bana_words_list += [""] * (len(viet_words_list) - len(bana_words_list))

            for i, word_viet in enumerate(viet_words_list):
                if word_viet in self.theme_mapping:
                    replacement_bana = self.theme_mapping[word_viet]

                    new_viet_words = viet_words_list.copy()
                    new_bana_words = bana_words_list.copy()

                    new_viet_words[i] = word_viet  # Keep Vietnamese word unchanged
                    new_bana_words[i] = replacement_bana  # Replace Bahnaric word

                    new_viet_sentence = " ".join(new_viet_words)
                    new_bana_sentence = " ".join(new_bana_words)

                    expanded_rows.append({
                        'Vietnamese': new_viet_sentence,
                        'Bahnaric': new_bana_sentence
                    })

        expanded_df = pd.DataFrame(expanded_rows)
        result_df = pd.concat([df_input, expanded_df], ignore_index=True)
        result_df.to_csv(self.output_file, index=False)

class ReplaceWithSameSynomyms(augmentmethods):
    def __init__(self, input_file: str, theme_file: str, output_file: str):
        self.input_file = input_file
        self.theme_file = theme_file
        self.output_file = output_file

        # Load theme file and validate required columns
        self.df_theme = pd.read_excel(self.theme_file)
        required_columns = ['Vietnamese', 'Bahnaric', 'pos']
        for col in required_columns:
            if col not in self.df_theme.columns:
                raise KeyError(f"Column '{col}' not found in the theme file.")

        # Create mapping dictionary from Vietnamese to Bahnaric
        self.theme_mapping = self.df_theme.set_index('Vietnamese')['Bahnaric'].to_dict()

    def augment(self):
        # Load input CSV file
        df_input = pd.read_csv(self.input_file)

        # Validate input columns
        if 'Vietnamese' not in df_input.columns or 'Bahnaric' not in df_input.columns:
            raise KeyError("Columns 'Vietnamese' or 'Bahnaric' not found in the input file.")

        expanded_rows = []

        for _, row in df_input.iterrows():
            original_viet = str(row['Vietnamese'])
            original_bana = str(row['Bahnaric'])

            viet_words_list = original_viet.split(" ")
            bana_words_list = original_bana.split(" ")

            if len(bana_words_list) < len(viet_words_list):
                bana_words_list += [""] * (len(viet_words_list) - len(bana_words_list))

            for i, word_viet in enumerate(viet_words_list):
                if word_viet in self.theme_mapping:
                    replacement_bana = self.theme_mapping[word_viet]

                    new_viet_words = viet_words_list.copy()
                    new_bana_words = bana_words_list.copy()

                    new_viet_words[i] = word_viet  # Keep Vietnamese word unchanged
                    new_bana_words[i] = replacement_bana  # Replace Bahnaric word

                    new_viet_sentence = " ".join(new_viet_words)
                    new_bana_sentence = " ".join(new_bana_words)

                    expanded_rows.append({
                        'Vietnamese': new_viet_sentence,
                        'Bahnaric': new_bana_sentence
                    })

        expanded_df = pd.DataFrame(expanded_rows)
        result_df = pd.concat([df_input, expanded_df], ignore_index=True)
        result_df.to_csv(self.output_file, index=False)

    
class RandomInsertion(augmentmethods):
    def __init__(self, input_folder: str, theme_file: str, output_folder: str):
        self.input_folder = input_folder
        self.output_folder = output_folder

        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

        # Load theme file and filter words by 'time' and 'place' themes
        df_theme = pd.read_excel(theme_file)
        required_columns = ['Vietnamese', 'Bahnaric', 'theme']
        for col in required_columns:
            if col not in df_theme.columns:
                raise KeyError(f"Column '{col}' not found in theme file.")

        filtered = df_theme[df_theme['theme'].isin(['time', 'place'])]
        self.viet_words = filtered['Vietnamese'].dropna().tolist()
        self.bana_words = filtered['Bahnaric'].dropna().tolist()

    def augment(self):
        for file_name in os.listdir(self.input_folder):
            if file_name.endswith('.xlsx'):
                input_path = os.path.join(self.input_folder, file_name)
                print(f"Processing file: {file_name}")

                df = pd.read_excel(input_path)

                if 'Vietnamese' not in df.columns or 'Bahnaric' not in df.columns:
                    raise KeyError(f"Columns 'Vietnamese' or 'Bahnaric' missing in file {file_name}.")

                def insert_random_word(paragraph, word_list):
                    punctuation_pattern = r'([;,!?.])'
                    if not word_list:
                        return paragraph
                    word = random.choice(word_list)
                    return re.sub(punctuation_pattern, f' {word}\\1', str(paragraph))

                df['Vietnamese'] = df['Vietnamese'].apply(lambda x: insert_random_word(x, self.viet_words))
                df['Bahnaric'] = df['Bahnaric'].apply(lambda x: insert_random_word(x, self.bana_words))

                output_path = os.path.join(self.output_folder, file_name)
                df.to_csv(output_path, index=False)
    
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