
import psycopg2
import pandas as pd
from airflow.hooks.base import BaseHook

class CustomPostgresHook(BaseHook):
    def __init__(self, postgres_conn_id, **kwargs):
        self.postgres_conn_id = postgres_conn_id
        
    def get_conn(self):
        """ BaseHook을 상속하여 사용하기 위해 오버라이드 필요 """
        conn = BaseHook.get_connection(self.postgres_conn_id)
        self.host = conn.host
        self.user = conn.login
        self.password = conn.password
        self.schema = conn.schema
        self.port = conn.port
        self.postgres_conn = psycopg2.connect(
            host=self.host, user=self.user, password=self.password, dbname=self.schema, port=self.port)
        return self.postgres_conn
    
    def bulk_load(self, table, file_name, delimiter: str, is_header: bool, is_replace: bool):
        """
        자체적으로 정의한 메서드로, 주어진 파일을 postgres 테이블에 update
            Args:
                table: 파일을 적재할 테이블 이름
                file_ame: 적재한 파일 이름
                delimiter: 파일의 컬럼 구분자
                is_header: Header를 사용할지 유무
                is_replace: 기존에 이미 table이 존재하는 경우에 새로 쓸 것인지, append 할 건지
        """
        from sqlalchemy import create_engine
        
        self.log.info(f"{table}에 {file_name}을 적재합니다")
        self.get_conn()
        
        header = 0 if is_header else None
        if_exists = "replace" if is_replace else "append"
        file_df = pd.read_csv(file_name, header=header, delimiter=delimiter)
        self.log.info(f"헤더는 {header}이고 파일은 {if_exists}")
        
        for col in file_df.columns:
            # 숫자, 날짜 등의 컬럼을 위해 try/except 구문 사용
            try:
                file_df[col] = file_df[col].str.replace("\r\n", "")
                self.log.info(f"{table}.{col}: 개행 문자 제거")
                # replace("\r\n", ""): CR, LF 제거
            except:
                continue
            
        self.log.info("적재 데이터의 크기: " + str(len(file_df)))
        self.log.info("적재 데이터의 컬럼 수: " + str(len(file_df.columns)))
        
        uri = f"postgresql://{self.user}:{self.password}@{self.host}/{self.schema}"
        engine = create_engine(uri)
        file_df.to_sql(name=table,
                            con=engine,
                            schema='public',
                            if_exists=if_exists,
                            index=False
                        )
        
        
        
        