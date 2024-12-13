from openai import OpenAI
import streamlit as st
from typing import List

# Streamlit 페이지 설정
st.set_page_config(page_title="문장 변형 생성기", page_icon="✍️")

# OpenAI API 키 입력 필드
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

def generate_variations(input_text: str, num_variations: int, api_key: str) -> List[str]:
    """GPT를 사용하여 입력 문장의 변형을 생성합니다."""
    
    # 새로운 클라이언트 초기화 방식
    client = OpenAI(api_key=api_key)
    
    try:
        # GPT에게 보낼 프롬프트 작성
        prompt = f"""
다음 문장의 의미는 유지하면서 {num_variations}개의 다른 표현으로 바꿔주세요:
"{input_text}"

규칙:
1. 원래 의미는 반드시 유지
2. 어순 변경, 어미 변경, 유의어 사용 등 다양한 방식으로 변형
3. 각각의 변형된 문장은 새로운 줄에 숫자와 함께 표시
4. 자연스러운 한국어로 표현
"""

        # 새로운 API 호출 방식
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 한국어 전문가입니다. 문장을 자연스럽게 변형하는 작업을 수행합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # 새로운 응답 구조에 맞게 수정
        variations = response.choices[0].message.content.strip().split('\n')
        # 빈 줄 제거 및 숫자. 형식 정리
        variations = [line.strip() for line in variations if line.strip()]
        
        return variations
    
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        return []

def main():
    st.title("📝 문장 변형 생성기")
    st.markdown("---")
    
    # 입력 필드
    input_text = st.text_area("변형하고 싶은 문장을 입력하세요:", height=100)
    num_variations = st.number_input("생성할 문장 수:", min_value=1, max_value=10, value=3)
    
    if st.button("변형 생성하기"):
        if not api_key:
            st.error("OpenAI API 키를 입력해주세요!")
            return
        
        if not input_text:
            st.warning("문장을 입력해주세요!")
            return
        
        with st.spinner("문장 변형을 생성중입니다..."):
            variations = generate_variations(input_text, num_variations, api_key)
            
            if variations:
                st.success("생성 완료!")
                st.markdown("### 생성된 문장 변형:")
                for i, variation in enumerate(variations, 1):
                    st.markdown(f"{i}. {variation}")
                    
                # 복사 버튼 추가
                all_variations = "\n".join(variations)
                st.markdown("### 전체 복사")
                st.code(all_variations, language="text")

if __name__ == "__main__":
    main()
