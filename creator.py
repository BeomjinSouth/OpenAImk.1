from openai import OpenAI
import streamlit as st
from typing import List, Dict

# Streamlit 페이지 설정
st.set_page_config(
    page_title="세부능력 특기사항 생성기",
    page_icon="📚",
    layout="wide"
)

def generate_assessments(school_type: str, grade: int, subject: str, content: str, achievement: str) -> Dict[str, List[str]]:
    """각 성취수준별 세부능력 특기사항을 생성합니다."""
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    levels = {
        "최상": "상위 5% 수준",
        "상": "상위 6~30% 수준",
        "중": "상위 31~70% 수준",
        "하": "상위 71~90% 수준",
        "최하": "상위 91~100% 수준"
    }
    
    try:
        prompt = f"""
{school_type} {grade}학년 {subject} 과목의 '{content}' 단원에 대해 학생의 성취수준이 '{achievement}'일 때,
각각의 성취수준(최상/상/중/하/최하)에 해당하는 세부능력 특기사항을 2개씩 작성해주세요.

각 수준별 정의:
- 최상: 상위 5% 수준
- 상: 상위 6~30% 수준
- 중: 상위 31~70% 수준
- 하: 상위 71~90% 수준
- 최하: 상위 91~100% 수준

요구사항:
1. 각 수준마다 2개의 다른 문장을 작성
2. 구체적이고 객관적인 표현 사용
3. 학생의 실제 수행 과정과 결과를 포함
4. 부정적인 표현보다는 발전 가능성을 제시
5. 교육적인 언어 사용
6. 각 문장은 100자 내외로 작성

형식:
최상-1: [문장1]
최상-2: [문장2]
상-1: [문장1]
...처럼 각 수준별로 두 개의 문장을 작성해주세요.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 학생 평가 전문가입니다. 교육적이고 발전적인 관점에서 학생을 평가합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # 응답 텍스트를 줄바꿈으로 분리
        lines = response.choices[0].message.content.strip().split('\n')
        
        # 결과를 성취수준별로 정리
        results = {level: [] for level in levels.keys()}
        current_level = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            for level in levels.keys():
                if line.startswith(f"{level}-"):
                    current_level = level
                    comment = line.split(":", 1)[1].strip()
                    results[current_level].append(comment)
                    break
        
        return results
    
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        return {}

def main():
    st.title("📚 세부능력 특기사항 생성기")
    st.markdown("---")
    
    # 입력 섹션
    col1, col2, col3 = st.columns(3)
    
    with col1:
        school_type = st.selectbox(
            "학교급",
            options=["중학교", "고등학교"]
        )
        
        grade = st.selectbox(
            "학년",
            options=[1, 2, 3]
        )
    
    with col2:
        subject = st.text_input("과목명")
        content = st.text_input("학습 내용")
    
    with col3:
        achievement = st.text_input("현재 성취수준")
    
    if st.button("세부능력 특기사항 생성"):
        if not all([subject, content, achievement]):
            st.warning("모든 필드를 입력해주세요!")
            return
        
        with st.spinner("세부능력 특기사항을 생성중입니다..."):
            results = generate_assessments(school_type, grade, subject, content, achievement)
            
            if results:
                st.success("생성 완료!")
                
                # 결과 표시
                for level, comments in results.items():
                    with st.expander(f"▶ {level} 수준 평가"):
                        for i, comment in enumerate(comments, 1):
                            st.write(f"{i}. {comment}")
                
                # 전체 복사를 위한 텍스트 생성
                all_comments = []
                for level, comments in results.items():
                    all_comments.append(f"【 {level} 수준 】")
                    for i, comment in enumerate(comments, 1):
                        all_comments.append(f"{i}. {comment}")
                    all_comments.append("")  # 빈 줄 추가
                
                st.markdown("### 전체 복사")
                st.code("\n".join(all_comments), language="text")

if __name__ == "__main__":
    main()
