"""
똑버스 Zone Operation API 테스트
GetZoneOperationInfo API 테스트 케이스
"""
import pytest
import time


@pytest.mark.api
@pytest.mark.zone
class TestZoneOperations:
    """Zone 운영 정보 API 테스트"""
    
    def test_get_zone_operation_success(self, api_client):
        """Zone 운영 정보 조회 성공 테스트"""
        # Given: 유효한 zone_id
        zone_id = 67  # 동탄신도시
        
        # When: Zone 운영 정보 조회
        response = api_client.get_zone_operation_info(zone_id)
        
        # Then: 응답 성공
        assert response is not None, "응답이 None입니다"
        assert "zone_id" in response or "zoneId" in response, "zone_id가 응답에 없습니다"
        
    def test_get_zone_operation_with_various_zones(self, api_client):
        """여러 Zone의 운영 정보 조회 테스트"""
        # Given: 다양한 지역의 zone_id들
        zone_ids = [
            2,   # 수원시 - 고색‧오목천‧평리
            67,  # 화성시 - 동탄신도시
            9,   # 파주시 - 운정‧교하지구
            20,  # 하남시 - 위례동
            18   # 평택시 - 고덕국제신도시
        ]
        
        results = []
        for zone_id in zone_ids:
            # When: 각 Zone 운영 정보 조회
            response = api_client.get_zone_operation_info(zone_id)
            results.append(response)
        
        # Then: 모든 Zone의 정보가 정상 조회됨
        assert len(results) == len(zone_ids), "일부 Zone 조회 실패"
        assert all(r is not None for r in results), "None 응답이 존재합니다"
        
    def test_zone_operation_response_structure(self, api_client):
        """Zone 운영 정보 응답 구조 검증"""
        # Given: 특정 zone_id
        zone_id = 67  # 동탄신도시
        
        # When: Zone 운영 정보 조회
        response = api_client.get_zone_operation_info(zone_id)
        
        # Then: 응답 구조 검증 (실제 API 응답 구조에 맞게 수정 필요)
        assert response is not None
        # TODO: Charles에서 실제 응답 확인 후 필드 검증 추가
        # 예상 필드: zone_id, operation_status, operating_hours 등
        
    @pytest.mark.smoke
    def test_zone_operation_response_time(self, api_client):
        """Zone 운영 정보 조회 응답 시간 테스트"""
        # Given: 특정 zone_id
        zone_id = 67
        
        # When: 응답 시간 측정
        start_time = time.time()
        response = api_client.get_zone_operation_info(zone_id)
        elapsed_time = time.time() - start_time
        
        # Then: 3초 이내 응답
        assert elapsed_time < 3.0, f"응답 시간 초과: {elapsed_time:.2f}초"
        assert response is not None
        
    def test_invalid_zone_id_handling(self, api_client):
        """잘못된 Zone ID 처리 테스트"""
        # Given: 존재하지 않는 zone_id
        invalid_zone_id = 99999
        
        # When: 잘못된 zone_id로 조회
        response = api_client.get_zone_operation_info(invalid_zone_id)
        
        # Then: 적절한 에러 처리 (응답이 None이거나 error 필드 포함)
        # TODO: 실제 API 에러 응답 확인 후 검증 로직 수정
        assert response is None or "error" in str(response).lower()


@pytest.mark.api
@pytest.mark.zone
@pytest.mark.integration
class TestZoneImageUrls:
    """Zone 이미지 URL 검증 테스트"""
    
    def test_zone_image_url_format(self, api_client):
        """Zone 이미지 URL 형식 검증"""
        # Given: Zone 목록 조회
        zones_response = api_client.list_simple_zones()
        
        # When: 첫 번째 Zone의 이미지 URL 확인
        # TODO: 실제 응답 구조에 맞게 수정
        # 예상: zones_response['zones'][0]['image_url']
        
        # Then: CloudFront URL 형식 검증
        expected_pattern = "https://d1fxl86ei6civ0.cloudfront.net/zone_images/"
        # assert image_url.startswith(expected_pattern)
        
    def test_multiple_zone_images_accessible(self, api_client):
        """여러 Zone 이미지 접근 가능 여부 테스트"""
        # Given: 여러 Zone ID
        zone_ids = [2, 67, 9, 20, 18]
        
        # When & Then: 각 Zone의 이미지 URL이 존재하는지 확인
        for zone_id in zone_ids:
            response = api_client.get_zone_operation_info(zone_id)
            assert response is not None
            # TODO: 이미지 URL 필드 확인 및 검증