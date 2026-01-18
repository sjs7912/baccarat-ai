import streamlit as st

# 1. 화면 설정 (에러 방지를 위해 가장 먼저 실행)
st.set_page_config(page_title="바카라 분석기", layout="centered")

# 2. 데이터 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 바카라 꺾기 로직 (5칸 기준)
def get_main_road(history):
    columns = [[]]
    c_idx = 0
    for i, res in enumerate(history):
        if i > 0 and res != history[i-1]: # 결과 바뀌면 새 줄
            c_idx += 1
            columns.append([])
        elif len(columns[c_idx]) >= 5: # 5칸 차면 옆으로 꺾기
            c_idx += 1
            columns.append([])
        columns[c_idx].append(res)
    return columns

# --- UI 시작 (사진 디자인 반영) ---

# 상단 노란색 전광판 영역
st.error("### 플레이어 \n\n 15,000원 배팅") # 임시로 붉은 계열 박스 사용 (에러 방지용 안전 설계)

# 기록판 (출목표)
st.write("---")
road_data = get_main_road(st.session_state.history)
grid_cols = st.columns(15) # 최대 15열 표시
for i, column_data in enumerate(road_data):
    if i < 15:
        with grid_cols[i]:
            for item in column_data:
                icon = "🔴" if item == "B" else "🔵"
                st.write(icon)

st.write("---")

# 메인 버튼: 플레이어(좌) / 뱅커(우) 가로 배치
# 버튼 크기를 크게 하기 위해 use_container_width 사용
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("🔵 플레이어", use_container_width=True):
        st.session_state.history.append("P")
        st.rerun()
with btn_col2:
    if st.button("🔴 뱅커", use_container_width=True):
        st.session_state.history.append("B")
        st.rerun()

st.write("") # 간격 조절

# 하단 기능 버튼: 좌측 카메라 / 중앙 취소 / 우측 리셋
f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
with f_col1:
    if st.button("📸 카메라"):
        st.toast("카메라 기능 준비 중")
with f_col2:
    if st.button("↩️ 취소"):
        if st.session_state.history:
            st.session_state.history.pop()
            st.rerun()
with f_col3:
    if st.button("♻️ 리셋"):
        st.session_state.history = []
        st.rerun()
