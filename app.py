
import random
import streamlit as st

st.set_page_config(
    page_title="Đại chiến phòng thi",
    page_icon="📝",
    layout="centered"
)

st.title("📝 ĐẠI CHIẾN PHÒNG THI")
st.caption("Game mô phỏng vui nhộn — hãy quản lý điểm số và mức độ nghi ngờ!")

LEVELS = {
    "Dễ": {"time": 12, "risk": 10},
    "Trung bình": {"time": 9, "risk": 25},
    "Khó": {"time": 7, "risk": 45},
}

QUESTIONS = [
    {
        "q": "1. Python là gì?",
        "choices": ["Một ngôn ngữ lập trình", "Một chiếc máy tính", "Một trò chơi"],
        "answer": "Một ngôn ngữ lập trình",
    },
    {
        "q": "2. 5 × 6 bằng bao nhiêu?",
        "choices": ["11", "30", "56"],
        "answer": "30",
    },
    {
        "q": "3. Hành tinh chúng ta đang sống là gì?",
        "choices": ["Sao Hỏa", "Sao Kim", "Trái Đất"],
        "answer": "Trái Đất",
    },
    {
        "q": "4. Một giờ có bao nhiêu phút?",
        "choices": ["30", "60", "100"],
        "answer": "60",
    },
    {
        "q": "5. GitHub thường được dùng để làm gì?",
        "choices": [
            "Lưu trữ và quản lý mã nguồn",
            "Sạc pin máy tính",
            "In tài liệu",
        ],
        "answer": "Lưu trữ và quản lý mã nguồn",
    },
}


def start_game(level):
    st.session_state.level = level
    st.session_state.score = 0
    st.session_state.suspicion = 0
    st.session_state.time_left = LEVELS[level]["time"]
    st.session_state.turn = 0
    st.session_state.log = []
    st.session_state.started = True


if "started" not in st.session_state:
    start_game("Dễ")

if not st.session_state.started:
    st.info("Chọn mức độ và bắt đầu ván mới.")

level_choice = st.selectbox(
    "🎚️ Chọn mức độ khó",
    list(LEVELS.keys()),
    index=list(LEVELS.keys()).index(st.session_state.level),
)

if st.button("🔄 Bắt đầu ván mới"):
    start_game(level_choice)
    st.rerun()

score = st.session_state.score
suspicion = st.session_state.suspicion
time_left = st.session_state.time_left
turn = st.session_state.turn

st.divider()

c1, c2, c3 = st.columns(3)
c1.metric("🏆 Điểm", score)
c2.metric("👀 Nghi ngờ", f"{suspicion}%")
c3.metric("⏳ Thời gian", time_left)

st.progress(min(suspicion, 100) / 100)

finished = (
    turn >= len(QUESTIONS)
    or suspicion >= 100
    or time_left <= 0
)

if finished:
    st.subheader("🏁 Kết thúc ván thi!")

    if suspicion >= 100:
        st.error("Bạn đã bị phát hiện trong trò chơi!")
    elif time_left <= 0:
        st.warning("Hết giờ làm bài!")
    else:
        st.success("Bạn đã hoàn thành tất cả câu hỏi!")

    st.write(f"**Điểm cuối cùng:** {score}/50")
    st.write(f"**Mức độ nghi ngờ cuối cùng:** {suspicion}%")

    if score >= 40 and suspicion < 60:
        st.balloons()
        st.write("🌟 Xếp loại: Xuất sắc!")
    elif score >= 25:
        st.write("👍 Xếp loại: Khá!")
    else:
        st.write("📚 Xếp loại: Cần cố gắng thêm!")

    st.subheader("📜 Nhật ký ván chơi")
    for item in st.session_state.log:
        st.write("• " + item)

else:
    question = QUESTIONS[turn]

    st.subheader(f"📖 Câu hỏi {turn + 1}/{len(QUESTIONS)}")
    st.write(question["q"])

    answer = st.radio(
        "Chọn câu trả lời:",
        question["choices"],
        key=f"answer_{turn}",
    )

    st.write("### Bạn sẽ làm gì?")

    st.caption(
        "Các lựa chọn chỉ tác động đến điểm số và xác suất "
        "bị phát hiện trong game."
    )

    def take_action(action):
        correct = answer == question["answer"]
        points = 0
        note = ""

        if action == "study":
            st.session_state.time_left -= 1
            st.session_state.suspicion = max(
                0, st.session_state.suspicion - 5
            )

            if correct:
                points = 10
                note = "Trả lời đúng khi tự làm bài: +10 điểm."
            else:
                note = "Trả lời sai: không có điểm."

        elif action == "observe":
            st.session_state.time_left -= 2
            st.session_state.suspicion = max(
                0, st.session_state.suspicion - 15
            )
            note = "Quan sát tình hình: giảm 15% nghi ngờ."

        elif action == "cheat":
            st.session_state.time_left -= 1
            risk = LEVELS[st.session_state.level]["risk"]
            detected = random.randint(1, 100) <= risk

            if detected:
                st.session_state.suspicion += 40
                note = "Bị phát hiện trong game: +40% nghi ngờ."
            else:
                if correct:
                    points = 10
                    note = "Qua được sự kiện: +10 điểm."
                else:
                    note = "Không bị phát hiện nhưng trả lời sai."

        st.session_state.score += points
        st.session_state.turn += 1
        st.session_state.log.append(
            f"Câu {turn + 1}: {note}"
        )

    b1, b2, b3 = st.columns(3)

    if b1.button("✍️ Tự làm bài", use_container_width=True):
        take_action("study")
        st.rerun()

    if b2.button("👀 Quan sát", use_container_width=True):
        take_action("observe")
        st.rerun()

    if b3.button("🎲 Thử vận may", use_container_width=True):
        take_action("cheat")
        st.rerun()

    st.info(
        "Mẹo chơi: mỗi hành động tiêu tốn thời gian. "
        "Nếu mức nghi ngờ đạt 100%, ván chơi kết thúc."
    )
