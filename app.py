import streamlit as st

# 1. 화면 기본 설정
st.set_page_config(page_title="바카라 분석기", layout="wide")

# 2. 데이터 저장소 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 분석 로직: 5칸 기준 꺾기 구현
def get_baccarat_grid(history):
    columns = [[]]
    curr_col = 0
    for i, res in enumerate(history):
        if i > 0 and res != history[i-1]:  # 결과가 바뀌면 새 열
            curr_col += 1
            columns.append([])
        elif len(columns[curr_col]) >= 5:  # 5칸 다 차면 옆으로 꺾기
            curr_col += 1
            columns.append([])
        columns[curr_col].append(res)
    return columns

# --- UI 시작 ---
st.title("🎰 바카라 실시간 분석기")

# 상단 추천 영역
st.info("💡 추천 베팅: 플레이어 (15,000원)")

# 기록판 영역 (꺾기 로직 반영)
grid_data = get_baccarat_grid(st.session_state.history)
st.write("### 실시간 출목표")
cols = st.columns(max(len(grid_data), 12))
for i, column_data in enumerate(grid_data):
    if i < len(cols):
        with cols[i]:
            for item in column_data:
                color = "red" if item == "B" else "blue"
                st.markdown(f":{color}[● {item}]")

st.divider()

# 메인 조작 버튼 (가로 배치 & 크게)
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("🔵 플레이어 (PLAYER)", use_container_width=True):
        st.session_state.history.append("P")
        st.rerun()

with btn_col2:
    if st.button("🔴 뱅커 (BANKER)", use_container_width=True):
        st.session_state.history.append("B")
        st.rerun()

# 하단 기능 버튼 (카메라, 취소, 리셋)
st.write("")
f_col1, f_col2, f_col3 = st.columns([1, 1, 2])
with f_col1:
    if st.button("📸 카메라", help="카드 인식 준비 중"):
        st.toast("카메라 기능은 현재 개발 중입니다.")
with f_col2:
    if st.button("↩️ 취소"):
        if st.session_state.history:
            st.session_state.history.pop()
            st.rerun()
with f_col3:
    if st.button("♻️ 전체 리셋"):
        st.session_state.history = []
        st.rerun()
