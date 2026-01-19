import streamlit as st

# 1. 페이지 초기 설정
st.set_page_config(page_title="바카라 분석기", layout="centered")

# 2. 데이터 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 5칸 꺾기 로직 (핵심)
def get_baccarat_road(history):
    columns = [[]]
    c_idx = 0
    for i, res in enumerate(history):
        if i > 0 and res != history[i-1]:
            c_idx += 1
            columns.append([])
        elif len(columns[c_idx]) >= 5: # 5번째 칸이 차면 옆으로 꺾음
            c_idx += 1
            columns.append([])
        columns[c_idx].append(res)
    return columns

# --- 화면 레이아웃 시작 ---

# 상단 노란 테두리 전광판 (에러 없는 표준 방식)
st.markdown("""
    <div style="border: 4px solid #F1C40F; border-radius: 15px; padding: 30px; text-align: center; background-color: #1E1E1E; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 45px;">플레이어</h1>
        <p style="color: #F1C40F; font-size: 20px; font-weight: bold;">15,000원 배팅</p>
    </div>
""", unsafe_allow_html=True)

# 출목표 (기록판)
road_data = get_baccarat_road(st.session_state.history)
grid_html = '<div style="background-color: white; border-radius: 10px; padding: 15px; display: flex; flex-direction: row; min-height: 160px; overflow-x: auto;">'
for col in road_data:
    grid_html += '<div style="display: flex; flex-direction: column; width: 30px;">'
    for item in col:
        color = "#FF4B4B" if item == "B" else "#007BFF"
        grid_html += f'<div style="width: 24px; height: 24px; border-radius: 50%; background-color: {color}; margin: 3px; display: flex; align-items: center; justify-content: center; color: white; font-size: 10px; font-weight: bold;">{item}</div>'
    grid_html += '</div>'
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

st.write("") # 간격

# 메인 버튼 (가로 배치 & 크게)
m_col1, m_col2 = st.columns(2)
with m_col1:
    if st.button("🔵 플레이어 (PLAYER)", use_container_width=True):
        st.session_state.history.append("P")
        st.rerun()
with m_col2:
    if st.button("🔴 뱅커 (BANKER)", use_container_width=True):
        st.session_state.history.append("B")
        st.rerun()

st.write("---")

# 하단 보조 버튼 (카메라, 취소, 리셋)
b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
with b_col1:
    if st.button("📸 카메라", use_container_width=True):
        st.toast("카메라 기능을 불러오는 중입니다...")
with b_col2:
    if st.button("↩️ 취소", use_container_width=True):
        if st.session_state.history:
            st.session_state.history.pop()
            st.rerun()
with b_col3:
    if st.button("♻️ 리셋", use_container_width=True):
        st.session_state.history = []
        st.rerun()
