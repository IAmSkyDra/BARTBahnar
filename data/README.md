# Data Folder

## 1. Introduction

This folder contains all datasets used in this study. The datasets are organized into four subfolders based on their purpose. Each dataset has been carefully collected and compiled over time. The data collection process took an entire year, during which we traveled to various provinces in Vietnam, such as Binh Dinh, Kom Tum, and Gia Lai, to gather these resources.

The datasets originate from various sources, including:

- **Field research**
- **Religious texts**
- **Broadcast transcripts**
- **Epic literature**

For the **field research** data, we enlisted 20 Bahnaric speakers to conduct surveys on their daily vocabulary and grammar usage. Additionally, we obtained **Bahnaric religious texts** from a local church. A regional **radio station** in the Bahnaric-speaking area provided us with daily broadcast transcripts. Moreover, we collected **epic literature** from village libraries, which serve as a cultural hub for Bahnaric children.

Since the raw data was originally in handwritten or paper format, we undertook the process of digitization. A total of 50 anonymous contributors assisted in this effort, resulting in a structured dataset with two columns: **"Bahnaric"** and **"Vietnamese"**. This dataset has been further divided for different research and development purposes.

---

## 2. Folder Structure

```plaintext
data
├── original
│   ├── train.csv
│   ├── test.csv
├── back_translation
│   ├── wikipedia_vi_ba.csv
├── dictionary
│   ├── bahnaric.csv
├── corpus
│   ├── corpus_bahnaric.txt
│   ├── vietnamese_words.csv
```

---

## 3. Description

- **original**: Contains the original dataset, which has been divided into two subsets: **training set (90%)** and **testing set (10%)**. This dataset serves as the foundation for all other processed datasets used in various tasks, including machine learning and linguistic analysis.

- **back_translation**: Includes datasets that have undergone **back translation** to enhance data diversity. This dataset is derived from Vietnamese sources, which were preprocessed and cleaned to ensure only Vietnamese content was included. The data was then translated from Vietnamese to Bahnaric using the **BartViBa** model. To improve accuracy, we employed anonymous linguists to manually review and verify each translation. This dataset is useful for improving model robustness and enriching the parallel corpus for translation tasks.

- **dictionary**: Contains dictionary data extracted from the original dataset. This is used for **lexical mapping (Solr)** and **data augmentation** in the project. The dictionary data provides a structured mapping between Bahnaric and Vietnamese words, facilitating tasks such as automatic translation, semantic search, and terminology alignment.

- **corpus**: Comprises **sentence-level** Bahnaric data and **word-level** Vietnamese data, which are crucial for the process of **loanword detection**. This dataset supports various linguistic analyses, including syntactic pattern recognition and phonetic similarity assessments. The corpus is essential for training and evaluating NLP models tailored for the Bahnaric language.

---

This dataset serves as a valuable resource for linguistic research and computational applications related to the Bahnaric language. 
