import streamlit as st
import random
import time

# --- Configuration & Setup ---
st.set_page_config(
    page_title="맞춤 음식 추천 서비스",
    page_icon="🍲",
    layout="centered"
)

# --- 로컬 음식 데이터베이스 ---
FOOD_DB = [
    {"name": "김치찌개", "category": "한식", "weather": ["흐림", "비", "한파"], "mood": ["평범함", "피곤함"], "taste": "매콤한 맛", "tip": "라면 사리를 추가하면 더 맛있어요!"},
    {"name": "삼겹살", "category": "한식", "weather": ["맑음", "강풍"], "mood": ["즐거움", "신남"], "taste": "담백한 맛", "tip": "구운 김치와 마늘을 곁들여 드세요."},
    {"name": "비빔밥", "category": "한식", "weather": ["맑음", "무더위"], "mood": ["평범함", "차분함"], "taste": "담백한 맛", "tip": "참기름 한 큰술을 더 넣으면 고소함이 살아나요."},
    {"name": "초밥", "category": "일식", "weather": ["맑음", "흐림"], "mood": ["즐거움", "차분함"], "taste": "상큼한 맛", "tip": "흰 살 생선부터 붉은 살 생선 순서로 드세요."},
    {"name": "돈카츠", "category": "일식", "weather": ["맑음", "눈"], "mood": ["평범함", "즐거움"], "taste": "담백한 맛", "tip": "와사비를 살짝 올려 먹으면 느끼함을 잡아줍니다."},
    {"name": "라멘", "category": "일식", "weather": ["비", "눈", "한파"], "mood": ["우울함", "피곤함"], "taste": "느끼한 맛", "tip": "반숙 계란(아지타마고)을 추가해 보세요."},
    {"name": "짜장면", "category": "중식", "weather": ["흐림", "강풍"], "mood": ["평범함", "의욕적"], "taste": "달콤한 맛", "tip": "고춧가루를 살짝 뿌려 먹으면 더 깔끔해요."},
    {"name": "짬뽕", "category": "중식", "weather": ["비", "눈", "강풍"], "mood": ["스트레스 받음", "피곤함"], "taste": "매콤한 맛", "tip": "해산물을 먼저 건져 먹고 면을 드세요."},
    {"name": "파스타", "category": "양식", "weather": ["맑음", "흐림"], "mood": ["즐거움", "차분함"], "taste": "느끼한 맛", "tip": "바질 페스토나 파마산 치즈를 곁들여 보세요."},
    {"name": "피자", "category": "양식", "weather": ["맑음", "무더위"], "mood": ["신남", "의욕적"], "taste": "느끼한 맛", "tip": "핫소스를 뿌려 매콤함을 조절해 보세요."},
    {"name": "떡볶이", "category": "분식", "weather": ["맑음", "비"], "mood": ["스트레스 받음", "신남"], "taste": "매콤한 맛", "tip": "튀김이나 순대를 소스에 찍어 드세요."},
    {"name": "햄버거", "category": "패스트푸드", "weather": ["맑음", "강풍"], "mood": ["신남", "피곤함"], "taste": "느끼한 맛", "tip": "콜라 대신 밀크쉐이크와 함께 먹어보세요."},
    {"name": "쌀국수", "category": "아시아 푸드", "weather": ["흐림", "비", "한파"], "mood": ["평범함", "차분함"], "taste": "담백한 맛", "tip": "해산물 소스와 스리라차 소스를 섞어 찍어 드세요."},
    {"name": "마라탕", "category": "아시아 푸드", "weather": ["흐림", "비"], "mood": ["스트레스 받음", "의욕적"], "taste": "매콤한 맛", "tip": "땅콩 소스(마장)를 찍어 먹으면 매운맛이 중화됩니다."},
    {"name": "조각 케이크", "category": "디저트", "weather": ["맑음", "눈"], "mood": ["우울함", "즐거움"], "taste": "달콤한 맛", "tip": "아메리카노와 함께 즐기면 단맛이 중화되어 완벽합니다."}
]

def get_local_recommendation(mood, weather, taste, preferred_categories):
    """로컬 데이터에서 조건에 맞는 음식을 필터링하여 추천합니다."""
    category_matches = [f for f in FOOD_DB if f["category"] in preferred_categories]
    taste_matches = [f for f in category_matches if f["taste"] == taste]
    
    final_candidates = [
        f for f in taste_matches 
        if weather in f["weather"] or mood in f["mood"]
    ]
    
    if not final_candidates:
        final_candidates = taste_matches
    if not final_candidates:
        final_candidates = category_matches
        
    if final_candidates:
        res = random.choice(final_candidates)
        return {
            "name": res["name"],
            "reason": f"오늘처럼 {weather} 날씨에 {mood} 기분이라면, {taste}이 일품인 {res['name']}이 제격입니다!",
            "tip": res["tip"]
        }
    return None

def main():
    st.title("🍲 맞춤 음식 추천 서비스")
    st.write("당신의 오늘 기분과 날씨를 분석하여 맛있는 메뉴를 제안합니다.")
    st.markdown("---")

    # --- Main Inputs ---
    st.subheader("🍴 오늘의 상태와 취향")
    
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

    if st.button("✨ 오늘의 메뉴 추천받기"):
        if not preferred_categories:
            st.error("최소 하나 이상의 카테고리를 선택해주세요!")
        else:
            with st.spinner("최고의 메뉴를 선별 중입니다..."):
                time.sleep(1) 
                recommendation = get_local_recommendation(mood, weather, taste, preferred_categories)

                if recommendation:
                    st.balloons()
                    
                    # 결과 카드 디자인 (사진 부분 제거)
                    st.markdown(f"""
                    <div style="background-color: #f9f9f9; padding: 25px; border-radius: 15px; border: 1px solid #ddd; border-top: 5px solid #10a37f; margin-bottom: 20px;">
                        <h2 style="color: #10a37f; margin-top: 0;">오늘의 추천: {recommendation['name']}</h2>
                        <p style="font-size: 1.1em; color: #333; line-height: 1.6;">{recommendation['reason']}</p>
                        <hr style="border: 0.5px solid #eee; margin: 20px 0;">
                        <p><strong>💡 더 맛있게 먹는 팁:</strong> {recommendation['tip']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("해당 조건에 맞는 음식을 찾지 못했습니다. 다른 카테고리를 선택해 보세요!")

    st.markdown("---")
    st.caption("© AI Food Recommender System")

if __name__ == "__main__":
    main()
