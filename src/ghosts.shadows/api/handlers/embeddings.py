from typing import List

import numpy as np
import torch
from transformers import BertModel, BertTokenizer


class BertEmbeddings:
    def __init__(self, model_name="bert-base-uncased", device=None):
        """
        Initializes the BertEmbeddings class with a specified model name and device.

        Args:
            model_name (str): The name of the pre-trained BERT model.
            device (str): The device to run the model on, either 'cpu' or 'mps' (for Mac).
        """
        self.device = device or ("mps" if torch.backends.mps.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name).to(self.device)

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Gets the BERT embedding for a single text.

        Args:
            text (str): The input text to get the embedding for.

        Returns:
            np.ndarray: The BERT embedding of the input text.
        """
        inputs = self.tokenizer(
            text, return_tensors="pt", max_length=512, truncation=True
        ).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

    def embed_documents(self, documents: List[str]) -> List[np.ndarray]:
        """
        Embeds a list of documents using BERT.

        Args:
            documents (List[str]): A list of documents to embed.

        Returns:
            List[np.ndarray]: A list of BERT embeddings for the documents.
        """
        embeddings = []
        for doc in documents:
            inputs = self.tokenizer(
                doc,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding="max_length",
            ).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings.append(outputs.last_hidden_state.mean(dim=1).cpu().numpy())
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """
        Embeds a query using BERT.

        Args:
            query (str): The query to embed.

        Returns:
            np.ndarray: The BERT embedding of the query.
        """
        inputs = self.tokenizer(
            query,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding="max_length",
        ).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

    def find_relevant_content(
        self,
        query_embedding: np.ndarray,
        document_embeddings: List[np.ndarray],
        documents: List[str],
        top_k: int = 3,
    ) -> str:
        """
        Finds the most relevant documents based on cosine similarity between query and document embeddings.

        Args:
            query_embedding (np.ndarray): The embedding of the query.
            document_embeddings (List[np.ndarray]): A list of embeddings for the documents.
            documents (List[str]): The list of documents corresponding to the embeddings.
            top_k (int): The number of top relevant documents to retrieve.

        Returns:
            str: The most relevant content combined from the top_k documents.
        """
        # Calculate cosine similarities between the query and document embeddings
        similarities = [
            np.dot(query_embedding, doc_emb)
            / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
            for doc_emb in document_embeddings
        ]
        # Get the indices of the top-k most similar documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return "\n".join([documents[i] for i in top_indices])
