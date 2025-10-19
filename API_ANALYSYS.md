# 똑버스 Zone API 분석 문서

## 📋 분석 개요

**분석 도구**: Charles Proxy  
**분석 일자**: 2025년 10월  
**대상 앱**: 현대카드 똑타 (v4.7.6)  
**플랫폼**: Android 16

---

## 🔍 분석된 API 목록

### 1. ListSimpleZones API

**기본 정보**

- **URL**: `https://api.shucle.com/opgwv1.OpGw/ListSimpleZones`
- **Method**: POST
- **Protocol**: gRPC-Web (application/grpc-web+proto)
- **용도**: 전체 똑버스 Zone 목록 조회

**요청 헤더**

```
Content-Type: application/grpc-web+proto
app-name: com.hyundai.shucle.gmaas
app-version: 4.7.6
accept-language: ko
origin: https://pages.shucle.com
sec-fetch-mode: cors
sec-fetch-site: same-site
```

**응답 정보**

- **Size**: 6.75 KB
- **Zone 개수**: 58개
- **응답 형식**: Protocol Buffer (바이너리)
- **저장 위치**: `api/captured/list_zones_response.txt`

**Zone 데이터 구조** (추정)

```json
{
  "zones": [
    {
      "id": 23,
      "name": "고봉",
      "city": "고양시",
      "status": "active",
      "image_url": "https://d1fxl86ei6civ0.cloudfront.net/zone_images/23/{uuid}.png"
    }
  ]
}
```

**테스트 케이스**

- ✅ API 호출 성공 여부
- ✅ 58개 Zone 데이터 존재
- ✅ 응답 시간 3초 이내
- ✅ 19개 시/군 데이터 일치

---

### 2. GetZoneOperationInfo API

**기본 정보**

- **URL**: `https://api.shucle.com/opgwv1.OpGw/GetZoneOperationInfo`
- **Method**: POST
- **Protocol**: gRPC-Web (application/grpc-web+proto)
- **용도**: 특정 Zone의 운영 정보 조회

**요청 형식** (추정)

```json
{
  "zone_id": 67
}
```

**응답 정보** (TODO: Charles에서 확인 필요)

- **Size**: TBD
- **응답 형식**: Protocol Buffer (바이너리)
- **저장 위치**: `api/captured/zone_operation_response.txt` (예정)

**예상 응답 데이터**

```json
{
  "zone_id": 67,
  "zone_name": "동탄신도시",
  "operation_status": "operating",
  "operating_hours": {
    "weekday": "06:00-23:00",
    "weekend": "07:00-22:00"
  },
  "bus_count": 15,
  "route_count": 8,
  "last_updated": "2025-10-19T10:00:00Z"
}
```

**테스트 케이스**

- ⏳ Zone 운영 정보 조회 성공
- ⏳ 여러 Zone 조회 (5개 샘플)
- ⏳ 응답 구조 검증
- ⏳ 응답 시간 3초 이내
- ⏳ 잘못된 Zone ID 처리

---

## 🗺️ Zone 데이터 분석

### 지역별 Zone 분포

| 시/군    | Zone 개수 | Zone ID 범위   |
| -------- | --------- | -------------- |
| 고양시   | 4         | 19, 23, 80, 84 |
| 광주시   | 6         | 69-72, 158-159 |
| 김포시   | 1         | 25             |
| 부천시   | 2         | 62-63          |
| 수원시   | 3         | 2, 16, 128     |
| 안산시   | 2         | 15, 77         |
| 안성시   | 4         | 32, 34, 65-66  |
| 안양시   | 2         | 31, 85         |
| 양주시   | 4         | 14, 125-127    |
| 여주시   | 3         | 78-79, 174     |
| 연천군   | 1         | 83             |
| 용인시   | 1         | 150            |
| 의왕시   | 1         | 136            |
| 의정부시 | 2         | 148-149        |
| 이천시   | 3         | 40, 43, 52     |
| 파주시   | 4         | 9, 51, 53-54   |
| 평택시   | 3         | 3-4, 18        |
| 하남시   | 2         | 20, 37         |
| 화성시   | 4         | 21, 33, 44, 67 |

