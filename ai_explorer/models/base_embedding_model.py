class BaseEmbeddingModel:
    """
    Base class for embedding models.

    This class should be inherited by any specific embedding model implementation.
    Subclasses should implement the `embed` method to generate embeddings for given text input.
    """
    def embed(self, text):
        """
        Generate embeddings for the given text.

        Args:
            text (str): The text to generate embeddings for.

        Returns:
            np.ndarray: The generated embedding vector.
        """
        raise NotImplementedError("This method should be overridden by subclasses")
