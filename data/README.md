# 📂 Data Folder

This folder contains all datasets used in this paper. The datasets are organized into three subfolders based on their purpose.

## 📂 Folder Structure

```plaintext
data/
├── original/
│   ├── ba_vi_train.csv
│   ├── ba_vi_test.csv
├── back_translation/
│   ├── ba_vi_back_translation.csv
├── dictionary/
│   ├── ba_vi_dictionary.csv
```

## 📄 Description of Subfolders

- **original/**: Contains the original datasets used for the project, and then divides into 2 sets named training set and testing set.
- **back_translation/**: Contains datasets that have been processed through back translation to enrich the dataset.
- **dictionary/**: Contains dictionary data used for lexical mapping (Solr)  and data augmentation in the project.

