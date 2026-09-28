from client import OkapiBM25Ranker

def main():
    ranker = OkapiBM25Ranker()
    corpus = [
        "Python agent planning and tool calling frameworks",
        "Deep learning and transformer language models",
        "Quantum computing state vectors and unitary transformations"
    ]
    ranker.index(corpus)
    hits = ranker.search("Python agent frameworks")
    print("Okapi BM25 Ranker Verification:")
    for h in hits:
        print(f"  Score: {h['score']} -> {h['document']}")

if __name__ == "__main__":
    main()
