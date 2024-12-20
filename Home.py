import streamlit as st

st.set_page_config(
    page_title="교사 업무 지원 시스템",
    page_icon="📚",
    layout="wide"
)

st.title("📚 교사 업무 지원 시스템")
st.markdown("---")

st.markdown("""
### 사용 가능한 기능

1. **📝 문장 변형기**
   - 입력한 문장을 다양한 형태로 변형
   - 의미는 유지하면서 다른 표현으로 변환
   - 사이드바에서 OpenAI API 키 입력 필요

2. **✍️ 생기부 작성기**
   - 학교급/학년/과목/내용/성취수준 기반 세부능력 특기사항 생성
   - 5단계 수준별 평가 문구 생성
   - 교육적이고 발전적인 서술 제공

### 사용 방법
1. 왼쪽 사이드바의 페이지 목록에서 원하는 기능 선택
2. 각 페이지의 안내에 따라 필요한 정보 입력
3. 결과 확인 및 활용

### 주의사항
- OpenAI API 키가 필요합니다
- API 사용량에 따라 비용이 발생할 수 있습니다
- 생성된 내용은 참고용으로만 사용하시기 바랍니다
""")
