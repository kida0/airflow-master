
from airflow.sensors.base import BaseSensorOperator
from airflow.hooks.base import BaseHook

# 서울시 공공데이터 API 추출시 특정 날짜 컬럼을 조사하여, 배치 날짜 기준 전날 데이터가 존재하는지 체크

class SeoulApiDateSensor(BaseSensorOperator):
    template_fields = ("endpoint", )
    
    def __init__(self, dataset_nm, base_dt_col, day_dff=0, **kwargs):
        """
        Args:
            dataset_nm: 센싱할 데이터셋 명
            base_dt_col: 센싱 기준 컬럼(y.m.d or, y/m/d만 가능)
            day_off: 배치일 기준 생성여부를 확인하고자 하는 날짜 차이를 입력
        """
        super().__init__(**kwargs)
        self.http_conn_id = "openapi.seoul.go.kr"
        self.endpoint = "{{ var.value.apikey_openapi_seoul_go_kr }}/json/" + dataset_nm + "/1/100"
        self.base_dt_col = base_dt_col
        self.day_off = day_dff
    
    def poke(self, context):
        import requests
        import json
        from dateutil.relativedelta import relativedelta
        connection = BaseHook.get_connection(self.http_conn_id)
        url = f"http://{connection.host}:{connection.port}/{self.endpoint}"
        self.log.info(f"request url:{url}")
        response = requests.get(url)
        