import streamlit as st

# [1] 설정: 메뉴 숨기기 및 스크롤 완전 차단
st.set_page_config(page_title="분석기", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* 전체 화면 스크롤 금지 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        background-color: #0e1117;
    }
    
    /* 영어 메뉴 및 헤더 제거 */
    header, #MainMenu, footer { visibility: hidden !important; }

    /* 추천 박스 디자인 */
    .bet-box {
        text-align: center; border: 2px solid #FFD700; 
        border-radius: 10px; padding: 5px; margin-bottom: 5px; background: #1f2937;
    }
    
    /* 뱅커 추천 시 빨간색 깜빡임 */
    @keyframes blinker { 50% { opacity: 0; } }
    .blink-red { color: #ff4b4b !important; font-weight: 900; animation: blinker 0.6s linear infinite; }
    .blue-text { color: #3b82f6 !important; font-weight: 900; }

    /* 버튼 높이 최적화 (좌우 배치용) */
    .stButton>button {
        height: 60px !important; font-size: 20px !important; border-radius: 10px;
    }
    
    /* 출목표 (가로형 정판 스타일) */
    .board-frame {
        display: flex; flex-direction: row; overflow-x: auto; 
        background: white; border-radius: 5px; padding: 5px; height: 130px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [2] AI 배팅 추천 (뱅커 깜빡이) ---
if st.session_state.history:
    추천 = "플레이어" if st.session_state.history[-1] == "B" else "뱅커"
    스타일 = "blue-text" if 추천 == "플레이어" else "blink-red"
    st.markdown(f'''
        <div class="bet-box">
            <div style="color:white; font-size:12px;">AI 추천</div>
            <div style="font-size:38px;" class="{스타일}">{추천}</div>
            <div style="color:#fbbf24; font-size:18px;">15,000원</div>
        </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('<div class="bet-box"><div style="font-size:25px; color:white; padding:10px;">데이터를 입력하세요</div></div>', unsafe_allow_html=True)

# --- [3] 결과 입력 버튼 (좌우 배치) ---
col_p, col_b = st.columns(2)
with col_p:
    if st.button("🔵 플레이어"): st.session_state.history.append("P"); st.rerun()
with col_b:
    if st.button("🔴 뱅커"): st.session_state.history.append("B"); st.rerun()

# --- [4] 바카라 출목표 (가로형) ---
st.markdown('<div style="font-size:11px; color:gray; margin-top:5px;">📊 실시간 출목표</div>', unsafe_allow_html=True)
if st.session_state.history:
    groups = [st.session_state.history[i:i+6] for i in range(0, len(st.session_state.history), 6)]
    html = '<div class="board-frame">'
    for group in groups:
        html += '<div style="display:flex; flex-direction:column; margin-right:3px;">'
        for item in group:
            color = "#3b82f6" if item == "P" else "#ff4b4b"
            html += f'<div style="width:18px; height:18px; border-radius:50%; background:{color}; color:white; font-size:9px; display:flex; align-items:center; justify-content:center; margin-bottom:1px;">{item}</div>'
        for _ in range(6 - len(group)):
            html += '<div style="width:18px; height:18px; border:1px solid #ddd; border-radius:50%; margin-bottom:1px;"></div>'
        html += '</div>'
    st.markdown(html + '</div>', unsafe_allow_html=True)

# --- [5] 하단 메뉴 (왼쪽 카메라 / 취소 / 리셋) ---
st.divider()
bot1, bot2, bot3 = st.columns([1, 1, 1])
with bot1:
    # 왼쪽 하단 카메라 버튼
    st.file_uploader("📸", type=['jpg','png'], label_visibility="collapsed")
with bot2:
    if st.button("🔄 취소"): 
        if st.session_state.history: st.session_state.history.pop(); st.rerun()
with bot3:
    if st.button("❌ 리셋"): st.session_state.history = []; st.rerun()
