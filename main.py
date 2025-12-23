import streamlit as st
from openai import OpenAI
import time
import json

# --- Configuration & Setup ---
st.set_page_config(
    page_title="ChatGPT 오늘의 메뉴 추천",
    page_icon="🍲",
    layout="centered"
)

def get_gpt_recommendation(api_key, mood, weather, taste, preferred_categories):
    """OpenAI 공식 라이브러리를 사용하여 음식 추천을 받습니다."""
    
    # 키가 비어있는지 확인
    if not api_key:
        return {
            "menu_name": "API 키 미입력",
            "reason": "화면 상단에서 OpenAI API Key를 입력해주세요.",
            "tip": "sk-... 형식의 키가 필요합니다."
        }

    try:
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=api_key.strip())
        
        prompt = f"""
        당신은 최고의 미식가이자 영양사입니다. 다음 상황에 가장 잘 어울리는 음식 메뉴 1개를 추천해주세요.
        
        상황 정보:
        - 기분: {mood}
        - 날씨: {weather}
        - 당기는 맛: {taste}
        - 선호 카테고리: {', '.join(preferred_categories)}
        
        반드시 다음 JSON 형식을 엄격히 지켜서 출력하세요 (추가 텍스트 없이 JSON만 반환):
        {{
          "menu_name": "음식 이름",
          "reason": "추천하는 이유 (2~3문장)",
          "tip": "더 맛있게 먹는 팁"
        }}
        """

        # GPT-4o 모델 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides food recommendations in JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )

        # 결과 파싱
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        # 인증 오류 처리 (401)
        if "401" in str(e):
            return {
                "menu_name": "API 키 인증 실패",
                "reason": "입력하신 API 키가 유효하지 않습니다. (401 Unauthorized)",
                "tip": "키를 다시 확인하거나 OpenAI 대시보드에서 유효성을 확인하세요."
            }
        # 기타 에러 처리
        st.error(f"오류 발생: {str(e)}")
        return None

def main():
    st.title("🍲 ChatGPT 맞춤 음식 추천")
    st.write("당신의 오늘 기분과 날씨를 분석하여 맛있는 메뉴를 제안합니다.")
    st.markdown("---")

    # --- API 키 입력 ---
    st.subheader("🔑 서비스 설정을 완료해주세요")
    api_key_input = st.text_input("OpenAI API Key를 입력하세요 (sk-...)", type="password", help="https://platform.openai.com/api-keys 에서 발급 가능합니다.")
    
    if not api_key_input:
        st.info("💡 API 키를 입력해야 추천 기능을 사용할 수 있습니다.")

    st.markdown("---")

    # --- Main Inputs ---
    st.subheader("🍴 오늘의 상태와 취향")
    
    # 카테고리 선택
    preferred_categories = st.multiselect(
        "선호하는 음식 카테고리를 선택하세요",
        options=["한식", "일식", "중식", "양식", "아시아 푸드", "분식", "패스트푸드", "디저트"],
        default=["한식", "일식"]
    )

    col1, col2 = st.columns(2)

    with col1:
        mood = st.selectbox(
            "지금 기분이 어떠신가요?",
            options=["평범함", "즐거움", "신남", "우울함", "스트레스 받음", "피곤함", "차분함", "의욕적"]
        )

    with col2:
        weather = st.selectbox(
            "현재 날씨는?",
            options=["맑음", "흐림", "비", "눈", "강풍", "무더위", "한파"]
        )

    taste = st.radio(
        "어떤 맛이 당기나요?",
        options=["매콤한 맛", "담백한 맛", "느끼한 맛", "상큼한 맛", "달콤한 맛"],
        horizontal=True
    )

    st.markdown("---")

    # 버튼 클릭 시 동작
    if st.button("✨ ChatGPT에게 메뉴 추천받기"):
        if not api_key_input:
            st.warning("먼저 API 키를 입력해주세요!")
        elif not preferred_categories:
            st.error("최소 하나 이상의 카테고리를 선택해주세요!")
        else:
            with st.spinner("ChatGPT가 최고의 메뉴를 선별 중입니다..."):
                recommendation = get_gpt_recommendation(api_key_input, mood, weather, taste, preferred_categories)

                if recommendation:
                    if "실패" in recommendation['menu_name'] or "미입력" in recommendation['menu_name']:
                        st.error(recommendation['reason'])
                        st.info(f"💡 {recommendation['tip']}")
                    else:
                        st.balloons()
                        
                        # 결과 카드 디자인
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 25px; border-radius: 15px; border: 1px solid #ddd; border-top: 5px solid #10a37f;">
                            <h2 style="color: #10a37f; margin-top: 0;">오늘의 추천: {recommendation['menu_name']}</h2>
                            <p style="font-size: 1.1em; color: #333; line-height: 1.6;">{recommendation['reason']}</p>
                            <hr style="border: 0.5px solid #eee; margin: 20px 0;">
                            <p><strong>💡 더 맛있게 먹는 팁:</strong> {recommendation['tip']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 이미지 표시
                        st.markdown("### 🖼️ 메뉴 이미지")
                        query = recommendation['menu_name'].replace(" ", ",")
                        image_url = f"https://loremflickr.com/800/600/{query},food/all"
                        st.image(image_url, caption=f"맛있는 {recommendation['menu_name']} (예시 이미지)")
                else:
                    st.error("추천을 불러오는 과정에서 네트워크 오류가 발생했습니다.")

    # 하단 푸터
    st.markdown("---")
    st.caption("© AI Food Recommender powered by GPT-4o")

if __name__ == "__main__":
    main()
