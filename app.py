import streamlit as st

# 1. 화면 설정
st.set_page_config(page_title="바카라 분석기", layout="centered")

# 2. 스타일 설정 (사진과 유사한 검은색 테마 및 버튼 크기)
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    .header-box {
        border: 2px solid #F1C40F; border-radius: 15px;
        padding: 30px; text-align: center; margin-bottom: 20px;
        background-color: #1E1E1E;
    }
    .grid-container {
        background-color: white; border-radius: 10px;
        padding: 10px; display: flex; flex-direction: row; min-height: 180px;
    }
    .column { display: flex; flex-direction: column; width: 35px; }
    .dot {
        width: 25px; height: 25px; border-radius: 50%;
        margin: 2px; display: flex; align-items: center;
        justify-content: center; font-size: 10px; color: white; font-weight: bold;
    }
    .stButton > button { width: 100%; height: 70px; font-size: 18px; border-radius: 12px; }
    </style>
""", unsafe_allow_value=True)

# 3. 데이터 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 4. 분석 로직 (5칸 후 꺾기)
def get_main_road(history):
    columns = [[]]
    col_idx = 0
    for i, res in enumerate(history):
        if i > 0 and res != history[i-1]:
            col_idx += 1
            columns.append([])
        elif len(columns[col_idx]) >= 5: # 5칸 차면 꺾기
            col_idx += 1
            columns.append([])
        columns[col_idx].append(res)
    return columns

# --- UI 구현 ---
# 상단 전광판
st.markdown("""
    <div class="header-box">
        <h1 style="color: white; margin: 0;">플레이어</h1>
        <p style="color: #F1C40F; font-size: 20px;">15,000원 배팅</p>
    </div>
""", unsafe_allow_html=True)

# 기록판 (출목표)
road_data = get_main_road(st.session_state.history)
cols = st.columns([1])
with cols[0]:
    html_grid = '<div class="grid-container">'
    for col in road_data:
        html_grid += '<div class="column">'
        for item in col:
            color = "#E74C3C" if item == "B" else "#3498DB"
            html_grid += f'<div class="dot" style="background-color: {color};">{item}</div>'
        html_grid += '</div>'
    html_grid += '</div>'
    st.markdown(html_grid, unsafe_allow_html=True)

st.write("")

# 메인 버튼 (가로 배치)
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("🔵 플레이어"):
        st.session_state.history.append("P")
        st.rerun()
with btn_col2:
    if st.button("🔴 뱅커"):
        st.session_state.history.append("B")
        st.rerun()

# 하단 기능바
st.write("")
f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
with f_col1:
    if st.button("📸"): st.toast("카메라 준비 중")
with f_col2:
    if st.button("취소"):
        if st.session_state.history:
            st.session_state.history.pop()
            st.rerun()
with f_col3:
    if st.button("리셋"):
        st.session_state.history = []
        st.rerun()
