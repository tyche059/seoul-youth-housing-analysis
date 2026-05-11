# seoul-youth-housing-analysis

# 시각화 관련 프롬프트
https://drive.google.com/file/d/11F6ICDdFf6MQyqmxMM0tabQCYJgYPc8n/view?usp=sharing, https://drive.google.com/file/d/1Qt_w_hds0wkq_oe5Td6-zciZzOQgTAdw/view?usp=sharing, https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221dHupdp9O8c6m3WTz8sieuKLtaFFdfEWV%22%5D,%22action%22:%22open%22,%22userId%22:%22102706636355949686702%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing

# 대시보드 관련 프롬프트
https://drive.google.com/file/d/1LLKUPDZqdXN6hZdGpnPRlJmmcD1pU0yN/view?usp=sharing, https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221rgsg6QSeIJfTaUFa-e-gdM6fpqJZcQLT%22%5D,%22action%22:%22open%22,%22userId%22:%22102706636355949686702%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing

# 사용 데이터
(서울 열린 데이터 광장) -> 청년안심주택임대료정보 / 거주지역_가구주의 성_연령대별 무주택 가구수 통계
(서울 통계 통합 플랫폼) -> 미거주+주택(빈집)+현황(구별)

# 데이터 클랜징(전처리) 과정
1. 3개 파일 전부 다운 받은 후 하나하나 열어보며 같은 내용인데 필드명이 다른 것 혹은 필요한 정보인데 없는 정보 확인
2. 확인 결과에 맞춰 데이터 전처리
   - 청년안심주택 자료의 경우, 주소가 '서울특별시 ㅇㅇ구 ~'로 되어있는 것도 있고 '서울시 ㅁㅁ구 ~'로 되어있는 것도 있어서 다른 파일과 동일하게 '&&구'로 통일함.
   - 미거주 주택 자료의 경우, 데이터 필드가 왼쪽에 정렬 되어 있어 위에 정렬되도록 정리함.
