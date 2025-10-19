# 똑타 똑버스 E2E 테스트 자동화

현대카드 똑타 앱의 똑버스 Zone 기능에 대한 E2E 테스트 자동화 프로젝트

## 🎯 프로젝트 개요

- **목적**: 똑버스 구역(Zone) 관리 기능 자동화 테스트
- **범위**: MVP - Zone API 2개 + UI 테스트
- **기간**: 1일
- **기술**: Python, pytest, Appium

## 🧪 테스트 범위

### API 테스트 (3개)

- ✅ 구역 목록 조회 (ListSimpleZones)
- ✅ 58개 구역 개수 검증
- ✅ 응답 시간 검증 (3초 이내)

### UI 테스트 (2개)

- ✅ 구역 카드 표시 확인
- ✅ 구역 선택 기능

**총 5개 테스트**

## 📊 테스트 결과

```
========== test session starts ==========
collected 5 items

api/tests/test_list_zones.py::test_list_zones_success PASSED
api/tests/test_list_zones.py::test_zone_count PASSED
api/tests/test_list_zones.py::test_response_time PASSED
appium/tests/test_zone_list.py::test_zone_cards_displayed PASSED
appium/tests/test_zone_list.py::test_zone_selection PASSED

========== 5 passed in 15.32s ==========
```

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. API 테스트 실행

```bash
pytest api/tests/ -v
```

### 3. UI 테스트 실행

```bash
# Appium 서버 시작 (별도 터미널)
appium

# 테스트 실행
pytest appium/tests/ -v
```

### 4. 전체 테스트

```bash
pytest -v --html=reports/report.html
```

## 📂 프로젝트 구조

```
ddokta-e2e-automation/
├─ api/
│  ├─ helpers/api_client.py
│  └─ tests/test_list_zones.py
├─ appium/
│  ├─ pages/ddokta_bus_page.py
│  └─ tests/test_zone_list.py
├─ data/zones.json
├─ conftest.py
└─ README.md
```

## 🔧 기술 스택

- **Language**: Python 3.8+
- **Test Framework**: pytest
- **API Testing**: requests
- **Mobile Testing**: Appium
- **Reporting**: pytest-html

## 📈 주요 성과

- ✅ gRPC-Web API 분석 및 테스트
- ✅ 58개 구역 데이터 검증
- ✅ Appium으로 모바일 UI 자동화
- ✅ API + UI 통합 테스트 구현

## 🎓 학습 내용

1. **Charles Proxy**를 활용한 API 캡처 및 분석
2. **gRPC-Web** 프로토콜 이해
3. **pytest fixture** 활용한 테스트 구조화
4. **Page Object Pattern** 적용
5. **CI/CD** 파이프라인 구성 (향후 확장)

## 📌 향후 계획

- [ ] 버스 검색 API 테스트 추가
- [ ] 정류장 API 테스트 추가
- [ ] 통합 테스트 확장
- [ ] Allure 리포트 적용
- [ ] GitHub Actions CI/CD

## 👤 Author

김선아

## 📄 License

MIT
