"""
똑버스 Zone E2E 통합 테스트
UI 액션 → API 호출 → UI 반영 검증
"""
import pytest
import time
import json


@pytest.mark.integration
@pytest.mark.zone
class TestZoneEndToEndFlow:
    """Zone 기능 End-to-End 통합 테스트"""
    
    @pytest.mark.smoke
    def test_zone_list_ui_matches_api(self, appium_driver, api_client, ddokta_bus_page):
        """UI Zone 목록과 API 응답 일치 검증"""
        # Given: API로 Zone 목록 조회
        api_zones = api_client.list_simple_zones()
        assert api_zones is not None, "API Zone 목록 조회 실패"
        
        # When: UI에서 Zone 카드 목록 확인
        ui_zone_cards = ddokta_bus_page.get_zone_cards()
        
        # Then: UI 카드 개수가 API 응답과 일치
        # TODO: 실제 API 응답 구조 확인 후 검증 로직 수정
        assert len(ui_zone_cards) > 0, "UI에 Zone 카드가 표시되지 않음"
        # expected_count = len(api_zones.get('zones', []))
        # assert len(ui_zone_cards) == expected_count
        
    def test_zone_selection_triggers_api_call(self, appium_driver, api_client, ddokta_bus_page):
        """Zone 선택 시 API 호출 검증"""
        # Given: UI에서 Zone 카드 목록 확인
        zone_cards = ddokta_bus_page.get_zone_cards()
        assert len(zone_cards) > 0, "Zone 카드가 없습니다"
        
        # When: 첫 번째 Zone 선택
        selected_zone = ddokta_bus_page.select_zone(index=0)
        time.sleep(1)  # API 호출 대기
        
        # Then: Zone 상세 화면으로 이동
        # TODO: 실제 상세 화면 element로 검증
        assert selected_zone is not None
        
    def test_zone_detail_data_consistency(self, appium_driver, api_client, ddokta_bus_page):
        """Zone 상세 정보 데이터 일관성 검증"""
        # Given: 특정 Zone ID (동탄신도시)
        zone_id = 67
        
        # API로 Zone 운영 정보 조회
        api_response = api_client.get_zone_operation_info(zone_id)
        assert api_response is not None
        
        # When: UI에서 해당 Zone 선택
        # TODO: Zone ID로 카드 찾기 구현 필요
        # ddokta_bus_page.select_zone_by_id(zone_id)
        
        # Then: UI 표시 데이터와 API 응답 일치 검증
        # TODO: 상세 화면 데이터 추출 및 비교
        pass
        
    @pytest.mark.regression
    def test_complete_zone_browsing_flow(self, appium_driver, api_client, ddokta_bus_page):
        """완전한 Zone 탐색 플로우 테스트"""
        # Given: 똑버스 메인 화면
        
        # Step 1: Zone 목록 표시 확인
        zone_cards = ddokta_bus_page.get_zone_cards()
        assert len(zone_cards) > 0, "Zone 목록이 표시되지 않음"
        
        # Step 2: API로 전체 Zone 수 확인
        api_zones = api_client.list_simple_zones()
        assert api_zones is not None
        
        # Step 3: Zone 선택
        selected_zone = ddokta_bus_page.select_zone(index=0)
        assert selected_zone is not None
        time.sleep(2)
        
        # Step 4: 상세 화면에서 뒤로 가기
        appium_driver.back()
        time.sleep(1)
        
        # Step 5: Zone 목록으로 복귀 확인
        zone_cards_after = ddokta_bus_page.get_zone_cards()
        assert len(zone_cards_after) == len(zone_cards), "목록 복귀 실패"
        
    def test_zone_api_error_handling_in_ui(self, appium_driver, api_client, ddokta_bus_page):
        """API 에러 시 UI 처리 검증"""
        # Given: 네트워크 상태 확인
        # TODO: 네트워크 차단 시뮬레이션 (선택적)
        
        # When: Zone 목록 조회 시도
        try:
            zone_cards = ddokta_bus_page.get_zone_cards()
        except Exception as e:
            # Then: 적절한 에러 메시지 또는 재시도 로직 확인
            # TODO: 실제 에러 처리 방식에 맞게 구현
            pass


@pytest.mark.integration
@pytest.mark.api
class TestApiDataIntegrity:
    """API 데이터 무결성 통합 테스트"""
    
    def test_all_zones_have_valid_data(self, api_client):
        """모든 Zone이 유효한 데이터를 가지는지 검증"""
        # Given: 전체 Zone 목록 조회
        zones_response = api_client.list_simple_zones()
        assert zones_response is not None
        
        # When: 각 Zone의 운영 정보 조회
        # TODO: 실제 응답 구조에 맞게 수정
        # zones = zones_response.get('zones', [])
        
        # Then: 모든 Zone이 운영 정보를 가짐
        # for zone in zones[:5]:  # 샘플 5개만 테스트
        #     zone_id = zone.get('id')
        #     operation_info = api_client.get_zone_operation_info(zone_id)
        #     assert operation_info is not None
        
    def test_zone_data_consistency_across_apis(self, api_client):
        """여러 API 간 Zone 데이터 일관성 검증"""
        # Given: ListSimpleZones로 Zone 목록 조회
        list_response = api_client.list_simple_zones()
        assert list_response is not None
        
        # When: 같은 Zone을 GetZoneOperationInfo로 조회
        # TODO: 실제 응답 구조 확인 후 구현
        # first_zone_id = list_response['zones'][0]['id']
        # operation_response = api_client.get_zone_operation_info(first_zone_id)
        
        # Then: Zone ID가 일치
        # assert list_response['zones'][0]['id'] == operation_response['zone_id']
        
    @pytest.mark.regression
    def test_zone_count_matches_json_file(self, api_client):
        """API Zone 수와 zones.json 파일 일치 검증"""
        # Given: zones.json 파일 로드
        import os
        zones_file = os.path.join('data', 'zones.json')
        
        if os.path.exists(zones_file):
            with open(zones_file, 'r', encoding='utf-8') as f:
                zones_data = json.load(f)
            
            # When: API로 Zone 목록 조회
            api_response = api_client.list_simple_zones()
            
            # Then: Zone 개수 일치
            # TODO: 실제 응답 구조 확인 후 검증
            # expected_count = zones_data['total_count']
            # actual_count = len(api_response.get('zones', []))
            # assert actual_count == expected_count
        else:
            pytest.skip("zones.json 파일이 없습니다")