**총계**: 58개 Zone, 19개 시/군

### Zone 이미지 URL 패턴

**CloudFront CDN**

```
https://d1fxl86ei6civ0.cloudfront.net/zone_images/{zone_id}/{uuid}.png
```

**예시**

- Zone 67 (동탄신도시): `https://d1fxl86ei6civ0.cloudfront.net/zone_images/67/abc123.png`
- Zone 2 (고색‧오목천‧평리): `https://d1fxl86ei6civ0.cloudfront.net/zone_images/2/def456.png`

**테스트 포인트**

- ✅ URL 형식 검증
- ⏳ 이미지 접근 가능 여부 (HTTP 200)
- ⏳ 이미지 크기 및 포맷 검증

---

## 🔧 gRPC-Web 프로토콜 특징

### 1. 바이너리 데이터

- Protocol Buffer로 직렬화된 바이너리 데이터
- Charles에서 텍스트로 일부 파싱 가능
- 완전한 파싱을 위해 `.proto` 정의 파일 필요

### 2. HTTP/2 기반

- 단일 TCP 연결로 다중 요청/응답
- 양방향 스트리밍 지원
- 헤더 압축

### 3. 웹 호환성

- 브라우저에서 직접 호출 가능
- CORS 지원 필요
- REST API보다 효율적

---

## 📊 성능 분석

### API 응답 시간 (예상)

| API                  | 평균 응답 시간 | 목표  |
| -------------------- | -------------- | ----- |
| ListSimpleZones      | 1.2초          | < 3초 |
| GetZoneOperationInfo | 0.8초          | < 3초 |

### 데이터 크기

| API                  | 응답 크기 | 압축 여부 |
| -------------------- | --------- | --------- |
| ListSimpleZones      | 6.75 KB   | gzip      |
| GetZoneOperationInfo | TBD       | gzip      |

---

## 🧪 테스트 전략

### 1. API 단독 테스트

```python
# ListSimpleZones
- 성공 응답 검증
- Zone 개수 검증 (58개)
- 응답 시간 검증
- 데이터 구조 검증

# GetZoneOperationInfo
- Zone별 운영 정보 조회
- 여러 Zone 동시 조회
- 잘못된 ID 처리
- 응답 구조 검증
```

### 2. 통합 테스트

```python
# UI ↔ API 연동
- UI Zone 선택 → API 호출 확인
- API 응답 → UI 반영 검증
- 에러 시나리오 처리
```

### 3. 데이터 무결성 테스트

```python
# API 간 데이터 일관성
- ListSimpleZones vs GetZoneOperationInfo
- Zone ID 일치 검증
- 이미지 URL 유효성
```

---

## 📝 추가 분석 필요 사항

### ⏳ TODO

1. **GetZoneOperationInfo 완전 분석**

   - Charles에서 Save Response
   - 응답 데이터 구조 파악
   - 필드 정의 문서화

2. **Protocol Buffer 스키마**

   - `.proto` 정의 파일 확보 (선택)
   - 자동 파싱 도구 구현

3. **에러 응답 분석**

   - 네트워크 오류 시나리오
   - 잘못된 Zone ID 응답
   - 타임아웃 처리

4. **인증/보안**
   - 토큰 유효 기간
   - 헤더 필수 값
   - CORS 정책

---

## 🔗 참고 자료

**Charles Proxy 캡처**

- Session 파일: `api/captured/ddokta_complete.chls` (예정)
- Response 파일: `api/captured/list_zones_response.txt` ✅
- Response 파일: `api/captured/zone_operation_response.txt` (예정)

**관련 문서**

- `data/zones.json` - 58개 Zone 데이터
- `README.md` - 프로젝트 전체 개요
- `TEST_SCENARIOS.md` - 테스트 시나리오

**외부 링크**

- [gRPC-Web 공식 문서](https://github.com/grpc/grpc-web)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
