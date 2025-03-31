from augment import Combine, SwapSentences, ReplaceWithSameThemes, ReplaceWithSameSynomyms, RandomInsertion, RandomDeletion, SlidingWindows

def main():
    # Configuration values
    lang_source = 'Bahnaric'
    lang_target = 'Vietnamese'
    input_path = 'augment/test.csv'
    theme_path = 'augment/dictionary.csv'
    batch_size = 10
    limit_new_sentences = 10
    num_insertions = 1
    max_lines_generated = 10
    num_deletions = 1
    window_size = 2
    METHOD_NUMS = 1

    # Instantiate each augmentation class with configurations
    combine = Combine(lang_source, lang_target, input_path, batch_size=batch_size)
    swap_sentences = SwapSentences(lang_source, lang_target, input_path)
    replace_with_same_themes = ReplaceWithSameThemes(lang_source, lang_target, input_path, theme_path, 'output/replaced_with_same_themes.csv')
    replace_with_same_synonyms = ReplaceWithSameSynomyms(lang_source, lang_target, input_path, theme_path, 'output/replaced_with_same_synonyms.csv')
    random_insertion = RandomInsertion(lang_source, lang_target, input_path, theme_path)
    random_deletion = RandomDeletion(lang_source, lang_target, input_path, num_deletions=num_deletions)
    sliding_windows = SlidingWindows(lang_source, lang_target, input_path, window_size=window_size)

    # Test selected augmentation method
    if METHOD_NUMS == 1:
        print("Testing Combine...")
        combined_data = combine.augment(None)
        combine.dataToCSV(combined_data, 'output/combined.csv')
    elif METHOD_NUMS == 2:
        print("Testing SwapSentences...")
        swapped_data = swap_sentences.augment(None)
        swap_sentences.dataToCSV(swapped_data, 'output/swapped_sentences.csv')
    elif METHOD_NUMS == 3:
        print("Testing ReplaceWithSameThemes...")
        replaced_data = replace_with_same_themes.augment()
        replace_with_same_themes.dataToCSV(replaced_data, 'output/replaced_with_same_themes.csv')
    elif METHOD_NUMS == 4:
        print("Testing ReplaceWithSameSynomyms...")
        replaced_data = replace_with_same_synonyms.augment()
        replace_with_same_synonyms.dataToCSV(replaced_data, 'output/replaced_with_same_synonyms.csv')
    elif METHOD_NUMS == 5:
        print("Testing RandomInsertion...")
        inserted_data = random_insertion.augment()
        random_insertion.dataToCSV(inserted_data, 'output/random_insertion.csv')
    elif METHOD_NUMS == 6:
        print("Testing RandomDeletion...")
        deleted_data = random_deletion.augment(None)
        random_deletion.dataToCSV(deleted_data, 'output/random_deletion.csv')
    elif METHOD_NUMS == 7:
        print("Testing SlidingWindows...")
        window_data = sliding_windows.augment(None)
        sliding_windows.dataToCSV(window_data, 'output/sliding_windows.csv')
    else:
        print("Invalid METHOD_NUMS value. Please select a valid method.")

if __name__ == '__main__':
    main()
