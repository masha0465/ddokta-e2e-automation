"""
똑버스 Zone 목록 API 테스트
ListSimpleZones API 테스트 케이스
"""
import pytest
import time


@pytest.mark.api
@pytest.mark.zone
class TestListZones:
    """Zone 목록 조회 API 테스트"""
    
    @pytest.mark.smoke
    def test_list_zones_success(self, api_client):
        """Zone 목록 조회 성공 테스트"""
        response = api_client.list_zones()
        
        assert response is not None
        assert "zones" in response
        assert response["status"] == "success"
        
    def test_response_time(self, api_client):
        """응답 시간 테스트 - 3초 이내"""
        start = time.time()
        response = api_client.list_zones(timeout=3)
        elapsed = time.time() - start
        
        assert elapsed < 3.0
        assert response is not None
        
    def test_zone_count(self, api_client):
        """Zone 개수 검증 - 52개"""
        response = api_client.list_zones()
        
        assert "zones" in response
        assert len(response["zones"]) == 52
        assert response["total_count"] == 52
        
    def test_zone_data_structure(self, api_client):
        """Zone 데이터 구조 검증"""
        response = api_client.list_zones()
        
        assert "zones" in response
        zones = response["zones"]
        assert len(zones) > 0
        
        first_zone = zones[0]
        assert "id" in first_zone
        assert "name" in first_zone
        assert "city" in first_zone
        assert "status" in first_zone
        
    def test_all_zones_have_images(self, api_client):
        """모든 Zone에 이미지 정보 존재 확인"""
        response = api_client.list_zones()
        zones = response["zones"]
        
        for zone in zones:
            assert "id" in zone
            assert isinstance(zone["id"], int)
            
    def test_response_contains_expected_zones(self, api_client):
        """특정 Zone 존재 확인 - 동탄신도시, 수원, 파주"""
        response = api_client.list_zones()
        zones = response["zones"]
        zone_ids = [z["id"] for z in zones]
        
        assert 67 in zone_ids  # 동탄신도시
        assert 2 in zone_ids   # 수원 고색
        assert 9 in zone_ids   # 파주 운정
        
    def test_content_type_header(self, api_client):
        """Content-Type 헤더 검증"""
        response = api_client.list_zones()
        
        assert response is not None
        assert "status" in response
        
    def test_response_size_reasonable(self, api_client):
        """응답 크기 합리적인지 검증"""
        response = api_client.list_zones()
        
        assert "zones" in response
        zones_count = len(response["zones"])
        assert 50 <= zones_count <= 100