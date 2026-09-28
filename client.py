"""Okapi BM25 Document Ranker & Search Engine
100% Python Standard Library (math, collections, re).
"""

import math
import collections
import re

class OkapiBM25Ranker:
    """Tunable Okapi BM25 relevance scorer."""
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = []
        self.doc_lens = []
        self.avg_doc_len = 0.0
        self.idf = {}
        self.tf_list = []

    def index(self, documents):
        self.docs = documents
        self.doc_lens = []
        self.tf_list = []
        df = collections.defaultdict(int)

        for doc in documents:
            tokens = re.findall(r"\b\w+\b", doc.lower())
            self.doc_lens.append(len(tokens))
            tf = collections.defaultdict(int)
            for t in tokens:
                tf[t] += 1
            self.tf_list.append(tf)
            for t in tf.keys():
                df[t] += 1

        self.avg_doc_len = sum(self.doc_lens) / max(1, len(documents))
        n_docs = len(documents)
        self.idf = {
            t: math.log((n_docs - count + 0.5) / (count + 0.5) + 1.0)
            for t, count in df.items()
        }

    def search(self, query, top_k=5):
        q_tokens = re.findall(r"\b\w+\b", query.lower())
        scores = []
        for idx, tf in enumerate(self.tf_list):
            doc_len = self.doc_lens[idx]
            score = 0.0
            for term in q_tokens:
                if term in tf:
                    t_idf = self.idf.get(term, 0.0)
                    t_freq = tf[term]
                    denom = t_freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                    score += t_idf * (t_freq * (self.k1 + 1.0)) / denom
            scores.append({"index": idx, "score": round(score, 4), "document": self.docs[idx]})

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]
