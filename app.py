import streamlit as st
import numpy as np
from PIL import Image

# 1. 앱 최상단 설정 (아이폰 홈 화면 아이콘 및 타이틀)
st.set_page_config(
    page_title="AI Baccarat Master",
    page_icon="🎰", # 사파리 홈 화면 추가 시 아이콘으로 표시됨
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 보안 스크립트 (우클릭 및 복사 방지)
st.markdown("""
    <script>
    document.addEventListener('contextmenu', event => event.preventDefault());
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && (e.key === 'c' || e.key === 'v' || e.key === 'u' || e.key === 's')) {
            event.preventDefault();
        }
    });
    </script>
    <style>
    @keyframes blink { 0% {opacity: 1;} 50% {opacity: 0.1;} 100% {opacity: 1;} }
    .blink-red { background-color: #ff4b4b !important; animation: blink 0.8s infinite; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; }
    .blink-blue { background-color: #1c83e1 !important; animation: blink 0.8s infinite; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; }
    .bead { width: 35px; height: 35px; border-radius: 50%; display: inline-block; text-align: center; line-height: 35px; font-weight: bold; color: white; margin: 3px; border: 2px solid #fff; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 3. 사용자 및 시스템 데이터베이스 초기화
if 'user_db' not in st.session_state:
    # 아이디: [비밀번호, 활성화여부]
    st.session_state.user_db = {"admin": ["admin1234", True]} 
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'history' not in st.session_state: st.session_state.history = []
if 'step' not in st.session_state: st.session_state.step = 0
if 'pair_loss' not in st.session_state: st.session_state.pair_loss = 0

# 4. 로그인 로직
if st.session_state.logged_in_user is None:
    st.title("🔐 AI Baccarat Master 접속")
    u_id = st.text_input("아이디")
    u_pw = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if u_id in st.session_state.user_db:
            pw, active = st.session_state.user_db[u_id]
            if pw == u_pw and active:
                st.session_state.logged_in_user = u_id
                st.rerun()
            elif not active: st.error("차단된 계정입니다.")
            else: st.error("비밀번호 오류")
        else: st.error("아이디가 없습니다.")
    st.stop()

# 5. 관리자 전용 사이드바 (사용자 차단/해제)
if st.session_state.logged_in_user == "admin":
    with st.sidebar.expander("🛠️ 관리자 패널"):
        new_id = st.text_input("신규 ID")
        new_pw = st.text_input("신규 PW")
        if st.button("사용자 생성"):
            st.session_state.user_db[new_id] = [new_pw, True]
        st.divider()
        for uid in list(st.session_state.user_db.keys()):
            if uid == "admin": continue
            status = "🟢" if st.session_state.user_db[uid][1] else "🔴"
            if st.button(f"{status} {uid} 권한전환"):
                st.session_state.user_db[uid][1] = not st.session_state.user_db[uid][1]
                st.rerun()

# 6. 이미지 인식 및 배팅 로직
st.sidebar.header("📷 화면 스캔")
uploaded_file = st.sidebar.file_uploader("출목표 캡처 업로드", type=["jpg","png"])
unit_money = st.sidebar.number_input("1유닛 금액", value=10000, step=5000)

# AI 확률 계산 (전체 30% + 최근 70%)
def get_ai_pred(hist):
    if len(hist) < 3: return None
    b_rate = hist.count('B') / len(hist)
    r_b_rate = hist[-5:].count('B') / len(hist[-5:])
    score = (b_rate * 0.3) + (r_b_rate * 0.7)
    if score > 0.75: return 'P'
    if score < 0.25: return 'B'
    return 'B' if score <= 0.5 else 'P'

# 배팅액 계산 (1-3-2-6 + 페어 복구)
units = [1, 3, 2, 6]
curr_u = units[st.session_state.step]
pair_fixed = 5000
raw_bet = (unit_money * curr_u) + st.session_state.pair_loss
main_bet_display = int((raw_bet + 4999) // 5000) * 5000

pred = get_ai_pred(st.session_state.history)

# 7. 메인 UI
st.title("🎰 AI 실시간 전략 지시")
c1, c2, c3 = st.columns([1.5, 1, 1])

with c1:
    if pred == 'B': st.markdown(f'<div class="blink-red">BANKER 배팅<br>{main_bet_display:,}원</div>', unsafe_allow_html=True)
    elif pred == 'P': st.markdown(f'<div class="blink-blue">PLAYER 배팅<br>{main_bet_display:,}원</div>', unsafe_allow_html=True)
    else: st.info("데이터를 입력하세요.")

with c2:
    st.metric("💎 페어 배팅", "5,000원")
    st.caption(f"누적 복구액: {st.session_state.pair_loss:,}원")

with c3:
    st.metric("📈 단계", f"{st.session_state.step + 1}/4")
    if st.button("로그아웃"): 
        st.session_state.logged_in_user = None
        st.rerun()

# 8. 결과 입력 버튼
st.divider()
st.subheader("🎲 결과 체크")
b1, b2, b3 = st.columns(3)
def record_res(r):
    st.session_state.pair_loss += pair_fixed
    if pred == r:
        st.session_state.step = (st.session_state.step + 1) % 4
        st.session_state.pair_loss = 0
    else: st.session_state.step = 0
    st.session_state.history.append(r)

if b1.button("🔵 PLAYER", use_container_width=True): record_res('P'); st.rerun()
if b2.button("🔴 BANKER", use_container_width=True): record_res('B'); st.rerun()
if b3.button("🟢 TIE", use_container_width=True): st.session_state.history.append('T'); st.rerun()

# 9. 그림판 표시
st.divider()
if st.session_state.history:
    html = "".join([f'<div class="bead" style="background-color:{"red" if r=="B" else "blue" if r=="P" else "green"};">{r}</div>' for r in st.session_state.history])
    st.markdown(html, unsafe_allow_html=True)
