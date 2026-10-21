
import random
import streamlit as st

st.set_page_config(
    page_title="Đại chiến phòng thi",
    page_icon="📝",
    layout="centered",
)

# ===== GIAO DIỆN =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #101827 0%, #182235 100%);
    color: #f4f6fb;
}
h1, h2, h3, p, label {
    color: #f4f6fb;
}
.hero {
    padding: 24px;
    border: 1px solid #45546c;
    border-radius: 18px;
    background: linear-gradient(135deg, #253650, #171f30);
    text-align: center;
    margin-bottom: 18px;
}
.hero h1 {
    font-size: 32px;
    margin-bottom: 8px;
}
.hero p {
    color: #c5d1e3;
}
div.stButton > button {
    border-radius: 10px;
    min-height: 44px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ===== CẤU HÌNH ĐỘ KHÓ =====
LEVELS = {
    "Dễ": {
        "time": 12,
        "risk": 10,
        "teacher": "Giáo viên đang ngồi chấm bài",
    },
    "Trung bình": {
        "time": 10,
        "risk": 25,
        "teacher": "Giáo viên thường xuyên đi kiểm tra",
    },
    "Khó": {
        "time": 8,
        "risk": 45,
        "teacher": "Giáo viên giám sát rất nghiêm",
    },
}

# ===== NGÂN HÀNG CÂU HỎI =====
QUESTIONS = [
    {
        "q": "Python là gì?",
        "choices": [
            "Ngôn ngữ lập trình",
            "Hệ điều hành",
            "Thiết bị máy tính",
            "Trình duyệt web",
        ],
        "answer": "Ngôn ngữ lập trình",
    },
    {
        "q": "5 × 6 bằng bao nhiêu?",
        "choices": ["11", "25", "30", "56"],
        "answer": "30",
    },
    {
        "q": "Hành tinh chúng ta đang sống là gì?",
        "choices": ["Sao Hỏa", "Sao Kim", "Trái Đất", "Sao Mộc"],
        "answer": "Trái Đất",
    },
    {
        "q": "Một giờ có bao nhiêu phút?",
        "choices": ["30", "45", "60", "100"],
        "answer": "60",
    },
    {
        "q": "GitHub chủ yếu được dùng để làm gì?",
        "choices": [
            "Quản lý và chia sẻ mã nguồn",
            "Sạc pin",
            "Chỉnh sửa ảnh",
            "Tăng tốc Internet",
        ],
        "answer": "Quản lý và chia sẻ mã nguồn",
    },
    {
        "q": "Thực vật hấp thụ khí nào trong quang hợp?",
        "choices": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
        "answer": "Carbon dioxide",
    },
    {
        "q": "Kết quả của 12² là bao nhiêu?",
        "choices": ["24", "124", "144", "122"],
        "answer": "144",
    },
    {
        "q": "Cơ quan nào bơm máu đi khắp cơ thể người?",
        "choices": ["Phổi", "Gan", "Thận", "Tim"],
        "answer": "Tim",
    },
    {
        "q": "File Python thường có phần mở rộng nào?",
        "choices": [".jpg", ".py", ".mp3", ".docx"],
        "answer": ".py",
    },
    {
        "q": "Nước tinh khiết đóng băng ở khoảng bao nhiêu độ C?",
        "choices": ["0", "10", "50", "100"],
        "answer": "0",
    },
]

# ===== KHỞI TẠO VÁN CHƠI =====
def new_game(level):
    st.session_state.level = level
    st.session_state.questions = random.sample(QUESTIONS, 5)
    st.session_state.score = 0
    st.session_state.suspicion = 0
    st.session_state.time_left = LEVELS[level]["time"]
    st.session_state.turn = 0
    st.session_state.log = []
    st.session_state.finished = False
    st.session_state.reason = ""

if "level" not in st.session_state:
    new_game("Dễ")

# ===== TIÊU ĐỀ =====
st.markdown("""
<div class="hero">
    <h1>📝 ĐẠI CHIẾN PHÒNG THI</h1>
    <p>Giữ bình tĩnh, hoàn thành bài thi và quản lý thời gian!</p>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Game mô phỏng vui nhộn. Các lựa chọn chỉ ảnh hưởng "
    "đến điểm số và sự kiện trong trò chơi."
)

# ===== CHỌN ĐỘ KHÓ =====
level_names = list(LEVELS.keys())
selected_level = st.selectbox(
    "🎚️ Mức độ khó",
    level_names,
    index=level_names.index(st.session_state.level),
)

if st.button("🔄 Bắt đầu ván mới", use_container_width=True):
    new_game(selected_level)
    st.rerun()

st.caption(LEVELS[selected_level]["teacher"])

# ===== TRẠNG THÁI VÁN CHƠI =====
score = st.session_state.score
suspicion = st.session_state.suspicion
time_left = st.session_state.time_left
turn = st.session_state.turn
questions = st.session_state.questions

finished = (
    st.session_state.finished
    or turn >= len(questions)
    or suspicion >= 100
    or time_left <= 0
)

st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("🏆 Điểm số", score)
col2.metric("👀 Nghi ngờ", f"{suspicion}%")
col3.metric("⏳ Lượt thời gian", time_left)

st.progress(min(suspicion, 100) / 100)
st.caption("Thanh tiến độ biểu thị mức độ nghi ngờ.")

# ===== MÀN HÌNH KẾT THÚC =====
if finished:
    st.session_state.finished = True
    st.subheader("🏁 KẾT THÚC VÁN THI")

    if suspicion >= 100:
        st.error("🚨 Bạn đã bị phát hiện!")
    elif time_left <= 0:
        st.warning("⏰ Hết thời gian làm bài!")
    else:
        st.success("🎉 Bạn đã hoàn thành bài thi!")

    st.write(f"**Điểm cuối cùng:** {score}/50")
    st.write(f"**Số câu đã xử lý:** {min(turn, 5)}/5")
    st.write(f"**Mức nghi ngờ:** {suspicion}%")

    if score >= 40 and suspicion < 60:
        st.balloons()
        st.success("Xếp loại: Xuất sắc!")
    elif score >= 25:
        st.info("Xếp loại: Khá!")
    else:
        st.info("Xếp loại: Cần cố gắng thêm!")

    st.subheader("📜 Nhật ký ván chơi")
    if st.session_state.log:
        for item in st.session_state.log:
            st.write("• " + item)
    else:
        st.write("Bạn chưa thực hiện hành động nào.")

    if st.button("🎮 Chơi lại", use_container_width=True):
        new_game(selected_level)
        st.rerun()

# ===== MÀN HÌNH CÂU HỎI =====
else:
    question = questions[turn]

    st.subheader(f"📖 Câu {turn + 1}/5")
    st.markdown(f"### {question['q']}")

    answer = st.radio(
        "Chọn một đáp án:",
        question["choices"],
        key=f"answer_{turn}",
    )

    st.write("### 🎯 Chọn hành động")

    st.write(
        "Mỗi hành động tiêu tốn lượt thời gian. "
        "Hãy cân nhắc trước khi lựa chọn."
    )

    def take_action(action):
        correct = answer == question["answer"]
        points = 0
        note = ""
        time_cost = 1

        if action == "study":
            time_cost = 1
            st.session_state.suspicion = max(
                0, st.session_state.suspicion - 5
            )

            if correct:
                points = 10
                note = "Tự làm bài đúng: +10 điểm."
            else:
                note = (
                    "Tự làm bài sai. Đáp án đúng: "
                    + question["answer"]
                )

        elif action == "observe":
            time_cost = 2
            st.session_state.suspicion = max(
                0, st.session_state.suspicion - 15
            )
            note = "Nghỉ quan sát: giảm 15% nghi ngờ."

        elif action == "cheat":
            time_cost = 1
            risk = LEVELS[st.session_state.level]["risk"]
            detected = random.randint(1, 100) <= risk

            if detected:
                st.session_state.suspicion = min(
                    100, st.session_state.suspicion + 40
                )
                note = "Bị phát hiện: tăng 40% nghi ngờ."
            elif correct:
                points = 10
                note = "Thoát sự kiện thành công: +10 điểm."
            else:
                note = "Không bị phát hiện nhưng trả lời sai."

        st.session_state.score += points
        st.session_state.time_left -= time_cost
        st.session_state.log.append(
            f"Câu {turn + 1}: {note}"
        )
        st.session_state.turn += 1

        if st.session_state.suspicion >= 100:
            st.session_state.finished = True
        elif st.session_state.time_left <= 0:
            st.session_state.finished = True
        elif st.session_state.turn >= len(questions):
            st.session_state.finished = True

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
        "Mẹo: tự làm bài giúp giảm nghi ngờ. "
        "Thử vận may có thể đem lại điểm hoặc khiến bạn bị phát hiện."
    )
