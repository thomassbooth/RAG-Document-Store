import pytest
from unittest.mock import Mock, patch
from io import BytesIO
from app.embeddings import DocumentEmbedder, DocumentProcessor
from langchain.schema import Document

@pytest.fixture
def mock_embedding_model():
    """Fixture to mock the OpenAIEmbeddings model."""
    mock_model = Mock()
    return mock_model

@pytest.fixture
def mock_storage_service():
    """Fixture to mock the VectorStore service."""
    return Mock()

@pytest.fixture
def mock_pdf_bytes():
    """Fixture to provide sample PDF content as bytes."""
    # Create mock PDF content
    return BytesIO(b'%PDF-1.4\n1 0 obj\n<< /Type /Page >>\nstream\nBT\n/F1 12 Tf\n(Hello World) Tj\nET\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF')

# Testing DocumentEmbedder
def test_document_embedder_initialization(monkeypatch, mock_embedding_model):
    """Test initialization of DocumentEmbedder."""
    # Mock the environment variable
    monkeypatch.setenv("OPENAI_API_KEY", "fake-api-key")

    with patch("document_processor.OpenAIEmbeddings", return_value=mock_embedding_model):
        embedder = DocumentEmbedder()
        assert embedder.get_embedding_model() == mock_embedding_model

def test_document_embedder_no_api_key(monkeypatch):
    """Test that DocumentEmbedder raises error if API key is not set."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable not set."):
        DocumentEmbedder()

def test_document_embedder_generate_embeddings(mock_embedding_model):
    """Test that generate_embeddings calls the embedding model correctly."""
    embedder = DocumentEmbedder()
    embedder._embedding_model = mock_embedding_model

    paragraphs = ["Paragraph 1", "Paragraph 2"]
    embedder.generate_embeddings(paragraphs)
    
    mock_embedding_model.embed_documents.assert_called_once_with(paragraphs)

# Testing DocumentProcessor
def test_document_processor_document_augmentation(mock_pdf_bytes, mock_embedding_model, mock_storage_service):
    """Test document augmentation by extracting text and storing embeddings."""
    mock_embedder = Mock()
    mock_embedder.get_embedding_model.return_value = mock_embedding_model
    
    processor = DocumentProcessor(mock_embedder, mock_storage_service)
    
    # Run the augmentation on the mock PDF
    processor.document_augmentation(mock_pdf_bytes.read(), "sample.pdf")
    
    # Ensure embeddings were generated for paragraphs
    mock_embedder.generate_embeddings.assert_called()
    
    # Ensure embeddings were stored
    mock_storage_service.store_embeddings.assert_called()

def test_document_processor_handles_empty_pdf(mock_storage_service):
    """Test document augmentation on an empty PDF with no content."""
    mock_embedder = Mock()
    processor = DocumentProcessor(mock_embedder, mock_storage_service)
    
    # Empty PDF bytes
    empty_pdf = BytesIO(b'')
    
    # No embeddings should be generated
    processor.document_augmentation(empty_pdf.read(), "empty.pdf")
    
    mock_embedder.generate_embeddings.assert_not_called()
    mock_storage_service.store_embeddings.assert_not_called()
