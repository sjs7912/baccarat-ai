import streamlit as st

# 1. 페이지 설정 (가장 상단 필수)
st.set_page_config(page_title="바카라 분석기", layout="centered")

# 2. 데이터 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 드래곤 꺾기 로직 (6행 고정 테이블 방식)
def get_clean_grid(history):
    # 6행 x 30열 빈 그리드 생성
    grid = [["" for _ in range(30)] for _ in range(6)]
    curr_col = 0
    curr_row = 0
    last_res = None

    for res in history:
        if last_res is not None and res != last_res:
            # 결과가 바뀌면 다음 열의 첫 번째 행으로 이동
            curr_col += 1
            curr_row = 0
            # 이미 데이터가 있는 열이라면 빈 열을 찾을 때까지 이동
            while any(grid[0][curr_col] != "" for _ in range(1)):
                curr_col += 1
        
        # 6번째 데이터(인덱스 5)부터는 행을 고정하고 열을 오른쪽으로 이동
        if curr_row >= 5:
            target_row = 5
            target_col = curr_col + (curr_row - 5)
        else:
            target_row = curr_row
            target_col = curr_col
        
        # 그리드 범위 내에 있을 때만 입력
        if target_col < 30:
            grid[target_row][target_col] = res
            
        curr_row += 1
        last_res = res
        
    return grid

# --- UI 레이아웃 (디자인) ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    .display-box {
        border: 3px solid #F1C40F; border-radius: 15px;
        padding: 30px; text-align: center; background-color: #1E1E1E;
        margin-bottom: 20px;
    }
    .road-map-container {
        background-color: white; border-radius: 10px;
        padding: 10px; overflow-x: auto; margin-bottom: 20px;
    }
    .baccarat-table { border-collapse: collapse; }
    .baccarat-td { 
        width: 28px; height: 28px; border: 1px solid #f0f0f0; 
        text-align: center; vertical-align: middle; 
    }
    .circle-dot {
        width: 22px; height: 22px; border-radius: 50%;
        display: inline-block; line-height: 22px;
        color: white; font-size: 10px; font-weight: bold;
    }
    </style>
""", unsafe_allow_value=True)

# [상단] 추천 전광판
st.markdown("""
    <div class="display-box">
        <h1 style="color: white; margin: 0; font-size: 40px;">플레이어</h1>
        <p style="color: #F1C40F; font-size: 20px; font-weight: bold;">15,000원 배팅</p>
    </div>
""", unsafe_allow_html=True)

# [중앙] 기록판 (드래곤 꺾기 적용)
grid_data = get_clean_grid(st.session_state.history)
html_table = '<div class="road-map-container"><table class="baccarat-table">'
for r in range(6):
    html_table += '<tr>'
    for c in range(25): # 25열까지 표시
        val = grid_data[r][c]
        if val == "B":
            content = '<div class="circle-dot" style="background-color: #FF4B4B;">B</div>'
        elif val == "P":
            content = '<div class="circle-dot" style="background-color: #007BFF;">P</div>'
        else:
            content = ""
        html_table += f'<td class="baccarat-td">{content}</td>'
    html_table += '</tr>'
html_table += '</table></div>'
st.markdown(html_table, unsafe_allow_html=True)

# [하단] 조작 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 플레이어 (PLAYER)", use_container_width=True):
        st.session_state.history.append("P")
        st.rerun()
with col2:
    if st.button("🔴 뱅커 (BANKER)", use_container_width=True):
        st.session_state.history.append("B")
        st.rerun()

st.divider()

# [기능] 카메라, 취소, 리셋
f1, f2, f3 = st.columns(3)
with f1:
    if st.button("📷 카메라", use_container_width=True): st.toast("준비 중")
with f2:
    if st.button("↩️ 취소", use_container_width=True):
        if st.session_state.history: st.session_state.history.pop(); st.rerun()
with f3:
    if st.button("♻️ 리셋", use_container_width=True):
        st.session_state.history = []
        st.rerun()
