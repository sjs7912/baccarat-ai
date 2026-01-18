import streamlit as st

# [1] 전체 화면 설정 (스크롤 방지를 위한 슬림 모드)
st.set_page_config(page_title="분석기", layout="wide", initial_sidebar_state="collapsed")

# [2] 재성님 요청 디자인 (빨간색 깜빡임 + 한 화면 구성)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 축소 */
    .main { background-color: #0e1117; padding-top: 0rem; }
    .stApp { overflow: hidden; } /* 스크롤 방지 */
    
    /* 배팅 지시 박스 슬림화 */
    .bet-box {
        padding: 10px; border-radius: 15px; border: 3px solid #FFD700;
        text-align: center; margin-bottom: 5px; background-color: #1f2937;
    }
    .bet-label { color: #ccc; font-size: 14px; margin-bottom: -10px; }
    .bet-target { font-size: 45px; font-weight: 900; }
    
    /* 뱅커 깜빡임 효과 */
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    .blink-red { color: #ef4444; animation: blink 0.7s infinite; }
    .blue-text { color: #3b82f6; }
    
    /* 버튼 사이즈 최적화 */
    .stButton>button {
        height: 60px !important; font-size: 20px !important; border-radius: 10px;
    }
    
    /* 카메라 버튼 (작게 구석으로) */
    .camera-zone { position: fixed; top: 10px; right: 10px; z-index: 1000; width: 60px; }
    
    /* 점판 사이즈 축소 (가로형) */
    .board { display: flex; overflow-x: auto; gap: 4px; padding: 10px; background: white; border-radius: 10px; height: 160px; }
    </style>
    """, unsafe_allow_html=True)

# --- [3] 우측 상단 카메라 아이콘 ---
with st.container():
    st.markdown('<div class="camera-zone">', unsafe_allow_html=True)
    st.file_uploader("📸", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [4] AI 추천 (깜빡이 적용) ---
if len(st.session_state.history) > 0:
    추천 = "플레이어" if st.session_state.history[-1] == "B" else "뱅커"
    클래스 = "blue-text" if 추천 == "플레이어" else "blink-red"
    st.markdown(f'''
        <div class="bet-box">
            <div class="bet-label">AI 추천</div>
            <div class="bet-target {클래스}">{추천}</div>
            <div style="font-size:20px; color:#fbbf24; margin-top:-10px;">15,000원</div>
        </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('<div class="bet-box"><div class="bet-target" style="color:white; font-size:30px;">결과 입력</div></div>', unsafe_allow_html=True)

# --- [5] 수동 입력 (BP 큰 버튼) ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 플 (P)"): st.session_state.history.append("P"); st.rerun()
with col2:
    if st.button("🔴 뱅 (B)"): st.session_state.history.append("B"); st.rerun()

# --- [6] 가로 출목표 (옆으로 보게 정렬) ---
st.markdown('<div style="font-size:12px; color:white; margin-bottom:2px;">📊 최근 기록 (가로형)</div>', unsafe_allow_html=True)
if st.session_state.history:
    # 6행 정렬
    rows = [st.session_state.history[i:i + 6] for i in range(0, len(st.session_state.history), 6)]
    board_html = '<div class="board">'
    for row in rows:
        board_html += '<div style="display:flex; flex-direction:column; gap:2px;">'
        for item in row:
            bg = "#3b82f6" if item == "P" else "#ef4444"
            board_html += f'<div style="width:22px; height:22px; border-radius:50%; background:{bg}; color:white; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px;">{item}</div>'
        for _ in range(6 - len(row)):
            board_html += '<div style="width:22px; height:22px; border:1px solid #eee; border-radius:50%;"></div>'
        board_html += '</div>'
    st.markdown(board_html + '</div>', unsafe_allow_html=True)

# --- [7] 하단 관리 (더 작게) ---
c1, c2, c3 = st.columns([1,1,1])
with c1:
    if st.button("🔄취소"):
        if st.session_state.history: st.session_state.history.pop(); st.rerun()
with c2:
    if st.button("❌초기화"): st.session_state.history = []; st.rerun()
with c3:
    if st.button("⚙️설정"): st.write("설정창")
