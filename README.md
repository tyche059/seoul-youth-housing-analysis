# seoul-youth-housing-analysis

# 시각화 관련 프롬프트
https://drive.google.com/file/d/11F6ICDdFf6MQyqmxMM0tabQCYJgYPc8n/view?usp=sharing, https://drive.google.com/file/d/1Qt_w_hds0wkq_oe5Td6-zciZzOQgTAdw/view?usp=sharing, https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221dHupdp9O8c6m3WTz8sieuKLtaFFdfEWV%22%5D,%22action%22:%22open%22,%22userId%22:%22102706636355949686702%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing

# 대시보드 관련 프롬프트
https://drive.google.com/file/d/1LLKUPDZqdXN6hZdGpnPRlJmmcD1pU0yN/view?usp=sharing, https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221rgsg6QSeIJfTaUFa-e-gdM6fpqJZcQLT%22%5D,%22action%22:%22open%22,%22userId%22:%22102706636355949686702%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing

# 사용 데이터
- (서울 열린 데이터 광장) -> 청년안심주택임대료정보 / 거주지역_가구주의 성_연령대별 무주택 가구수 통계
- (서울 통계 통합 플랫폼) -> 미거주+주택(빈집)+현황(구별)

# 데이터 클랜징(전처리) 과정
1. 3개 파일 전부 다운 받은 후 하나하나 열어보며 같은 내용인데 필드명이 다른 것 혹은 필요한 정보인데 없는 정보 확인
2. 확인 결과에 맞춰 데이터 전처리
   - 청년안심주택 자료의 경우, 주소가 '서울특별시 ㅇㅇ구 ~'로 되어있는 것도 있고 '서울시 ㅁㅁ구 ~'로 되어있는 것도 있어서 다른 파일과 동일하게 '&&구'로 통일하였다.
   - 미거주 주택 자료의 경우, 데이터 필드가 왼쪽에 정렬 되어 있어 위에 정렬되도록 정리하였.

# 대시보드 작성
**1. 분석 주제 :**
   - 시군구별 무주택 청년 인구와 청년주택 공급의 미스매치 비율 (원그래프&상세 표)
   - 바로 입주 가능한 시군구 Top5 (가로 막대 그래프)
   - 평균 임대료가 높은 시군구 Top5 (버블 차트)
     
**2. SQL문 작성** (app.py 파일에 존재)

**3. 예상 결과 및 인사이트**
   - 시군구별 무주택 청년 인구와 청년주택 공급의 미스매치 비율 (원그래프) -> 대학가 주변의 미스매치 비율이 가장 높을 것이다.
   - 바로 입주 가능한 시군구 Top5 (가로 막대 그래프) -> 서울 중심부, 대학가 근처를 제외한 곳들(외곽)이 공실이 많을 것이다.
   - 평균 임대료가 높은 시군구 Top5 (버블 차트) -> 한강 주변, 대학가 주변이 높을 것이다.
  
# 시각화 결과
**1. 시군구별 무주택 청년 인구와 청년주택 공급의 미스매치 비율 (원그래프&상세 표)**
   <img width="1336" height="1149" alt="image" src="https://github.com/user-attachments/assets/8128835e-8de2-47d5-8c82-4099f68dd035" />
   -> 원그래프만 봤을 때 수요(빨간색)에 비해 공급(파란색)이 확연히 적은 것을 볼 수 있고, 상세 표와 함께 보면 수요 대비 공급 비율이 0인 지역도 심심찮게 볼 수 있다.
   
**2. 바로 입주 가능한 시군구 Top5 (가로 막대 그래프)**
   <img width="1318" height="534" alt="image" src="https://github.com/user-attachments/assets/73c0f6a0-2e20-4634-b97b-0f5ea7c102cf" />
   -> 구도심이나 서울 외곽에 공실이 많을 것이라 예상했는데, 예상 외로 강남구가 2위에 올라 생각지 못한 결과를 얻을 수 있었다. 
   
**3. 평균 임대료가 높은 시군구 Top5 (버블 차트)**
   <img width="1368" height="554" alt="image" src="https://github.com/user-attachments/assets/8dd9b69a-2f90-47e1-bffb-301159c7832b" />
   -> 예상대로 강남구가 임대료가 높았지만, 강남구만 월등하게 높고 타지역은 비슷한 정도임을 알게 되었다.
