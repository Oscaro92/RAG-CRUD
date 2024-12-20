# * import libraries
import os
from decouple import config
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader


class AgentCRUD():
    def __init__(self):
        temperature = 0.0
        model = "gpt-4o-mini"
        os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.access = {
            'admin': False,
            'accountant': False,
            'sales': False
        }


    def loadDoc(self, path: str, access: list)->list:
        '''
        Load the documents

        :param path: path of the document (PDF format)
        :param access: access of the document
        :return: list of PDF file (Document)
        '''

        loader = PyPDFLoader(path)
        pages = loader.load_and_split()

        # update access
        self.addAccess(access)

        for page in pages:
            page.page_content = page.page_content.replace('\n', ' ')
            # add access in metadata of Document
            for key, value in self.access.items():
                page.metadata[key] = value

        return pages


    def addAccess(self, access:list):
        """
        Change access

        :param access: list of access
        :return: void
        """

        for key in access:
            if key in self.access:
                self.access[key] = True


    def calculateChunkIds(self, chunks):
        '''
        calculate chunk ids

        :param chunks: list of chunks
        :return: list of chunk with ids
        '''

        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks


    def saveDoc(self, chunks: list):
        # Load the existing database.
        db = Chroma(persist_directory="chroma", embedding_function=self.embeddings)

        # Calculate Page IDs.
        chunks_with_ids = self.calculateChunkIds(chunks)

        # Add or Update the documents.
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            db.persist()
        else:
            print("✅ No new documents to add")


    def similarityFilter(self, query:str, access:str)->list:
        '''
        Return docs with scoring

        :param query: query to evaluate
        :param access: access to filter
        :return: list of document
        '''
        db = Chroma(persist_directory="chroma", embedding_function=self.embeddings)
        results = db.similarity_search_with_relevance_scores(query, filter={access: {"$eq": True}})

        return results


    def chat(self, docs: list, messages: list)->str:
        '''
        get response of LLM

        :param docs: list of docs similar
        :param messages: list of message in chat
        :return: LLM response
        '''

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Tu es un assistant d'analyse de document. A partir des données des documents fournis tu dois répondre aux questions posés.\n"
                    "Les documents fournis : {docs} \n"
                    "Si il y a aucun document fournis répond : Désolé je n'ai rien trouvé à propos de ce sujet..."
                )
            ]
        )

        for message in messages:
            prompt.append((message['role'], message['content']))

        chain = prompt | self.llm
        response = chain.invoke(
            {
                "docs": docs
            }
        )

        return response.content
