from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()

FILE_NAME = "토마토_스파게티_레시피.txt"

loader = TextLoader("data/" + FILE_NAME, encoding="utf-8")
doc = loader.load()

# print(doc)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


# print(splitter)

chunks = splitter.split_documents(doc)

# print(len(chunks))

# 3. metadata 추가
for chunk in chunks:
    chunk.metadata = {
        "source": FILE_NAME,
        "type": "recipe"
    }

# print(chunks)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# print(vector_store)
results= vector_store.similarity_search("된장", k=3)

for result in results:
    print("-------------------------------------------------------------------")
    print(result.page_content)

# 직접 임베딩
# result = embeddings.embed_documents([chunk.page_content for chunk in chunks])
# print(result)