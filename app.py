import streamlit as st

# 1. 시스템 설정 (에러 방지를 위해 최상단 고정)
st.set_page_config(page_title="바카라 분석기", layout="centered")

# 2. 데이터 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 드래곤 꺾기 핵심 로직 (6행 테이블 기반)
def get_baccarat_road(history):
    # 6행 x 40열의 빈 판 생성
    grid = [["" for _ in range(40)] for _ in range(6)]
    curr_col = 0
    curr_row = 0
    last_res = None

    for res in history:
        if last_res is not None and res != last_res:
            # 결과가 바뀌면 다음 '빈 열'의 첫 번째 칸으로 이동
            curr_col += 1
            curr_row = 0
            while any(grid[0][curr_col] != "" for _ in range(1)):
                curr_col += 1
        
        # 위치 계산 (5행부터는 오른쪽으로 꺾음)
        if curr_row >= 5:
            target_row = 5
            target_col = curr_col + (curr_row - 5)
        else:
            target_row = curr_row
            target_col = curr_col
        
        # 범위 내 입력
        if target_col < 40:
            grid[target_row][target_col] = res
            
        curr_row += 1
        last_res = res
    return grid

# --- UI 구성 ---

# 상단 알림 (에러가 가장 적은 st.info 사용)
st.info("### 💡 추천 베팅: 플레이어 (15,000원)")

# 출목표 출력 (안전한 표준 표 방식)
st.write("#### 실시간 기록지 (꺾기 적용)")
grid_data = get_baccarat_road(st.session_state.history)

# 드래곤 꺾기 시각화 (이모지 사용으로 에러 방지)
for r in range(6):
    row_str = ""
    for c in range(20): # 화면 크기상 20열까지 표시
        val = grid_data[r][c]
        if val == "B": row_str += "🔴 "
        elif val == "P": row_str += "🔵 "
        else: row_str += "⚪ " # 빈칸
    st.text(row_str)

st.divider()

# 메인 조작 버튼 (가로 배치)
col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 플레이어 클릭", use_container_width=True):
        st.session_state.history.append("P")
        st.rerun()
with col2:
    if st.button("🔴 뱅커 클릭", use_container_width=True):
        st.session_state.history.append("B")
        st.rerun()

# 하단 기능 버튼
st.write(" ")
f1, f2, f3 = st.columns(3)
with f1:
    if st.button("📷 카메라"):
        st.toast("카메라 기능 준비 중")
with f2:
    if st.button("↩️ 취소"):
        if st.session_state.history:
            st.session_state.history.pop()
            st.rerun()
with f3:
    if st.button("♻️ 리셋"):
        st.session_state.history = []
        st.rerun()
