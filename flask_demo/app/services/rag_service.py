from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

# 初始化
# llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
embeddings = OpenAIEmbeddings()

# 处理PDF文件->向量存储
def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # 每个文本块的字符数
        chunk_overlap=200,     # 相邻文本块的重叠字符数
        length_function=len    # 计算长度的函数
    )
    texts = text_splitter.split_documents(documents)
    
    # 创建向量存储
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=os.path.join('uploads', 'chroma_db')
    )
    vectordb.persist()
    
    return vectordb

