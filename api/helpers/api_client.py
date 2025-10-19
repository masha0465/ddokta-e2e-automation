"""
똑타 Zone API 클라이언트 (초간단 버전 - 1일 완성용)
"""
import requests
import re


class DdoktaAPIClient:
    """똑타 Zone API 클라이언트"""
    
    def __init__(self):
        self.base_url = "https://api.shucle.com"
        self.headers = {
            "Content-Type": "application/grpc-web+proto",
            "app-name": "com.hyundai.shucle.gmaas",
            "app-version": "4.7.6",
            "accept-language": "ko",
        }
    
    def list_zones(self):
        """구역 목록 조회"""
        url = f"{self.base_url}/opgwv1.OpGw/ListSimpleZones"
        response = requests.post(url, headers=self.headers, data=b'', timeout=10)
        return response
    
    def parse_zones(self, response):
        """응답 파싱 (간단 버전)"""
        text = response.text
        zones = []
        
        # 정규식으로 Zone 추출
        pattern = r'(\d+)([가-힣\s·‧]+)\]https://(.*?\.png)'
        for match in re.finditer(pattern, text):
            zone_id, name, img_path = match.groups()
            zones.append({
                'zone_id': int(zone_id),
                'name': name.strip(),
                'image_url': f'https://{img_path}'
            })
        
        return zones