import streamlit as st

# 페이지 설정
st.set_page_config(page_title="바카라 분석기", layout="centered")

# CSS를 이용한 UI 커스텀 (버튼 크기 및 가로 배치)
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
    }
    .player-btn button { background-color: #3498DB !important; color: white !important; }
    .banker-btn button { background-color: #E74C3C !important; color: white !important; }
    .header-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #F1C40F;
        text-align: center;
        margin-bottom: 20px;
    }
    .circle {
        width: 30px; height: 30px; border-radius: 15px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: bold; margin: 2px; font-size: 12px;
    }
    </style>
""", unsafe_allow_value=True)

# 데이터 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 로직: 기록판 꺾기 계산 ---
def get_grid(history):
    columns = [[]]
    curr_col = 0
    for i, res in enumerate(history):
        if i > 0 and res != history[i-1]: # 결과 바뀌면 새 줄
            curr_col += 1
            columns.append([])
        elif len(columns[curr_col]) >= 5: # 5칸 다 차면 옆으로 꺾기
            curr_col += 1
            columns.append([])
        columns[curr_col].append(res)
    return columns

# --- UI 레이아웃 ---
st.markdown('<div class="header-box"><h1 style="color: #F1C40F;">플레이어</h1><p style="color: #F1C40F;">15,000원 배팅</p></div>', unsafe_allow_html=True)

# 기록판 표시 (가로 스크롤 가능하게)
cols_data = get_grid(st.session_state.history)
grid_ui = st.container()
with grid_ui:
    cols = st.columns(max(len(cols_data), 10)) # 최소 10열 확보
    for i, column_data in enumerate(cols_data):
        if i < len(cols):
            with cols[i]:
                for item in column_data:
                    color = "#E74C3C" if item == "B" else "#3498DB"
                    st.markdown(f'<div class="circle" style="background-color: {color};">{item}</div>', unsafe_allow_html=True)

st.write("---")

# 메인 버튼 (가로 배치)
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    st.markdown('<div class="player-btn">', unsafe_allow_html=True)
    if st.button("플레이어"):
        st.session_state.history.append("P")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with btn_col2:
    st.markdown('<div class="banker-btn">', unsafe_allow_html=True)
    if st.button("뱅커"):
        st.session_state.history.append("B")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 하단 기능바
st.write("")
low_col1, low_col2, low_col3 = st.columns([1, 1, 2])
with low_col1:
    if st.button("📸"): # 카메라 버튼 (기능은 추후 구현)
        st.info("카메라 기능을 준비 중입니다.")
with low_col2:
    if st.button("취소"):
        if st.session_state.history:
            st.session_state.history.pop()
            st.rerun()
with low_col3:
    if st.button("리셋"):
        st.session_state.history = []
        st.rerun()
