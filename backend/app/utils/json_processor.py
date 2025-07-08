def process_json_data(json_data, document_id, chunk_size=500):
    """
    Process JSON document into text chunks
    
    Args:
        json_data: Parsed JSON document
        document_id: ID of the document
        chunk_size: Maximum size of each chunk
    
    Returns:
        List of chunk dictionaries
    """
    chunks = []
    chunk_index = 0
    
    # Extract text based on your JSON structure
    if "pages" in json_data:
        for page in json_data["pages"]:
            content = page.get("content", "")
            
            # Simple chunking by size
            for i in range(0, len(content), chunk_size):
                chunk_text = content[i:i+chunk_size]
                if chunk_text.strip():  # Skip empty chunks
                    chunks.append({
                        "document_id": document_id,
                        "chunk_index": chunk_index,
                        "content": chunk_text
                    })
                    chunk_index += 1
    
    return chunks
