
import random
import streamlit as st

# =========================
# 1. CAU HINH TRANG
# =========================
st.set_page_config(
    page_title="Dai chien phong thi",
    page_icon="📝",
    layout="centered"
)

# =========================
# 2. GIAO DIEN
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #edf4ff;
}
.title {
    text-align: center;
    color: #183153;
    font-size: 32px;
    font-weight: bold;
}
.classroom {
    background: #d9efff;
    border: 4px solid #34495e;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}
.board {
    background: #245c48;
    color: white;
    border: 6px solid #8b5a2b;
    padding: 15px;
    margin-bottom: 15px;
    font-size: 22px;
    font-weight: bold;
}
.teacher {
    display: inline-block;
    background: #f8d7da;
    border: 3px solid #842029;
    border-radius: 10px;
    padding: 12px;
    margin: 6px;
    font-size: 24px;
}
.student {
    display: inline-block;
    background: #fff3cd;
    border: 3px solid #34495e;
    border-radius: 8px;
    padding: 10px;
    margin: 5px;
    font-size: 22px;
}
.desk {
    display: inline-block;
    background: #c58b52;
    border: 3px solid #80552d;
    padding: 10px;
    margin: 5px;
    border-radius: 5px;
}
.warning {
    background: #ffe0e0;
    color: #8b0000;
    border: 2px solid #cc0000;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 3. KHOI TAO GAME
# =========================
def new_game(level):
    settings = {
        "Dễ": {"target": 50, "max_turns": 15, "risk": 10},
        "Trung bình": {"target": 70, "max_turns": 12, "risk": 20},
        "Khó": {"target": 90, "max_turns": 10, "risk": 35}
    }

    config = settings[level]

    st.session_state.level = level
    st.session_state.score = 0
    st.session_state.suspicion = 0
    st.session_state.energy = 100
    st.session_state.target = config["target"]
    st.session_state.max_turns = config["max_turns"]
    st.session_state.risk = config["risk"]
    st.session_state.turn = 1
    st.session_state.status = "playing"
    st.session_state.last_action = "Chưa có"
    st.session_state.last_event = "Chuông báo giờ kiểm tra đã vang lên!"
    st.session_state.last_icon = "🔔"
    st.session_state.teacher_alert = False
    st.session_state.log = ["🔔 Bắt đầu ván chơi!"]


if "status" not in st.session_state:
    new_game("Dễ")

# Dam bao cac bien luon ton tai
defaults = {
    "level": "Dễ",
    "score": 0,
    "suspicion": 0,
    "energy": 100,
    "target": 50,
    "max_turns": 15,
    "risk": 10,
    "turn": 1,
    "status": "playing",
    "last_action": "Chưa có",
    "last_event": "",
    "last_icon": "🔔",
    "teacher_alert": False,
    "log": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# 4. XU LY HANH DONG
# =========================
def do_action(action):
    if st.session_state.status != "playing":
        return

    score = st.session_state.score
    suspicion = st.session_state.suspicion
    energy = st.session_state.energy
    risk = st.session_state.risk

    event = ""
    icon = "🔔"
    st.session_state.teacher_alert = False

    if action == "Làm bài":
        gain = random.randint(8, 15)
        score += gain
        energy -= random.randint(4, 9)
        suspicion = max(0, suspicion - 2)
        event = f"Bạn tập trung làm bài và tăng {gain} điểm."
        icon = "📚"

    elif action == "Quan sát":
        energy -= 2
        suspicion = max(0, suspicion - random.randint(1, 5))
        event = "Bạn quan sát giáo viên và tình hình lớp học."
        icon = "👀"

    elif action == "Nghỉ ngơi":
        energy = min(100, energy + random.randint(10, 20))
        event = "Bạn nghỉ ngơi và hồi phục thể lực."
        icon = "☕"

    elif action == "Xem tài liệu":
        gain = random.randint(10, 20)
        score += gain
        suspicion += random.randint(5, risk)
        energy -= 4
        event = f"Bạn tăng {gain} điểm nhưng mức nghi ngờ tăng."
        icon = "📖"

    elif action == "Trao đổi":
        if random.random() < 0.6:
            gain = random.randint(8, 16)
            score += gain
            event = f"Bạn nhận được gợi ý và tăng {gain} điểm."
            icon = "🤝"
        else:
            suspicion += random.randint(10, risk + 5)
            event = "Bạn bị chú ý khi trao đổi với bạn bên cạnh."
            icon = "😰"
        energy -= 5

    score = max(0, score)
    suspicion = max(0, min(100, suspicion))
    energy = max(0, min(100, energy))

    st.session_state.score = score
    st.session_state.suspicion = suspicion
    st.session_state.energy = energy
    st.session_state.last_action = action
    st.session_state.last_event = event
    st.session_state.last_icon = icon

    if suspicion >= 100:
        st.session_state.status = "lost"
        st.session_state.teacher_alert = True
        event += " Giáo viên đã phát hiện bạn!"
    elif suspicion >= 70 and random.random() < 0.5:
        st.session_state.teacher_alert = True
        event += " Giáo viên đang chú ý đến bạn!"

    st.session_state.last_event = event
    st.session_state.log.append(
        f"Lượt {st.session_state.turn}: {event}"
    )

    if st.session_state.status == "playing":
        if score >= st.session_state.target:
            st.session_state.status = "won"
        elif energy <= 0:
            st.session_state.status = "lost"
            st.session_state.last_event += " Bạn đã hết thể lực!"
        elif st.session_state.turn >= st.session_state.max_turns:
            st.session_state.status = "lost"
            st.session_state.last_event += " Đã hết lượt chơi!"
        else:
            st.session_state.turn += 1

# =========================
# 5. VE LOP HOC
# =========================
def draw_classroom():
    st.markdown('<div class="classroom">', unsafe_allow_html=True)

    st.markdown(
        '<div class="board">🏫 ĐẠI CHIẾN PHÒNG THI<br>'
        '📝 GIỜ KIỂM TRA ĐANG DIỄN RA</div>',
        unsafe_allow_html=True
    )

    if st.session_state.teacher_alert:
        st.markdown(
            '<div class="warning">🚨 GIÁO VIÊN ĐANG CHÚ Ý ĐẾN BẠN!</div>',
            unsafe_allow_html=True
        )

    st.markdown("### 👩‍🏫 Giáo viên")
    st.markdown(
        '<div class="teacher">👩‍🏫<br>Giáo viên</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 👨‍🎓 Học sinh")
    st.markdown(
        '<div class="student">🧑‍🎓<br>Bạn</div>'
        '<div class="student">👨‍🎓<br>Bạn A</div>'
        '<div class="student">👩‍🎓<br>Bạn B</div>'
        '<div class="student">🧑‍🎓<br>Bạn C</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🪑 Bàn thi")
    st.markdown(
        '<div class="desk">📄 Bài thi</div>'
        '<div class="desk">✏️ Bút</div>'
        '<div class="desk">📚 Sách</div>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 6. TIEU DE
# =========================
st.markdown(
    '<div class="title">📝 ĐẠI CHIẾN PHÒNG THI</div>',
    unsafe_allow_html=True
)
st.caption("Game mô phỏng lớp học — quản lý điểm số, thể lực và mức nghi ngờ.")

# =========================
# 7. CHON DO KHO
# =========================
levels = ["Dễ", "Trung bình", "Khó"]
current_level = st.session_state.level

if current_level not in levels:
    current_level = "Dễ"

difficulty = st.selectbox(
    "Chọn độ khó",
    levels,
    index=levels.index(current_level)
)

if st.button("🔄 Bắt đầu ván mới", use_container_width=True):
    new_game(difficulty)
    st.rerun()

st.caption(
    "Dễ: 50 điểm / 15 lượt | "
    "Trung bình: 70 điểm / 12 lượt | "
    "Khó: 90 điểm / 10 lượt"
)

# =========================
# 8. HIEN THI GAME
# =========================
draw_classroom()

st.markdown("### 📊 Chỉ số người chơi")
col1, col2 = st.columns(2)

with col1:
    st.metric("⭐ Điểm số", st.session_state.score)
    st.metric("👀 Mức nghi ngờ", f"{st.session_state.suspicion}/100")

with col2:
    st.metric("⚡ Thể lực", f"{st.session_state.energy}/100")
    st.metric(
        "🎮 Lượt chơi",
        f"{st.session_state.turn}/{st.session_state.max_turns}"
    )

st.progress(min(st.session_state.score / st.session_state.target, 1.0))
st.caption(f"Mục tiêu: {st.session_state.target} điểm")

st.progress(st.session_state.suspicion / 100)
st.caption("Mức nghi ngờ")

st.progress(st.session_state.energy / 100)
st.caption("Thể lực")

st.markdown(f"**Hành động gần nhất:** {st.session_state.last_action}")
st.info(f"{st.session_state.last_icon} {st.session_state.last_event}")

# =========================
# 9. CAC NUT HANH DONG
# =========================
st.markdown("---")
st.markdown("### 🕹️ Chọn hành động")

if st.session_state.status == "playing":
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📚 Tập trung làm bài", use_container_width=True):
            do_action("Làm bài")
            st.rerun()

        if st.button("👀 Quan sát giáo viên", use_container_width=True):
            do_action("Quan sát")
            st.rerun()

        if st.button("☕ Nghỉ ngơi", use_container_width=True):
            do_action("Nghỉ ngơi")
            st.rerun()

    with col2:
        if st.button("📖 Xem tài liệu", use_container_width=True):
            do_action("Xem tài liệu")
            st.rerun()

        if st.button("🤝 Trao đổi với bạn", use_container_width=True):
            do_action("Trao đổi")
            st.rerun()

else:
    if st.session_state.status == "won":
        st.success("🏆 CHIẾN THẮNG! Bạn đã đạt mục tiêu.")
    else:
        st.error("❌ GAME OVER! Bạn chưa hoàn thành mục tiêu.")

    if st.button("🎮 Chơi lại", use_container_width=True):
        new_game(difficulty)
        st.rerun()

# =========================
# 10. NHAT KY
# =========================
st.markdown("---")
st.markdown("### 📜 Nhật ký trò chơi")

with st.expander("Xem lịch sử hành động", expanded=True):
    if st.session_state.log:
        for item in reversed(st.session_state.log[-10:]):
            st.write("• " + item)
    else:
        st.write("Chưa có hoạt động.")

# =========================
# 11. HUONG DAN
# =========================
with st.expander("❓ Hướng dẫn chơi"):
    st.markdown("""
    **Mục tiêu:** Đạt đủ điểm trước khi hết lượt.

    - 📚 **Tập trung làm bài:** Tăng điểm và tiêu hao thể lực.
    - 👀 **Quan sát giáo viên:** Giảm nhẹ mức nghi ngờ.
    - ☕ **Nghỉ ngơi:** Hồi phục thể lực.
    - 📖 **Xem tài liệu:** Có thể tăng điểm nhưng tăng nghi ngờ.
    - 🤝 **Trao đổi với bạn:** Có cơ hội tăng điểm nhưng cũng có rủi ro.

    **Chiến thắng:** Đạt đủ điểm mục tiêu.

    **Thất bại:** Bị phát hiện, hết thể lực hoặc hết lượt chơi.
    """)
```
