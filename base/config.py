import configparser
import os
import ast

class Config:
    def __init__(self, config_file=None):
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

        self.PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

        self.LOG_DIR = os.path.join(self.PROJECT_ROOT, 'logs')
        self.DATA_DIR = os.path.join(self.PROJECT_ROOT, 'rag_qa/data')
        self.MODELS_DIR = os.path.join(self.PROJECT_ROOT, 'rag_qa/models')
        self.EDU_DOCUMENT_LOADERS_DIR = os.path.join(self.PROJECT_ROOT, 'rag_qa/edu_document_loaders')

        if config_file is None:
            config_file = os.path.join(self.PROJECT_ROOT, 'config.ini')

        self.config.read(config_file, encoding='utf-8')

        # MySQL
        self.MYSQL_HOST = os.getenv('MYSQL_HOST', self.config.get(section='mysql', option='host', fallback='127.0.0.1'))
        self.MYSQL_PORT = int(os.getenv('MYSQL_PORT', self.config.get('mysql', 'port', fallback=3306)))
        self.MYSQL_USER = os.getenv('MYSQL_USER', self.config.get('mysql', 'user', fallback='edu_rag'))
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', self.config.get('mysql', 'password', fallback='040710'))
        self.MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', self.config.get('mysql', 'database', fallback='subjects_kg'))
        self.MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', self.config.get('mysql', 'charset', fallback='utf8'))

        # Redis
        self.REDIS_HOST = os.getenv('REDIS_HOST', self.config.get('redis', 'host', fallback='127.0.0.1'))
        self.REDIS_PORT = int(os.getenv('REDIS_PORT', self.config.get('redis', 'port', fallback=6379)))
        self.REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', self.config.get('redis', 'password', fallback='1234'))
        self.REDIS_DB = int(os.getenv('REDIS_DB', self.config.get('redis', 'db', fallback=0)))

        # Milvus
        self.MILVUS_HOST = os.getenv('MILVUS_HOST', self.config.get('milvus', 'host', fallback='127.0.0.1'))
        self.MILVUS_PORT = os.getenv('MILVUS_PORT', self.config.get('milvus', 'port', fallback='19530'))
        self.MILVUS_DATABASE_NAME = os.getenv('MILVUS_DATABASE_NAME',self.config.get('milvus', 'database_name', fallback='itcast'))
        self.MILVUS_COLLECTION_NAME = os.getenv('MILVUS_COLLECTION_NAME',self.config.get('milvus', 'collection_name', fallback='edurag'))

        # LLM
        self.LLM_MODEL = self.config.get('llm', 'model', fallback='qwen-plus')
        self.DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', self.config.get('llm', 'dashscope_api_key'))
        self.DASHSCOPE_BASE_URL = self.config.get('llm', 'dashscope_base_url',fallback='https://dashscope.aliyuncs.com/compatible-mode/v1')

        # 检索参数
        self.PARENT_CHUNK_SIZE = self.config.getint('retrieval', 'parent_chunk_size', fallback=1200)
        self.CHILD_CHUNK_SIZE = self.config.getint('retrieval', 'child_chunk_size', fallback=300)
        self.CHUNK_OVERLAP = self.config.getint('retrieval', 'chunk_overlap', fallback=50)
        self.RETRIEVAL_K = self.config.getint('retrieval', 'retrieval_k', fallback=10)
        self.CANDIDATE_M = self.config.getint('retrieval', 'candidate_m', fallback=2)
        # BM25的双重检索阈值
        raw = self.config.get('retrieval', 'bm25_threshold', fallback=(0.85, 10.0))
        try:
            parsed = ast.literal_eval(raw)
            self.BM25_THRESHOLD = (float(parsed[0]), float(parsed[1]))
        except Exception:
            self.BM25_THRESHOLD = (0.85, 10.0)
        self.RERANK_SCORE_THRESHOLD = self.config.getfloat('retrieval', 'rerank_score_threshold', fallback=0.5)

        # 应用配置
        self.VALID_SOURCES = ast.literal_eval(
            self.config.get('app', 'valid_sources', fallback='["ai", "java", "test", "ops", "bigdata"]'))
        # 客服电话
        self.CUSTOMER_SERVICE_PHONE = self.config.get('app', 'customer_service_phone', fallback='10086')

        self.KB_ADMIN_USERNAME = os.getenv('KB_ADMIN_USERNAME',self.config.get('app', 'kb_admin_username', fallback='melo'))
        self.KB_ADMIN_PASSWORD = os.getenv('KB_ADMIN_PASSWORD',self.config.get('app', 'kb_admin_password', fallback='123456'))
        self.KB_TOKEN_EXPIRE_MINUTES = self.config.getint('app', 'kb_token_expire_minutes', fallback=120)

        # 日志文件路径
        self.LOG_FILE = os.path.join(self.LOG_DIR, 'app.log')

config = Config()

if __name__ == '__main__':
    print(config.PROJECT_ROOT)
    print(config.MYSQL_USER)
    print(config.LOG_FILE)
    print(config.BM25_THRESHOLD)
    print(type(config.BM25_THRESHOLD))
    print(config.VALID_SOURCES)