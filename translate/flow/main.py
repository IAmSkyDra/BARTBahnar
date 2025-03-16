import argparse
from translate_process import translate

def main():
    parser = argparse.ArgumentParser(description="Translate a given sentence using custom NLP models.")

    # Input
    parser.add_argument("--src", type=str, help="Input sentence to be processed")

    # Endpoint
    parser.add_argument("--translator_model", type=str, default="IAmSkyDra/BARTBana_Translation", 
                        help="Translation model (default: BARTBana Translation)")
    parser.add_argument("--segment_model", type=str, default="undertheseanlp/vietnamese-ner-v1.4.0a2", 
                        help="Word segmentation model (default: Underthesea NER v1.4.0a2)")
    parser.add_argument("--best_candidate_model", type=str, default="NlpHUST/gpt2-vietnamese", 
                        help="Best candidate selection model (default: GPT-2 Vietnamese by NlpHUST)")
    parser.add_argument("--solr_url", type=str, default="http://localhost:8983/solr/mycore", 
                        help="Solr base URL (default: http://localhost:8983/solr/mycore)")

    args = parser.parse_args()

    # Gọi hàm translate với thông tin models và Solr
    result = translate(args.sentence, args.solr_url)

    # Hiển thị kết quả
    print("\n🔹 Final Translated Sentence:", result)

    # Hiển thị thông tin các model được sử dụng
    print("\n📌 Model Configuration:")
    print(f"   🏆 Translator Model: {args.translator_model}")
    print(f"   ✂️  Segmentation Model: {args.segment_model}")
    print(f"   🎯 Best Candidate Model: {args.best_candidate_model}")
    print(f"   🔗 Solr URL: {args.solr_url}")

if __name__ == "__main__":
    main()
