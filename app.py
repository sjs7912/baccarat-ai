import streamlit as st

# [1] 설정: 메뉴 숨기기 및 스크롤 완전 차단
st.set_page_config(page_title="분석기", layout="wide")

st.markdown("""
    <style>
    /* 전체 화면 스크롤 금지 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        background-color: #0e1117;
    }
    
    header, #MainMenu, footer { visibility: hidden !important; }
    .stDeployButton { display: none !important; }

    /* 배경 깜빡이 애니메이션 */
    @keyframes blink-red { 0%, 100% { background-color: #0e1117; } 50% { background-color: #8b0000; } }
    @keyframes blink-blue { 0%, 100% { background-color: #0e1117; } 50% { background-color: #00008b; } }
    
    .bg-red { animation: blink-red 0.6s infinite; }
    .bg-blue { animation: blink-blue 0.6s infinite; }

    /* 추천 박스 */
    .bet-box {
        text-align: center; border: 3px solid #FFD700; 
        border-radius: 15px; padding: 15px; background: rgba(31, 41, 55, 0.8);
    }

    /* 버튼 크기 */
    .stButton>button { height: 75px !important; font-size: 24px !important; font-weight: bold; }
    
    /* 정식 출목표 스타일 */
    .baccarat-board {
        display: flex; flex-direction: row; overflow-x: auto; 
        background: white; border-radius: 8px; padding: 5px; height: 140px; gap: 3px;
    }
    .board-col { display: flex; flex-direction: column; gap: 2px; }

    /* 카메라 버튼 */
    .fixed-cam {
        position: fixed; bottom: 20px; right: 20px; z-index: 9999;
        background: #333; border-radius: 50%; width: 60px; height: 60px;
        display: flex; align-items: center; justify-content: center; border: 2px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [2] 추천 및 배경 깜빡이 제어 ---
if st.session_state.history:
    추천 = "플레이어" if st.session_state.history[-1] == "B" else "뱅커"
    bg_style = "bg-blue" if 추천 == "플레이어" else "bg-red"
    # 화면 전체에 깜빡이 효과 주입
    st.markdown(f'<div class="{bg_style}" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1;"></div>', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="bet-box">
            <div style="font-size:50px; color:white; font-weight:900;">{추천}</div>
            <div style="color:#fbbf24; font-size:22px;">15,000원 배팅</div>
        </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('<div class="bet-box"><div style="font-size:25px; color:white;">데이터 입력 대기</div></div>', unsafe_allow_html=True)

# --- [3] 정식 출목표 로직 ---
if st.session_state.history:
    columns = []
    current_col = [st.session_state.history[0]]
    for i in range(1, len(st.session_state.history)):
        if st.session_state.history[i] == st.session_state.history[i-1] and len(current_col) < 6:
            current_col.append(st.session_state.history[i])
        else:
            columns.append(current_col)
            current_col = [st.session_state.history[i]]
    columns.append(current_col)
    
    board_html = '<div class="baccarat-board">'
    for col in columns:
        board_html += '<div class="board-col">'
        for item in col:
            c = "#3b82f6" if item == "P" else "#ff4b4b"
            board_html += f'<div style="width:18px; height:18px; border-radius:50%; background:{c}; color:white; font-size:9px; display:flex; align-items:center; justify-content:center;">{item}</div>'
        for _ in range(6 - len(col)):
            board_html += '<div style="width:18px; height:18px; border:1px solid #eee; border-radius:50%;"></div>'
        board_html += '</div>'
    st.markdown(board_html + '</div>', unsafe_allow_html=True)

# --- [4] 좌우 버튼 및 하단 메뉴 ---
st.write("")
col_p, col_b = st.columns(2)
with col_p:
    if st.button("🔵 플레이어"): st.session_state.history.append("P"); st.rerun()
with col_b:
    if st.button("🔴 뱅커"): st.session_state.history.append("B"); st.rerun()

st.write("")
c1, c2, _ = st.columns([1, 1, 1.5])
with c1:
    if st.button("🔄 취소"): 
        if st.session_state.history: st.session_state.history.pop(); st.rerun()
with c2:
    if st.button("❌ 리셋"): st.session_state.history = []; st.rerun()

st.markdown('<div class="fixed-cam">', unsafe_allow_html=True)
st.file_uploader("📸", type=['jpg','png'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
