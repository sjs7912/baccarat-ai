
import streamlit as st

# [1] 화면 설정
st.set_page_config(page_title="AI 바카라 분석기", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .bet-box {
        background-color: #1f2937;
        padding: 30px;
        border-radius: 20px;
        border: 5px solid #FFD700;
        text-align: center;
        margin-bottom: 25px;
    }
    .bet-target { font-size: 65px; font-weight: 900; margin-bottom: 10px; }
    .p-text { color: #3b82f6; } 
    .b-text { color: #ef4444; } 
    .stButton>button {
        width: 100%; height: 100px; font-size: 30px !important; font-weight: bold !important; border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎰 AI 실시간 전략 지시")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- [2] 배팅 지시 (한글 크게!) ---
st.divider()
if len(st.session_state.history) > 0:
    추천 = "플레이어" if st.session_state.history[-1] == "B" else "뱅커"
    색상 = "p-text" if 추천 == "플레이어" else "b-text"
    st.markdown(f'<div class="bet-box"><div style="color:white; font-size:25px;">📢 다음 추천 배팅</div><div class="bet-target {색상}">{추천} ({"P" if 추천=="플레이어" else "B"})</div><div style="font-size:35px; color:#fbbf24;">금액: 15,000원</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="bet-box"><div class="bet-target" style="color:white; font-size:35px;">결과를 입력해주세요</div></div>', unsafe_allow_html=True)

# --- [3] 카메라 스캔 기능 ---
st.subheader("📸 화면 스캔 (카메라)")
st.file_uploader("사진을 찍거나 업로드하세요", type=['png', 'jpg', 'jpeg'])

# --- [4] 입력 버튼 (BP 중심) ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 플레이어 (P)"):
        st.session_state.history.append("P"); st.rerun()
with col2:
    if st.button("🔴 뱅커 (B)"):
        st.session_state.history.append("B"); st.rerun()

# --- [5] 바카라 출목표 (6행 정렬) ---
st.divider()
if st.session_state.history:
    rows = [st.session_state.history[i:i + 6] for i in range(0, len(st.session_state.history), 6)]
    html_code = "<div style='display: flex; overflow-x: auto; gap: 10px; padding: 20px; background: white; border-radius: 15px;'>"
    for row in rows:
        html_code += "<div style='display: flex; flex-direction: column; gap: 6px;'>"
        for item in row:
            bg = "#3b82f6" if item == "P" else "#ef4444"
            html_code += f"<div style='width: 45px; height: 45px; border-radius: 50%; background:{bg}; color:white; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:20px;'>{item}</div>"
        for _ in range(6 - len(row)):
            html_code += "<div style='width: 45px; height: 45px; border:1px solid #ddd; border-radius:50%;'></div>"
        html_code += "</div>"
    st.markdown(html_code + "</div>", unsafe_allow_html=True)

# --- [6] 초기화 메뉴 ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 한 칸 지우기"):
        if st.session_state.history: st.session_state.history.pop(); st.rerun()
with c2:
    if st.button("❌ 전체 초기화"):
        st.session_state.history = []; st.rerun()
