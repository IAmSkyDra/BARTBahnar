# Bahnaric - Vietnamese Translator

Bahnaric-Vietnamese Translator is a sentence translation tool that follows a **Hybrid NMT Architecture**, integrating multiple **Natural Language Processing (NLP) techniques** to enhance translation accuracy and fluency.  
The system leverages **Loanword Detection, Word Segmentation, Lexical Mapping with Solr, and BART-based translation** to handle phrases that cannot be directly translated using a dictionary.

## Translation Flow

![Translation Flow](./pipeline.png)
📄 [View Translation Flow](./pipeline.pdf)

1. **Loanword Detection & Removal**

    - Uses **Underthesea** and a **Vietnamese dictionary** to detect and extract borrowed words from Vietnamese, including:
        - **Named Entities** (e.g., "Binh Minh", "Da Nang")
        - **Numerical Values** (e.g., "50", "2", "500")
        - **Punctuation** (e.g., "%", ",", ".", etc.)
    - Detected loanwords are then processed separately.

2. **Word Segmentation** Applies **PMI-based (Pointwise Mutual Information) word segmentation** to split the sentence into meaningful word units.

3. **Lexical Mapping with Solr** Uses the **Bahnaric-Vietnamese bilingual dictionary** powered by Solr to find possible translations.

4. **Fallback to BARTBahnar** If certain words or phrases are not found in the dictionary, the system applies **BARTBahnar**, a BART-based translation model, to process the remaining text.

5. **Post-Processing** Reconstructs the translated words into a well-formed Vietnamese sentence while maintaining grammatical correctness.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/IAmSkyDra/BARTBahnar.git
cd translate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Before running the script, ensure the required files are correctly set up in the configuration.

### **Modify Paths in `config.py`**

Update the following paths to match your directory structure if needed:

```python
DICTIONARY_PATH = "../data/dictionary/bahnaric.csv"
WORD_PATH = "../data/corpus/vietnamese_words.csv"
CORPUS = "../data/corpus/corpus_bahnaric.txt"
```

### **Explanation of Each File**

-   `DICTIONARY_PATH`: Path to the Bahnaric-Vietnamese dictionary, used for lexical mapping.
-   `WORD_PATH`: A dictionary of known Vietnamese words, used in loanword detection and classification.
-   `CORPUS`: A Bahnaric text corpus, used for word segmentation to improve translation accuracy.

---

## Usage

### Run the script:

```bash
python main.py --translator_model "your_custom_model" --classification_model "your_ner_model" --solr_url "http://your-solr-url"
```

Example:

```bash
python main.py --translator_model "IAmSkyDra/BARTBana_Translation" --classification_model "undertheseanlp/vietnamese-ner-v1.4.0a2" --best_candidate_model "NlpHUST/gpt2-vietnamese" --solr_url "http://localhost:8983/solr/mycore"
```

-   The **BARTBana translation model** can be retrieved from: **[BARTBana Model Download](#insert-bartbana-model-url-here)**
-   Refer to the [Apache Solr Setup Guide (Windows)](#apache-solr-setup-guide-windows) for instructions on setting up Solr and obtaining the solr_url.

If you want to use the default models, simply run:

```bash
python main.py
```

### Translate a sentence interactively:

Once the script starts, **you can enter sentences continuously**:

```plaintext
Enter a sentence to translate: Sô Noâng nghieâp oeêng pôjing cham pôlei ôêi tôdrong toâng hôêp, pôtho khan UBND tinh, ‘Boâ Noâng nghieâp oeêng pôjing cham pôlei adrol ‘naêr ‘baêl jiêt pôñaêm rim kheêi (kôdih kheêi minh jiêt ‘baêl göi ‘baêo kaêo adrol ‘naêr minh jiêt) oeêng pôtho khan ñoât xuaât jônang ôêi tôdrong waê.

Final Translated Sentence: Sở nông nghiệp và phát triển nông thôn; bãi làng có thể tổng hợp , tuyên truyền tinh , bộ nông nghiệp và ptnt trước ngày 25/5 các tháng ( tự tháng một gọt hai là báo cáo trước ngày 10/10 ) và báo cáo đột xuất khi có yêu cầu.

Enter a sentence to translate: exit
Exiting the program. See you next time!
```

---

## Notes

-   Use **Ctrl + C** to force stop the script anytime.
-   Ensure **Solr** is running.
-   It is **recommended to create a separate Solr core** for this script, as it **will delete all data in the specified core** before processing.

---

# Apache Solr Setup Guide (Windows)

## 1. Download & Install Solr

1. Download the latest Solr version from:  
   [https://solr.apache.org/downloads.html](https://solr.apache.org/downloads.html)

2. Extract the downloaded `.zip` file to a preferred location.

3. Open **Command Prompt (cmd)** and navigate to the Solr folder:
    ```sh
    cd path\to\solr-9.x.x\bin
    ```

## 2. Start Solr

Run the following command to start Solr in standalone mode:

```sh
solr start
```

By default, Solr runs on **port 8983**.

## 3. Access Solr Admin Panel

Once Solr is running, open your browser and go to:

```
http://localhost:8983/solr
```

This is the **Solr URL** where you can manage collections and query data.

## 4. Create a Core in Solr

Before indexing data, you need to create a core. Open **Command Prompt (cmd)** and run:

```sh
solr create -c mycore
```

-   Replace `mycore` with your desired core name.

After creation, you can see your core in the **Solr Admin Panel**: [http://localhost:8983/solr](http://localhost:8983/solr)

## 5. Get Core URL for API Use

Once the core is created, you can access it using:

```
http://localhost:8983/solr/mycore
```

Replace `mycore` with your actual core name.

**_This URL serves as the `solr_url` parameter in the script, allowing the program to interact with the Solr core for querying and indexing data._**

### Example: Query all data in the core

```
http://localhost:8983/solr/mycore/select?q=*
```

## 6. Stop Solr

To stop Solr, use:

```sh
solr stop
```

---

### References

-   **[Underthesea](https://github.com/undertheseanlp/underthesea)** – Vietnamese NLP toolkit for tokenization and loanword detection.

-   **[Solr](https://solr.apache.org/)** – A powerful search engine for fast dictionary-based lookups.

-   **[GPT-2 Vietnamese](https://huggingface.co/NlpHUST/gpt2-vietnamese)** – A language model for selecting the best translation candidate.
