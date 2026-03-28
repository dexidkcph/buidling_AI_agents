import numpy as np


class SearchTool:
    def __init__(self, binance_docs, text_index, embedding_model, vector_embeddings):
        self.binance_docs = binance_docs
        self.text_index = text_index
        self.embedding_model = embedding_model
        self.vector_embeddings = vector_embeddings

    def text_search(self, query: str, num_results: int = 5):
        """
        Exact keyword-based search.
        """
        return self.text_index.search(query, num_results=num_results)

    def vector_search(self, query: str, num_results: int = 5):
        """
        Semantic similarity search using cosine similarity.
        """
        query_embedding = self.embedding_model.encode([query])[0]
        query_embedding = np.array(query_embedding)

        doc_norms = np.linalg.norm(self.vector_embeddings, axis=1)
        query_norm = np.linalg.norm(query_embedding)

        similarities = np.dot(self.vector_embeddings, query_embedding) / (
            doc_norms * query_norm + 1e-10
        )

        top_indices = np.argsort(similarities)[::-1][:num_results]
        return [self.binance_docs[i] for i in top_indices]

    def hybrid_search(self, query: str, num_results: int = 5):
        """
        Combine text and vector results, then deduplicate.
        """
        text_results = self.text_search(query, num_results=num_results)
        vector_results = self.vector_search(query, num_results=num_results)

        seen_ids = set()
        combined = []

        for result in text_results + vector_results:
            result_id = result.get("id")
            if result_id not in seen_ids:
                seen_ids.add(result_id)
                combined.append(result)

        return combined[:num_results]

    def format_results(self, results):
        """
        Convert raw search results into clean text for the agent.
        """
        if not results:
            return "No relevant documentation found."

        output = []

        for i, r in enumerate(results, start=1):
            title = r.get("title", "")
            section = r.get("section", "")
            filename = r.get("filename", "")
            text = r.get("chunk", "")

            formatted = (
                f"Result {i}\n"
                f"Title: {title}\n"
                f"Section: {section}\n"
                f"Filename: {filename}\n"
                f"Content: {text}\n"
            )
            output.append(formatted)

        return "\n---\n".join(output)

    def search_docs(self, query: str) -> str:
        """
        Main tool method the agent will call.
        """
        results = self.hybrid_search(query, num_results=5)
        return self.format_results(results)