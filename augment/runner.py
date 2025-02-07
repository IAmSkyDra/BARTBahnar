from augment import Combine, SwapSentences, ReplaceWithSameType, RandomInsertion, RandomDeletion, SlidingWindows

def main():
    # Instantiate each augmentation class
    combine = Combine()
    swap_sentences = SwapSentences()
    replace_with_same_type = ReplaceWithSameType()
    random_insertion = RandomInsertion()
    random_deletion = RandomDeletion()
    sliding_windows = SlidingWindows()

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
