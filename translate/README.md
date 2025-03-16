# Bana Translator  

Bana Translator is a sentence translation tool that follows a structured **flow-based approach** using **custom NLP models**. It leverages **NER (Named Entity Recognition), Solr-based dictionary lookup, GPT-2 for best candidate selection, and BART-based translation** to improve translation accuracy and fluency.  

## Translation Flow  
1. **Vietnamese Word Identification**: The system first detects and extracts Vietnamese words from the input sentence.  
2. **Foreign Word Separation**: Any remaining words that are not identified as Vietnamese are separated.  
3. **Dictionary Lookup with Solr**: The system queries Solr to find possible translations for recognized words in its dictionary.  
4. **Best Candidate Selection with GPT-2**: If multiple translations exist, the **GPT-2 model** selects the most contextually appropriate word.  
5. **Word Recombination**: The translated words are combined to form a structured sentence.  
6. **Fallback to BARTBana**: If certain words or phrases cannot be translated via Solr, the system uses **BARTBana**, a BART-based translation model, to translate the remaining text.  

## Features  
- **Flow-based processing** ensures structured and accurate translations.  
- **GPT-2-based best candidate selection** enhances translation precision.  
- **Solr integration** enables dictionary-based translations.  
- **Pretrained AI models** improve Vietnamese text processing and translation quality.  
- **Continuous translation** allows multiple sentences to be translated in one session.  
- **Data cleaning and preprocessing** optimize input text before translation.  
---

## Installation  

### 1. Clone the Repository  
```bash
git clone https://github.com/your-repo/bana-translator.git
cd bana-translator
```

### 2. Install Dependencies  
```bash
pip install -r requirements.txt
```
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
- Use **Ctrl + C** to force stop the script anytime.   
- Ensure **Solr** is running.  
- It is **recommended to create a separate Solr core** for this script, as it **will delete all data in the specified core** before processing.

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
solr create -c my_core
```
- Replace `my_core` with your desired core name.

After creation, you can see your core in the **Solr Admin Panel**:  [http://localhost:8983/solr](http://localhost:8983/solr)

## 5. Get Core URL for API Use  
Once the core is created, you can access it using:
```
http://localhost:8983/solr/my_core
```
Replace `my_core` with your actual core name.

**_This URL serves as the `solr_url` parameter in the script, allowing the program to interact with the Solr core for querying and indexing data._**

### Example: Query all data in the core  
```
http://localhost:8983/solr/my_core/select?q=*
```

## 6. Stop Solr  
To stop Solr, use:
```sh
solr stop
```

---

## Contributors