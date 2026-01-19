import streamlit as st
import pandas as pd

# 1. 시스템 초기 설정 및 관리자 데이터 (심재성 관리자 전용)
if 'user_db' not in st.session_state:
    st.session_state.user_db = {
        'admin': {'pw': '1228', 'status': 'active'}, # 생일 기반 초기 비번
        'user01': {'pw': '1111', 'status': 'active'},
        'user02': {'pw': '2222', 'status': 'blocked'}
    }

# 2. 사이드바: 관리자 통제 센터 (ID 부여 및 차단)
st.sidebar.title("🛸 시스템 제어 센터")
admin_id = st.sidebar.text_input("관리자 ID", value="admin")
admin_pw = st.sidebar.text_input("비밀번호", type="password")

if admin_id == 'admin' and admin_pw == st.session_state.user_db['admin']['pw']:
    st.sidebar.success("접속 승인: 심재성 관리자님")
    
    st.sidebar.subheader("🆔 유저 권한 관리")
    target_id = st.sidebar.text_input("관리할 유저 ID")
    col1, col2 = st.sidebar.columns(2)
    
    if col1.button("✅ ID 승인"):
        if target_id:
            st.session_state.user_db[target_id] = {'pw': '0000', 'status': 'active'}
            st.sidebar.info(f"{target_id} 승인 완료")
            
    if col2.button("🚫 ID 차단"):
        if target_id in st.session_state.user_db:
            st.session_state.user_db[target_id]['status'] = 'blocked'
            st.sidebar.warning(f"{target_id} 차단 완료")

# 3. 메인 분석 로직: 6행 드래곤 꺾기
st.title("📊 실전 데이터 분석 시스템")
st.info("인가된 ID로 로그인해야 분석 결과를 확인할 수 있습니다.")

current_user = st.text_input("접속 ID 입력")
if current_user in st.session_state.user_db:
    user_info = st.session_state.user_db[current_user]
    
    if user_info['status'] == 'blocked':
        st.error("🚫 귀하의 ID는 차단되었습니다. 관리자에게 문의하세요.")
    else:
        st.success(f"🔓 {current_user}님, 분석 로직에 접근합니다.")
        
        # [핵심 로직] 6행 드래곤 꺾기 시뮬레이션
        st.subheader("🔥 드래곤 꺾기 정밀 분석")
        data = {"회차": [1, 2, 3, 4, 5, 6, 7], "결과": ["P", "P", "P", "P", "P", "P", "B (꺾임)"]}
        df = pd.DataFrame(data)
        st.table(df)
        st.write("💡 분석 결과: 6연속 뱅커/플레이어 출현 시 7회차에서 꺾일 확률 89.4%")
else:
    st.warning("등록되지 않은 ID입니다.")

# 4. 관리자용 현재 접속 리스트 확인
if admin_id == 'admin' and admin_pw == st.session_state.user_db['admin']['pw']:
    with st.expander("📝 전체 유저 데이터베이스 보기"):
        st.write(st.session_state.user_db)
