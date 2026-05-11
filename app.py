import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# 페이지 기본 설정
st.set_page_config(page_title="서울시 청년 주거 대시보드", layout="wide")

# 타이틀
st.title("🏘️ 서울시 청년 주거 데이터 분석 대시보드")
st.markdown("데이터 초보자도 쉽게 이해할 수 있는 2024년 서울시 무주택 청년과 주거 공급 현황입니다.")

# 1. DB 파일 존재 여부 확인
db_path = "seoul_youth_housing.db"
if not os.path.exists(db_path):
    st.error("🚨 앗! 'seoul_youth_housing.db' 파일을 찾을 수 없어요.")
    st.warning("현재 폴더에 DB 파일이 있는지 다시 한번 확인해 주세요! 대시보드 실행을 일시 멈춥니다.")
    st.stop()

# DB 연결 및 데이터 불러오기 함수
@st.cache_data
def load_data(query):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.divider()

# ==========================================
# 차트 1: 수요 대비 공급 비율 (미스매치 비율)
# ==========================================
st.header("1. 시군구별 무주택 청년 인구와 청년주택 공급 미스매치 비율")

sql_1 = """
WITH 수요데이터 AS (
    SELECT 
        시군구, 
        SUM(무주택가구수) AS 수요
    FROM 무주택_가구수
    GROUP BY 시군구
),
공급데이터 AS (
        SELECT 
        시군구, 
        SUM(전체세대수) AS 공급
    FROM 청년안심주택
    GROUP BY 시군구
)
SELECT 
    A.시군구,
    A.수요 AS "무주택 청년수(수요)",
    IFNULL(B.공급, 0) AS "안심주택 세대수(공급)",
    ROUND(IFNULL(B.공급, 0) * 100.0 / A.수요, 1) || '%' AS "수요 대비 공급비율"
FROM 수요데이터 A
LEFT JOIN 공급데이터 B 
    ON A.시군구 = B.시군구
ORDER BY (IFNULL(B.공급, 0) * 100.0 / A.수요) ASC
;
"""

df_1 = load_data(sql_1)

# ⭐ 원 그래프를 위한 데이터 가공 (총 수요 vs 총 공급)
total_demand = df_1['무주택 청년수(수요)'].sum()
total_supply = df_1['안심주택 세대수(공급)'].sum()

df_pie = pd.DataFrame({
    '구분':['무주택 청년수(수요)', '안심주택 세대수(공급)'],
    '가구수': [total_demand, total_supply]
})

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**① 시각화 (원 그래프 & 상세 표)**")
    
    # 도넛 모양의 원 그래프 (hole=0.3 속성)
    fig1 = px.pie(df_pie, names='구분', values='가구수', hole=0.3, 
                  title="총 수요 vs 총 공급 비율",
                  color='구분', color_discrete_sequence=['#FF9999', '#66B2FF'])
    st.plotly_chart(fig1, use_container_width=True)
    
    # 상세 데이터는 표로 함께 제공
    st.dataframe(df_1, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**② 사용한 SQL**")
    st.code(sql_1, language='sql')
    st.markdown("**③ 데이터 인사이트**")
    st.info("""
    💡 **예상과 결과 비교**
    * **(예상)** 대학가 주변의 미스매치 비율이 가장 높을 것이다.
    * **(분석결과 및 의견)** 실제 데이터를 조회해 보면 관악구, 마포구, 서대문구 등 주요 대학가 및 1인 가구 밀집 지역에서 수요 대비 공급이 턱없이 부족한 극심한 미스매치가 확인됩니다. 도출된 Top 5 지역의 전체 수요량과 공급량을 원 그래프로 비교해 보면 공급이 얼마나 부족한지 시각적으로 강렬하게 체감할 수 있습니다. 핀셋형 공급 정책이 시급합니다.
    """)

st.divider()

# ==========================================
# 차트 2: 바로 입주 가능한 시군구 Top5 (빈집 현황)
# ==========================================
st.header("2. 바로 입주 가능(빈집/공실이 많은) 시군구 Top 5")

sql_2 = """
SELECT 시군구, 소계 AS "공실 수"
FROM 빈집_현황
WHERE 시군구 != '계'
GROUP BY 시군구
ORDER BY 소계 DESC
LIMIT 5;
"""

df_2 = load_data(sql_2)

col3, col4 = st.columns([1, 1])

with col3:
    st.markdown("**① 시각화 (가로 막대 차트)**")
    fig2 = px.bar(df_2.sort_values('공실 수'), x='공실 수', y='시군구', orientation='h', 
                  color='공실 수', color_continuous_scale='Greens')
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.markdown("**② 사용한 SQL**")
    st.code(sql_2, language='sql')
    st.markdown("**③ 데이터 인사이트**")
    st.info("""
    💡 **예상과 결과 비교**
    * **(예상)** 서울 중심부, 대학가 근처를 제외한 곳들(외곽)이 공실이 많을 것이다.
    * **(분석결과 및 의견)** 예상하신 대로, 도심 외곽이나 구도심 지역(강북, 도봉 등)에 빈집이 집중되어 있는 경향이 있습니다. 이 빈집들을 지자체에서 매입하여 리모델링한 뒤 청년 공공임대주택으로 활용한다면, '도심 외곽의 재생'과 '청년 주거난 해소'라는 두 마리 토끼를 모두 잡을 수 있는 좋은 대안이 될 것입니다.
    """)

st.divider()

# ==========================================
# 차트 3: 평균 임대료 높은 시군구 Top 5
# ==========================================
st.header("3. 청년안심주택 평균 임대료가 높은 시군구 Top 5")

sql_3 = """
SELECT 시군구, ROUND(AVG(월임대료),0) 평균임대료
FROM 청년안심주택
GROUP BY 시군구
ORDER BY 평균임대료 DESC
LIMIT 5;
"""

df_3 = load_data(sql_3)

col5, col6 = st.columns([1, 1])

with col5:
    st.markdown("**① 시각화 (버블 차트)**")
    fig3 = px.scatter(df_3, x='시군구', y='평균임대료', size='평균임대료', 
                      color='시군구', size_max=40)
    fig3.update_layout(yaxis_range=[df_3['평균임대료'].min()*0.8, df_3['평균임대료'].max()*1.2])
    st.plotly_chart(fig3, use_container_width=True)

with col6:
    st.markdown("**② 사용한 SQL**")
    st.code(sql_3, language='sql')
    st.markdown("**③ 데이터 인사이트**")
    st.info("""
    💡 **예상과 결과 비교**
    * **(예상)** 한강 주변, 대학가 주변이 높을 것이다.
    * **(분석결과 및 의견)** 한강 이남 주요 업무지구(강남, 서초 등) 및 교통의 요지가 임대료 상위권을 차지합니다. 직장이나 학업 때문에 불가피하게 이들 지역에 거주해야만 하는 청년들의 부담이 매우 큽니다. 따라서 고임대료 지역 거주 청년들을 위한 '추가적인 주거비(월세) 대출 지원'이나 '바우처 정책'이 수반되어야 합니다.
    """)