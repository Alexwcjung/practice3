import streamlit as st

st.set_page_config(page_title="영어 부정문 퀴즈", layout="centered")

st.title("🚀 Alex선생님과 함께하는 영어 부정문 퀴즈")
st.caption("일반동사와 be동사의 부정문 · 20문제 · 2지선다")

# ---------------------------
# 문제 데이터 (20문제)
# 문제 순서 / 보기 순서 고정
# ---------------------------
question_data = [
    {"question": "I (     ) a student.", "answer": "am not", "choices": ["am not", "do not"]},
    {"question": "She (     ) happy.", "answer": "is not", "choices": ["is not", "does not"]},
    {"question": "They (     ) teachers.", "answer": "are not", "choices": ["are not", "do not"]},
    {"question": "He (     ) tall.", "answer": "is not", "choices": ["is not", "does not"]},
    {"question": "We (     ) busy now.", "answer": "are not", "choices": ["are not", "do not"]},
    {"question": "You (     ) my friend.", "answer": "are not", "choices": ["are not", "do not"]},
    {"question": "The dog (     ) hungry.", "answer": "is not", "choices": ["is not", "does not"]},
    {"question": "My father (     ) at home.", "answer": "is not", "choices": ["is not", "does not"]},
    {"question": "I (     ) like pizza.", "answer": "do not", "choices": ["am not", "do not"]},
    {"question": "She (     ) play soccer.", "answer": "does not", "choices": ["is not", "does not"]},
    {"question": "They (     ) study English.", "answer": "do not", "choices": ["are not", "do not"]},
    {"question": "He (     ) eat breakfast.", "answer": "does not", "choices": ["is not", "does not"]},
    {"question": "We (     ) watch TV every day.", "answer": "do not", "choices": ["are not", "do not"]},
    {"question": "You (     ) know the answer.", "answer": "do not", "choices": ["are not", "do not"]},
    {"question": "My brother (     ) get up early.", "answer": "does not", "choices": ["is not", "does not"]},
    {"question": "The students (     ) run fast.", "answer": "do not", "choices": ["are not", "do not"]},
    {"question": "My mother (     ) a doctor.", "answer": "is not", "choices": ["is not", "does not"]},
    {"question": "Tom and I (     ) classmates.", "answer": "are not", "choices": ["are not", "do not"]},
    {"question": "She (     ) drink milk.", "answer": "does not", "choices": ["is not", "does not"]},
    {"question": "I (     ) go to bed late.", "answer": "do not", "choices": ["am not", "do not"]},
]

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = question_data.copy()

if "stage" not in st.session_state:
    # stage 1: 전체 풀이
    # stage 2: 오답만 다시 풀이
    # stage 3: 틀린 문제만 정답 공개
    st.session_state.stage = 1

if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []

if "first_score" not in st.session_state:
    st.session_state.first_score = 0

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

# ---------------------------
# 다시 시작
# ---------------------------
if st.button("처음부터 다시 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")
quiz_data = st.session_state.quiz_data

# ---------------------------
# 1단계: 전체 문제 풀이
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 풀이")

    for i, item in enumerate(quiz_data):
        st.write(f"### {i+1}. {item['question']}")
        st.radio(
            "알맞은 답을 고르세요.",
            item["choices"],
            key=f"q1_{i}",
            index=None
        )

    if st.button("1차 제출"):
        wrong_indices = []
        correct_count = 0

        for i, item in enumerate(quiz_data):
            user_answer = st.session_state.get(f"q1_{i}")
            if user_answer == item["answer"]:
                correct_count += 1
            else:
                wrong_indices.append(i)

        st.session_state.first_score = correct_count
        st.session_state.wrong_indices = wrong_indices

        if len(wrong_indices) == 0:
            st.session_state.final_score = 20
            st.session_state.stage = 3
        else:
            st.session_state.stage = 2

        st.rerun()

# ---------------------------
# 2단계: 틀린 문제만 다시 풀기
# ---------------------------
elif st.session_state.stage == 2:
    first_score = st.session_state.first_score
    wrong_indices = st.session_state.wrong_indices

    st.subheader("1차 결과")
    st.write(f"점수: **{first_score} / 20**")
    st.warning(f"틀린 문제 수: {len(wrong_indices)}문제")

    st.markdown("---")
    st.subheader("2차 풀이")
    st.caption("1차에서 틀린 문제만 다시 풉니다.")

    for idx in wrong_indices:
        item = quiz_data[idx]
        st.write(f"### {idx+1}. {item['question']}")
        st.radio(
            "다시 정답을 고르세요.",
            item["choices"],
            key=f"q2_{idx}",
            index=None
        )

    if st.button("2차 제출"):
        additional_correct = 0

        for idx in wrong_indices:
            item = quiz_data[idx]
            retry_answer = st.session_state.get(f"q2_{idx}")
            if retry_answer == item["answer"]:
                additional_correct += 1

        st.session_state.final_score = st.session_state.first_score + additional_correct
        st.session_state.stage = 3
        st.rerun()

# ---------------------------
# 3단계: 1차에서 틀린 문제만 정답 공개
# ---------------------------
elif st.session_state.stage == 3:
    wrong_indices = st.session_state.wrong_indices

    st.subheader("최종 결과")
    st.write(f"1차 점수: **{st.session_state.first_score} / 20**")
    st.write(f"최종 점수: **{st.session_state.final_score} / 20**")

    if st.session_state.final_score == 20:
        st.success("만점입니다!")
        st.balloons()
    elif st.session_state.final_score >= 16:
        st.success("아주 잘했습니다!")
    elif st.session_state.final_score >= 12:
        st.info("잘했습니다.")
    else:
        st.warning("조금 더 연습해 봅시다.")

    st.markdown("---")
    st.subheader("정답 확인")

    if len(wrong_indices) == 0:
        st.success("1차에서 모두 맞혔습니다. 확인할 오답이 없습니다.")
    else:
        st.caption("아래에는 1차에서 틀린 문제만 표시됩니다.")

        for idx in wrong_indices:
            item = quiz_data[idx]
            first_answer = st.session_state.get(f"q1_{idx}")
            second_answer = st.session_state.get(f"q2_{idx}")

            st.write(f"### {idx+1}. {item['question']}")
            st.write(f"- 정답: **{item['answer']}**")
            st.write(f"- 1차 선택: {first_answer if first_answer else '미응답'}")
            st.write(f"- 2차 선택: {second_answer if second_answer else '미응답'}")

            if second_answer == item["answer"]:
                st.success("2차에서 정답")
            else:
                st.error("2차에서도 오답")
