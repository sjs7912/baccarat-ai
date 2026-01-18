import streamlit as st

# 1. 페이지 설정 및 다크 테마 기본값
st.set_page_config(page_title="바카라 분석기", layout="centered")

# 2. 사진 속 UI와 똑같이 만들기 위한 스타일 시트
st.markdown("""
    <style>
    /* 배경색 및 폰트 설정 */
    .stApp { background-color: #0F1117; }
    
    /* 상단 노란색 테두리 박스 */
    .header-container {
        border: 2px solid #F1C40F;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        background-color: #1A1C23;
        margin-bottom: 20px;
    }
    .header-main { color: white; font-size: 50px; font-weight: bold; margin: 0; }
    .header-sub { color: #F1C40F; font-size: 22px; margin-top: 10px; }

    /* 기록지(흰색 박스) */
    .road-map {
        background-color: white;
        border-radius: 15px;
        min-height: 180px;
        padding: 15px;
        display: flex;
        flex-direction: row;
        margin-bottom: 30px;
        overflow-x: auto;
    }
    .grid-col { display: flex; flex-direction: column; width: 32px; }
    .circle {
        width: 26px; height: 26px; border-radius: 50%;
        margin: 3px; display: flex; align-items: center;
        justify-content: center; font-size: 11px; color: white; font-weight: bold;
    }

    /* 버튼 스타일 조정 */
    div.stButton > button {
        height: 100px !important;
        border-radius: 15px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
    }
    /* 플레이어 버튼 (파란색) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background-color: #2E5BFF !important;
    }
    /* 뱅커 버튼 (빨간색) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #FF4B4B !important;
    }
    
    /* 하단 보조 버튼 스타일 */
    .bottom-btns button { height: 50px !important; font-size: 16px !important; background-color: #2D2F36 !important; }
    </style>
""", unsafe_allow_value=True)

# 3. 데이터 로직
if 'history' not in st.session_state:
    st.session_state.history = []

def get_logic(history):
    cols = [[]]; c_idx = 0
    for i, res in enumerate(history):
        if i > 0 and res != history[i-1]: c_idx += 1; cols.append([])
        elif len(cols[c_idx]) >= 5: c_idx += 1; cols.append([])
        cols[c_idx].append(res)
    return cols

# --- UI 그리기 ---

# 상단 영역
st.markdown(f'''
    <div class="header-container">
        <p class="header-main">플레이어</p>
        <p class="header-sub">15,000원 배팅</p>
    </div>
''', unsafe_allow_html=True)

# 기록지 영역
road_data = get_logic(st.session_state.history)
html_road = '<div class="road-map">'
for col in road_data:
    html_road += '<div class="grid-col">'
    for item in col:
        color = "#FF4B4B" if item == "B" else "#2E5BFF"
        html_road += f'<div class="circle" style="background-color: {color};">{item}</div>'
    html_road += '</div>'
html_road += '</div>'
st.markdown(html_road, unsafe_allow_html=True)

# 메인 버튼 (가로 배치)
col1, col2 = st.columns(2)
with col1:
    if st.button("● 플레이어", key="p_btn"):
        st.session_state.history.append("P"); st.rerun()
with col2:
    if st.button("● 뱅커", key="b_btn"):
        st.session_state.history.append("B"); st.rerun()

# 하단 버튼 (카메라, 취소, 리셋)
st.markdown('<div class="bottom-btns">', unsafe_allow_html=True)
b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
with b_col1:
    if st.button("📸 카메라"): st.toast("준비 중")
with b_col2:
    if st.button("↩️ 취소"):
        if st.session_state.history: st.session_state.history.pop(); st.rerun()
with b_col3:
    if st.button("♻️ 리셋"):
        st.session_state.history = []; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
