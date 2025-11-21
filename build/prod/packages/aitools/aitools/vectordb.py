from abc import ABC, abstractmethod
import json
import pandas as pd
# from langchain.vectorstores import Chroma
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.llms import OpenAI
# from langchain.chains import VectorDBQA
# from langchain.document_loaders import TextLoader, DirectoryLoader
# from chromadb.config import Settings
# from chromadb.utils import embedding_functions
# from langchain.document_loaders import PyPDFLoader


#from langchain_community.vectorstores import Chroma

import chromadb
from aitools.documents import TextDocument


# class VectorDB(ABC):
#     @abstractmethod
#     def add(self, id, document):
#         pass

#     @abstractmethod
#     def query(self, query_text, num_results=10):
#         pass


class ChromaVectorDB():
    def __init__(self, persist_dir=None) -> None:

        if persist_dir is None:
            self.chroma_client = chromadb.Client()
        else:
            self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        
        #self.collection_name = collection_name
            
    def get_collection(self, collection_name):
        return self.chroma_client.get_or_create_collection(name=collection_name)

#     def add(self, documents):
#         for document in documents:
#             text = document.page_content
#             metadata = document.metadata
#             print("Metadata: ", metadata)
#             id = metadata.get('id', None)
#             assert id is not None
#             print("Adding document ", id)
#             self.collection.add(documents=[text], metadatas=[metadata], ids=[id])

    def add_documents(self, collection, documents):
        documents_content = []
        documents_metadata = []
        documents_ids = []
        for document in documents:
            documents_content.append(document.get_content())
            documents_metadata.append(document.get_metadata())
            documents_ids.append(document.get_id())

        #self.add_chunk(collection, id, text, metadata)
        c = self.get_collection(collection)
        c.add(documents=documents_content, metadatas=documents_metadata, ids=documents_ids)
        #print("Added chunk ", id)
        return True
    
    def upsert_documents(self, collection, documents):
        c = self.get_collection(collection)
        for document in documents:
            text = document.page_content
            metadata = document.metadata
            id = document.uri
            c.upsert(documents=[text], metadatas=[metadata], ids=[id])
            print("Added document ", id)
    
    def query(self, collection_name, query_text, num_results=10):
        c = self.get_collection(collection_name)
        results = c.query(
            query_texts=[query_text],
            n_results=num_results,
            include=["distances"],
        )
        '''
        Example result...
        {
            "ids": [
                [
                    "id1",
                    "id2",
                    "id3"
                ]
            ],
            "distances": [
                [
                    1.7941185196221001,
                    1.8292055830621659,
                    1.8421470347695077
                ]
            ],
            "metadatas": null,
            "embeddings": null,
            "documents": null,
            "uris": null,
            "data": null
        }
        '''
        ids = results["ids"][0]
        distances = results["distances"][0]

        # Creating the dataframe
        df = pd.DataFrame({
            "id": ids,
            "distance": distances
        })
        df.set_index('id', inplace=True, drop=True)
        df.sort_values(by="distance", ascending=False, inplace=True)
        return df
    
    
    def get_documents(self, collection, ids):
        c = self.get_collection(collection)
        result = c.get(ids=ids)
        #print("Result: ", result)

        '''
        {'ids': ['id1', 'id3'], 'embeddings': None, 'metadatas': [{'source': 'my_source'}, {'source': 'my_source'}], 'documents': ['This is document 1', 'This is a document 3'], 'uris': None, 'data': None}
        '''

        ids = result['ids']
        contents = result['documents']
        metadata_list = [metadata['source'] for metadata in result['metadatas']]

        # Creating a list of TextDocument objects
        text_documents = [TextDocument(id, content, metadata) for id, content, metadata in zip(ids, contents, metadata_list)]
        return text_documents

    def count(self, collection):
        c = self.get_collection(collection)
        return c.count()
    
    def delete(self, collection):
        try:
            self.chroma_client.delete_collection(collection)
            return True
        except ValueError:
            False

if __name__ == "__main__":

    collection_name = 'test'
    vdb = ChromaVectorDB(collection_name, persist_dir="/app/data/chroma")

    vdb.add_chunk("id1", "This is document 1", {"source": "my_source"})
    vdb.add_chunk("id2", "This is a document 2", {"source": "my_source"})
    vdb.add_chunk("id3", "This is a document 3", {"source": "my_source"})

    query_text = 'document'
    results = vdb.query(query_text, num_results=10)
    print(json.dumps(results, indent=4))

