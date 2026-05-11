import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# 페이지 기본 설정
st.set_page_config(page_title="서울시 청년 주거 대시보드", layout="wide")

# 타이틀
st.title("🏘️ 서울시 청년 주거 데이터 분석 대시보드")
st.markdown("데이터 초보자도 쉽게 이해할 수 있는 서울시 무주택 청년과 주거 공급 현황입니다.")

# 1. DB 파일 존재 여부 확인 (친절한 에러 메시지)
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
st.header("1. 무주택 청년 수요 대비 안심주택 공급 비율 (미스매치)")

sql_1 = """
WITH Demand AS (
    SELECT 시군구, SUM(무주택가구수) AS 총수요
    FROM 무주택_가구수
    GROUP BY 시군구
),
Supply AS (
    SELECT 시군구, SUM(전체세대수) AS 총공급
    FROM 청년안심주택
    GROUP BY 시군구
)
SELECT SUM(d.총수요) AS 총수요, SUM(s.총공급) AS 총공급
FROM Demand d
JOIN Supply s ON d.시군구 = s.시군구
"""

df_1 = load_data(sql_1)

# 파이 차트를 위해 데이터 형태 변환
df_pie = pd.DataFrame({
    '구분':['무주택 가구 (수요)', '청년안심주택 (공급)'],
    '가구수': [df_1['총수요'][0], df_1['총공급'][0]]
})

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**① 시각화 (원 그래프)**")
    fig1 = px.pie(df_pie, names='구분', values='가구수', hole=0.3, color='구분',
                  color_discrete_sequence=['#FF9999', '#66B2FF'])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("**② 사용한 SQL**")
    st.code(sql_1, language='sql')
    st.markdown("**③ 인사이트**")
    st.info("💡 **수요에 비해 공급이 턱없이 부족합니다.**\n\n무주택 가구 수(수요)가 청년안심주택 세대수(공급)를 압도하고 있습니다. 청년 주거난 해결을 위해 안심주택 공급량을 지금보다 훨씬 공격적으로 늘려야 함을 시사합니다.")

st.divider()

# ==========================================
# 차트 2: 입주 가능 시군구 Top5 (빈집 현황)
# ==========================================
st.header("2. 빈집이 많은 시군구 Top 5 (입주 및 리모델링 잠재 구역)")

sql_2 = """
SELECT 시군구, SUM(소계) AS 빈집수
FROM 빈집_현황
WHERE 시군구 != '계'
GROUP BY 시군구
ORDER BY 빈집수 DESC
LIMIT 5
"""

df_2 = load_data(sql_2)

col3, col4 = st.columns([1, 1])

with col3:
    st.markdown("**① 시각화 (가로 막대 차트)**")
    # 가로 막대는 y축에 범주(시군구)가 와야 보기 좋습니다.
    fig2 = px.bar(df_2.sort_values('빈집수'), x='빈집수', y='시군구', orientation='h', 
                  color='빈집수', color_continuous_scale='Greens')
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.markdown("**② 사용한 SQL**")
    st.code(sql_2, language='sql')
    st.markdown("**③ 인사이트**")
    st.info("💡 **도심 외곽 또는 구도심에 빈집이 집중되어 있습니다.**\n\n상위 5개 지역의 빈집들을 지자체에서 매입하여 리모델링한 뒤, 청년 공공임대주택으로 활용한다면 주거 미스매치 해소에 큰 도움이 될 수 있습니다.")

st.divider()

# ==========================================
# 차트 3: 임대료 높은 시군구 Top 5
# ==========================================
st.header("3. 청년안심주택 월임대료가 가장 높은 시군구 Top 5")

sql_3 = """
SELECT 시군구, ROUND(AVG(월임대료), 0) AS 평균월임대료
FROM 청년안심주택
GROUP BY 시군구
ORDER BY 평균월임대료 DESC
LIMIT 5
"""

df_3 = load_data(sql_3)

col5, col6 = st.columns([1, 1])

with col5:
    st.markdown("**① 시각화 (버블 차트)**")
    # 버블 차트는 scatter plot에서 size 속성을 활용합니다.
    fig3 = px.scatter(df_3, x='시군구', y='평균월임대료', size='평균월임대료', 
                      color='시군구', size_max=40)
    fig3.update_layout(yaxis_range=[df_3['평균월임대료'].min()*0.8, df_3['평균월임대료'].max()*1.2])
    st.plotly_chart(fig3, use_container_width=True)

with col6:
    st.markdown("**② 사용한 SQL**")
    st.code(sql_3, language='sql')
    st.markdown("**③ 인사이트**")
    st.info("💡 **주요 업무 지구나 번화가의 임대료 부담이 큽니다.**\n\n임대료가 높은 상위 5개 지역은 주로 역세권 및 상업 중심지입니다. 이 지역에 거주해야 하는 청년들을 위한 추가적인 주거비(월세) 지원 정책이 필요해 보입니다.")
