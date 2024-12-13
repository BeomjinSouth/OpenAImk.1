from openai import OpenAI
import streamlit as st
from typing import List, Dict, Tuple

# Streamlit 페이지 설정
st.set_page_config(
    page_title="세부능력 특기사항 생성기",
    page_icon="📚",
    layout="wide"
)

system_content = """당신은 학생평가 전문가이자 생활기록부 작성 전문가입니다.

## 작성 원칙
1. 기본 서술 방향
    - 긍정적 서술을 기본으로 함
    - 성취도가 낮은 경우 '참여함', '수행함', '해결함' 등 중립적 표현 사용
    - 부정적 표현 대신 발전 가능성과 성장 과정을 기술

2. 문장 구조
    - 주어('학생은', '위 학생은' 등) 생략
    - '~했음', '~함', '~하였음' 등의 어미 사용
    - '~습니다', '~입니다' 등의 종결어미 사용 금지

3. 내용 구성
    - 각 문장은 80-100자 내외로 작성
    - 구체적인 학습 활동과 과정 중심으로 기술
    - 문제해결 과정과 사고력 발현 과정을 상세히 서술
    - 단원별 특징적인 활동과 성과를 개별적으로 기술
    - 교과 특성을 반영한 전문적 용어 적절히 사용

4. 금지 사항
    - 평가 결과나 점수 언급 금지
    - 등수나 석차 관련 내용 언급 금지
    - 부정적 표현 사용 금지
    - 나열식 단순 기술 지양
    - 추상적이고 모호한 표현 지양

5. 수준별 서술 원칙
    - 최상위권: 탁월한 사고력과 문제해결력 중심 서술
    - 상위권: 우수한 이해도와 적용력 중심 서술
    - 중위권: 기본 개념 이해와 성실한 참여도 중심 서술
    - 하위권: 수업 참여도와 과제 완수 중심 서술
    - 최하위권: 기본적인 활동 참여와 발전 가능성 중심 서술

6. 필수 포함 요소
    - 구체적인 학습 활동
    - 문제해결 과정
    - 창의적 사고력
    - 참여도와 태도
    - 발전 가능성"""


def generate_assessments(school_type: str, grade: int, subject: str, content: str, achievement: str) -> Tuple[Dict[str, List[str]], List[str]]:
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
{school_type} {grade}학년 {subject} 과목의 '{content}' 단원에 대해 교과의 성취기준이 '{achievement}'일 때,
각각의 성취수준(최상/상/중/하/최하)에 해당하는 세부능력 특기사항을 2개씩 작성하고,
마지막에는 생성된 평가의 주요 포인트를 3줄로 요약해주세요.

각 수준별 정의:
- 최상: 상위 5% 수준
- 상: 상위 6~30% 수준
- 중: 상위 31~70% 수준
- 하: 상위 71~90% 수준
- 최하: 상위 91~100% 수준

형식:
최상-1: [문장1]
최상-2: [문장2]
상-1: [문장1]
...처럼 각 수준별로 두 개의 문장을 작성해주세요.

마지막에 '###요약###' 구분자를 넣고 평가 시 중요 포인트 3줄을 작성해주세요.
"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # 응답 텍스트를 구분자로 분리
        full_response = response.choices[0].message.content.strip()
        assessment_part, summary_part = full_response.split("###요약###")
        
        # 평가 내용 처리
        lines = assessment_part.strip().split('\n')
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
        
        # 요약 내용 처리
        summary_points = [point.strip() for point in summary_part.strip().split('\n') if point.strip()]
        
        return results, summary_points
    
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        return {}, []

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
        achievement = st.text_input("교과 성취기준")
    
    if st.button("세부능력 특기사항 생성"):
        if not all([subject, content, achievement]):
            st.warning("모든 필드를 입력해주세요!")
            return
        
        with st.spinner("세부능력 특기사항을 생성중입니다..."):
            results, summary_points = generate_assessments(school_type, grade, subject, content, achievement)
            
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
                
                # 요약 포인트 표시
                st.markdown("### 📌 평가 작성 시 주요 포인트")
                for point in summary_points:
                    st.markdown(f"- {point}")
                
                st.markdown("### 전체 복사")
                st.code("\n".join(all_comments + ["", "[ 평가 작성 주요 포인트 ]"] + summary_points), language="text")

if __name__ == "__main__":
    main()
