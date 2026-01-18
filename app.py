import streamlit as st

# 1. 페이지 설정 (가장 상단에 위치해야 함)
st.set_page_config(page_title="바카라 분석기", layout="centered")

# 2. 커스텀 스타일 (에러를 일으키는 복잡한 문법 제외)
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    .main-box {
        border: 3px solid #F1C40F;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        background-color: #1E1E1E;
        margin-bottom: 20px;
    }
    .road-map-bg {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        min-height: 150px;
        display: flex;
        flex-direction: row;
        overflow-x: auto;
        margin-bottom: 20px;
    }
    .grid-column { display: flex; flex-direction: column; width: 30px; }
    .dot {
        width: 24px; height: 24px; border-radius: 50%;
        margin: 3px; display: flex; align-items: center;
        justify-content: center; font-size: 10px; color: white; font-weight: bold;
    }
    /* 버튼 크기 및 색상 강제 지정 */
    div.stButton > button {
        width: 100%;
        height: 100px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_value=True)

# 3. 데이터 로직 (5칸 꺾기 기능)
if 'history' not in st.session_state:
    st.session_state.history = []

def get_road_data(history):
    columns = [[]]
    c_idx = 0
    for i, res in enumerate(history):
        if i > 0 and res != history[i-1]:
            c_idx += 1
            columns.append([])
        elif len(columns[c_idx]) >= 5: # 5칸 차면 옆으로 꺾기
            c_idx += 1
            columns.append([])
        columns[c_idx].append(res)
    return columns

# --- 화면 그리기 ---

# 상단 전광판 (노란 테두리)
st.markdown("""
    <div class="main-box">
        <h1 style="color: white; margin: 0; font-size: 50px;">플레이어</h1>
        <p style="color: #F1C40F; font-size: 22px;">15,000원 배팅</p>
    </div>
""", unsafe_allow_html=True)

# 기록판 (흰색 박스 내 꺾기 로직 반영)
road_data = get_road_data(st.session_state.history)
grid_html = '<div class="road-map-bg">'
for col in road_data:
    grid_html += '<div class="grid-column">'
    for item in col:
        color = "#FF4B4B" if item == "B" else "#007BFF"
        grid_html += f'<div class="dot" style="background-color: {color};">{item}</div>'
    grid_html += '</div>'
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

# 메인 버튼 (가로 배치)
col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 플레이어", key="p_btn"):
        st.session_state.history.append("P")
        st.rerun()
with col2:
    if st.button("🔴 뱅커", key="b_btn"):
        st.session_state.history.append("B")
        st.rerun()

st.write(" ")

# 하단 보조 버튼 (카메라, 취소, 리셋)
f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
with f_col1:
    if st.button("📸 카메라"):
        st.toast("카메라 연결 중...")
with f_col2:
    if st.button("↩️ 취소"):
        if st.session_state.history:
            st.session_state.history.pop()
            st.rerun()
with f_col3:
    if st.button("♻️ 리셋"):
        st.session_state.history = []
        st.rerun()
