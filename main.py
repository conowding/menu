import streamlit as st
import requests
import time
import json

# --- Configuration & Setup ---
st.set_page_config(
    page_title="ChatGPT 오늘의 메뉴 추천",
    page_icon="🍲",
    layout="centered"
)

# OpenAI API 설정 (사용자의 API 키를 여기에 입력해야 합니다)
OPENAI_API_KEY = "" # 실제 사용 시 본인의 OpenAI API Key를 입력하세요.

def get_gpt_recommendation(mood, weather, taste, preferred_categories):
    """ChatGPT API(GPT-4o)를 호출하여 음식 추천을 받습니다."""
    if not OPENAI_API_KEY:
        return {
            "menu_name": "API 키 미설정",
            "reason": "프로그램 상단에 OpenAI API Key를 설정해야 합니다.",
            "tip": "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"
        }

    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    prompt = f"""
    당신은 최고의 미식가이자 영양사입니다. 다음 상황에 가장 잘 어울리는 음식 메뉴 1개를 추천해주세요.
    
    상황 정보:
    - 기분: {mood}
    - 날씨: {weather}
    - 당기는 맛: {taste}
    - 선호 카테고리: {', '.join(preferred_categories)}
    
    반드시 다음 JSON 형식을 엄격히 지켜서 출력하세요:
    {{
      "menu_name": "음식 이름",
      "reason": "추천하는 이유 (2~3문장)",
      "tip": "더 맛있게 먹는 팁"
    }}
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides food recommendations in JSON format."},
            {"role": "user", "content": prompt}
        ],
        "response_format": { "type": "json_object" }
    }

    # Exponential Backoff 구현
    retries = 5
    for i in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return json.loads(content)
            elif response.status_code == 429: # Rate limit
                time.sleep(2**i)
                continue
            else:
                st.error(f"API 오류: {response.status_code} - {response.text}")
                break
        except Exception as e:
            time.sleep(2**i)
            continue
    
    return None

def main():
    st.title("🍲 ChatGPT 맞춤 음식 추천")
    st.write("ChatGPT가 당신의 오늘 기분과 날씨를 분석하여 맛있는 메뉴를 제안합니다.")
    st.markdown("---")

    # --- Sidebar ---
    st.sidebar.header("⚙️ 개인 설정")
    preferred_categories = st.sidebar.multiselect(
        "선호하는 카테고리",
        options=["한식", "일식", "중식", "양식", "아시아 푸드", "분식", "패스트푸드", "디저트"],
        default=["한식", "일식", "중식", "양식"]
    )
    
    st.sidebar.info("참고: 이 앱을 실행하려면 유효한 OpenAI API Key가 필요합니다.")

    # --- Main Inputs ---
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

    if st.button("✨ ChatGPT에게 메뉴 추천받기"):
        if not preferred_categories:
            st.error("최소 하나 이상의 카테고리를 선택해주세요!")
            return

        with st.spinner("ChatGPT가 최고의 레시피를 검색 중입니다..."):
            recommendation = get_gpt_recommendation(mood, weather, taste, preferred_categories)

            if recommendation:
                st.balloons()
                
                # 결과 카드 디자인
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 25px; border-radius: 15px; border: 1px solid #ddd; border-top: 5px solid #10a37f;">
                    <h2 style="color: #10a37f; margin-top: 0;">오늘의 추천: {recommendation['menu_name']}</h2>
                    <p style="font-size: 1.1em; color: #333;">{recommendation['reason']}</p>
                    <hr style="border: 0.5px solid #eee;">
                    <p><strong>💡 꿀팁:</strong> {recommendation['tip']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 이미지 예시 (Unsplash 무료 이미지 API 활용)
                st.markdown("### 🖼️ 메뉴 이미지")
                query = recommendation['menu_name'].replace(" ", "+")
                image_url = f"https://source.unsplash.com/1600x900/?food,{query}"
                # Unsplash 소스 서비스가 종료되었을 수 있으므로 대체 방식 사용
                st.image(f"https://loremflickr.com/800/600/{query},food", caption=f"맛있는 {recommendation['menu_name']}")
                
            else:
                st.error("추천을 불러오지 못했습니다. API 키가 유효한지 확인해주세요.")

if __name__ == "__main__":
    main()
