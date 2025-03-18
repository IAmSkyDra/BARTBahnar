from augment import Combine, SwapSentences, ReplaceWithSameType, RandomInsertion, RandomDeletion, SlidingWindows

def main():
    # Configuration values
    lang_source = 'tiếng bana'
    lang_target = 'tiếng việt'
    input_path = 'augment/test.csv'
    dictionary_path = 'augment/dictionary.csv'
    batch_size = 10
    limit_new_sentences = 10
    num_insertions = 1
    max_lines_generated = 10
    num_deletions = 1
    window_size = 2

    # Instantiate each augmentation class with configurations
    combine = Combine(lang_source, lang_target, input_path, batch_size=batch_size)
    swap_sentences = SwapSentences(lang_source, lang_target, input_path)
    replace_with_same_type = ReplaceWithSameType(lang_source, lang_target, input_path, dictionary_path, limit_new_sentences=limit_new_sentences)
    random_insertion = RandomInsertion(lang_source, lang_target, input_path, dictionary_path, num_insertions=num_insertions, max_lines_generated=max_lines_generated)
    random_deletion = RandomDeletion(lang_source, lang_target, input_path, num_deletions=num_deletions)
    sliding_windows = SlidingWindows(lang_source, lang_target, input_path, window_size=window_size)

    # Test each augmentation method
    print("Testing Combine...")
    combined_data = combine.augment(None)
    combine.dataToCSV(combined_data, 'output/combined.csv')

    print("Testing SwapSentences...")
    swapped_data = swap_sentences.augment(None)
    swap_sentences.dataToCSV(swapped_data, 'output/swapped_sentences.csv')

    print("Testing ReplaceWithSameType...")
    replaced_data = replace_with_same_type.augment(None)
    replace_with_same_type.dataToCSV(replaced_data, 'output/replaced_with_same_type.csv')

    print("Testing RandomInsertion...")
    inserted_data = random_insertion.augment(None)
    random_insertion.dataToCSV(inserted_data, 'output/random_insertion.csv')

    print("Testing RandomDeletion...")
    deleted_data = random_deletion.augment(None)
    random_deletion.dataToCSV(deleted_data, 'output/random_deletion.csv')

    print("Testing SlidingWindows...")
    window_data = sliding_windows.augment(None)
    sliding_windows.dataToCSV(window_data, 'output/sliding_windows.csv')

if __name__ == '__main__':
    main()
