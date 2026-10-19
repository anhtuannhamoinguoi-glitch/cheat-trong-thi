
import random
import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Đại chiến phòng thi",
    page_icon="📝",
    layout="centered"
)

# ==========================================
# 2. GIAO DIỆN
# ==========================================
st.markdown("""
<style>
.stApp {
    background-color: #eef5ff;
}
.main-title {
    text-align: center;
    color: #183153;
    font-size: 34px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #53657d;
    margin-bottom: 20px;
}
.classroom {
    background: #d9efff;
    border: 4px solid #34495e;
    border-radius: 15px;
    padding: 16px;
    text-align: center;
    color: #243447;
}
.blackboard {
    background: #245c48;
    color: white;
    border: 6px solid #8b5a2b;
    border-radius: 5px;
    padding: 15px;
    margin: 5px auto 20px auto;
    font-size: 21px;
    font-weight: bold;
}
.teacher {
    display: inline-block;
    background: #f8d7da;
    border: 3px solid #842029;
    border-radius: 10px;
    padding: 12px 20px;
    margin: 8px;
    font-size: 25px;
}
.student {
    display: inline-block;
    background: #fff3cd;
    border: 3px solid #34495e;
    border-radius: 8px;
    padding: 10px;
    margin: 5px;
    min-width: 75px;
    font-size: 23px;
}
.desk {
    display: inline-block;
    background: #c58b52;
    border: 3px solid #80552d;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
    font-size: 20px;
}
.alert-box {
    background: #ffe0e0;
    color: #8b0000;
    border: 2px solid #cc0000;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
    margin: 10px 0;
}
.safe-box {
    background: #d8f3dc;
    color: #1b4332;
    border: 2px solid #40916c;
    border-radius: 8px;
    padding: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KHỞI TẠO TRẠNG THÁI GAME
# ==========================================
def new_game(level):
    settings = {
        "Dễ": {
            "target": 50,
            "risk": 15,
            "max_turns": 15
        },
        "Trung bình": {
            "target": 70,
            "risk": 25,
            "max_turns": 12
        },
        "Khó": {
            "target": 90,
            "risk": 40,
            "max_turns": 10
        }
    }

    config = settings[level]

    st.session_state.level = level
    st.session_state.score = 0
    st.session_state.suspicion = 0
    st.session_state.energy = 100
    st.session_state.target = config["target"]
    st.session_state.risk = config["risk"]
    st.session_state.turn = 1
    st.session_state.max_turns = config["max_turns"]
    st.session_state.status = "playing"
    st.session_state.scene = "classroom"
    st.session_state.log = [
        "🔔 Tiếng chuông báo hiệu giờ kiểm tra bắt đầu!"
    ]
    st.session_state.last_action = ""
    st.session_state.last_event = "Hãy hoàn thành mục tiêu của bạn!"
    st.session_state.last_icon = "🔔"
    st.session_state.teacher_alert = False


# Tự khởi tạo nếu chưa có dữ liệu game
if "status" not in st.session_state:
    new_game("Dễ")

# Bổ sung giá trị mặc định để tránh thiếu khóa session_state
defaults = {
    "level": "Dễ",
    "score": 0,
    "suspicion": 0,
    "energy": 100,
    "target": 50,
    "risk": 15,
    "turn": 1,
    "max_turns": 15,
    "status": "playing",
    "scene": "classroom",
    "log": [],
    "last_action": "",
    "last_event": "",
    "last_icon": "🔔",
    "teacher_alert": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# 4. XỬ LÝ HÀNH ĐỘNG
# ==========================================
def do_action(action):
    if st.session_state.status != "playing":
        return

    score = st.session_state.score
    suspicion = st.session_state.suspicion
    energy = st.session_state.energy
    risk = st.session_state.risk

    st.session_state.last_action = action
    st.session_state.teacher_alert = False

    if action == "Tập trung làm bài":
        gain = random.randint(8, 15)
        score += gain
        energy -= random.randint(5, 10)
        suspicion = max(0, suspicion - random.randint(0, 3))
        event = f"📚 Bạn tập trung làm bài và đạt thêm {gain} điểm."
        icon = "📚"

    elif action == "Quan sát giáo viên":
        energy -= 3
        suspicion = max(0, suspicion - random.randint(0, 5))
        event = "👀 Bạn quan sát tình hình trong lớp."
        icon = "👀"

    elif action == "Nghỉ ngơi":
        energy = min(100, energy + random.randint(10, 20))
        event = "☕ Bạn nghỉ ngơi và hồi phục thể lực."
        icon = "☕"

    elif action == "Xem tài liệu":
        gain = random.randint(10, 20)
        score += gain
        suspicion += random.randint(5, risk)
        energy -= random.randint(3, 8)
        event = f"📖 Bạn có thêm {gain} điểm nhưng mức nghi ngờ tăng."
        icon = "📖"

    elif action == "Trao đổi với bạn":
        result = random.randint(1, 100)

        if result <= 60:
            gain = random.randint(8, 18)
            score += gain
            event = f"🤝 Bạn nhận được gợi ý, tăng {gain} điểm."
            icon = "🤝"
        else:
            suspicion += random.randint(10, risk + 5)
            event = "😰 Cuộc trao đổi khiến bạn bị chú ý."
            icon = "😰"

        energy -= 5

    else:
        event = "Bạn chưa thực hiện hành động nào."
        icon = "🔔"

    # Giáo viên có thể phát hiện khi mức nghi ngờ tăng cao
    if suspicion >= 100:
        suspicion = 100
        st.session_state.status = "lost"
        event += " Giáo viên phát hiện bạn! Trò chơi kết thúc."
        st.session_state.teacher_alert = True

    elif suspicion >= 70 and random.random() < 0.5:
        st.session_state.teacher_alert = True
        event += " Giáo viên đang chú ý đến bạn!"

    # Giới hạn các chỉ số
    st.session_state.score = max(0, score)
    st.session_state.suspicion = max(0, min(100, suspicion))
    st.session_state.energy = max(0, min(100, energy))
    st.session_state.last_event = event
    st.session_state.last_icon = icon

    # Ghi nhật ký
    st.session_state.log.append(
        f"Lượt {st.session_state.turn}: {event}"
    )

    # Kết thúc lượt
    if st.session_state.status == "playing":
        if st.session_state.score >= st.session_state.target:
            st.session_state.status = "won"
            st.session_state.last_event += " 🏆 Bạn đã hoàn thành mục tiêu!"

        elif st.session_state.energy <= 0:
            st.session_state.status = "lost"
            st.session_state.last_event += " 😵 Bạn đã hết thể lực!"

        elif st.session_state.turn >= st.session_state.max_turns:
            if st.session_state.score >= st.session_state.target:
                st.session_state.status = "won"
            else:
                st.session_state.status = "lost"
                st.session_state.last_event += " ⏰ Hết lượt chơi!"

        else:
            st.session_state.turn += 1

# ==========================================
# 5. VẼ LỚP HỌC
# ==========================================
def draw_classroom():
    turn = st.session_state.get("turn", 1)
    action = st.session_state.get("last_action", "")
    status = st.session_state.get("status", "playing")
    alert = st.session_state.get("teacher_alert", False)
    score = st.session_state.get("score", 0)
    suspicion = st.session_state.get("suspicion", 0)
    energy = st.session_state.get("energy", 100)
    event = st.session_state.get("last_event", "")
    icon = st.session_state.get("last_icon", "🔔")

    st.markdown('<div class="classroom">', unsafe_allow_html=True)

    st.markdown(
        '<div class="blackboard">'
        '🏫 LỚP HỌC — ĐẠI CHIẾN PHÒNG THI<br>'
        '📝 KIỂM TRA ĐANG DIỄN RA'
        '</div>',
        unsafe_allow_html=True
    )

    if alert:
        st.markdown(
            '<div class="alert-box">'
            '🚨 GIÁO VIÊN ĐANG CHÚ Ý ĐẾN BẠN!'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="safe-box">'
            '🤫 Hãy quản lý điểm số, thể lực và mức nghi ngờ.'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("### 👩‍🏫 Khu vực giáo viên")
    st.markdown(
        '<div class="teacher">👩‍🏫<br>GIÁO VIÊN</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 👨‍🎓 Khu vực học sinh")
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

    # Hiển thị chỉ số
    st.markdown("### 📊 Thông tin người chơi")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("⭐ Điểm số", score)
        st.metric("👀 Mức nghi ngờ", f"{suspicion}/100")

    with col2:
        st.metric("⚡ Thể lực", f"{energy}/100")
        st.metric("🎮 Lượt chơi", f"{turn}/{st.session_state.max_turns}")

    st.progress(min(score / max(st.session_state.target, 1), 1.0))
    st.caption(f"Mục tiêu điểm số: {st.session_state.target}")

    st.progress(suspicion / 100)
    st.caption("Mức nghi ngờ: càng cao càng nguy hiểm.")

    st.progress(energy / 100)
    st.caption("Thể lực: cần duy trì trên 0.")

    st.markdown(f"**🎬 Hành động gần nhất:** {action or 'Chưa thực hiện'}")
    st.markdown(f"**{icon} Sự kiện:** {event or 'Chưa có sự kiện mới'}")

    if status == "playing":
        st.info("🟢 Trạng thái: Đang chơi")
    elif status == "won":
        st.success("🏆 CHIẾN THẮNG! Bạn đã hoàn thành mục tiêu.")
    else:
        st.error("❌ GAME OVER! Hãy thử lại.")

# ==========================================
# 6. TIÊU ĐỀ GAME
# ==========================================
st.markdown(
    '<div class="main-title">📝 ĐẠI CHIẾN PHÒNG THI</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">'
    'Game mô phỏng lớp học — quản lý điểm số và mức độ nghi ngờ'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================
# 7. CHỌN ĐỘ KHÓ
# ==========================================
st.markdown("### 🎯 Chọn độ khó")

difficulty = st.selectbox(
    "Độ khó của ván chơi",
    ["Dễ", "Trung bình", "Khó"],
    index=["Dễ", "Trung bình", "Khó"].index(
        st.session_state.level
        if st.session_state.level in ["Dễ", "Trung bình", "Khó"]
        else "Dễ"
    )
)

if st.button("🔄 Bắt đầu ván mới", use_container_width=True):
    new_game(difficulty)
    st.rerun()

st.caption(
    "Dễ: 15 lượt, mục tiêu 50 điểm. "
    "Trung bình: 12 lượt, mục tiêu 70 điểm. "
    "Khó: 10 lượt, mục tiêu 90 điểm."
)

# ==========================================
# 8. HIỂN THỊ LỚP HỌC VÀ CHỈ SỐ
# ==========================================
draw_classroom()

# ==========================================
# 9. NÚT HÀNH ĐỘNG
# ==========================================
st.markdown("---")
st.markdown("### 🕹️ Chọn hành động")

if st.session_state.status == "playing":
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📚 Tập trung làm bài", use_container_width=True):
            do_action("Tập trung làm bài")
            st.rerun()

        if st.button("👀 Quan sát giáo viên", use_container_width=True):
            do_action("Quan sát giáo viên")
            st.rerun()

        if st.button("☕ Nghỉ ngơi", use_container_width=True):
            do_action("Nghỉ ngơi")
            st.rerun()

    with col2:
        if st.button("📖 Xem tài liệu", use_container_width=True):
            do_action("Xem tài liệu")
            st.rerun()

        if st.button("🤝 Trao đổi với bạn", use_container_width=True):
            do_action("Trao đổi với bạn")
            st.rerun()

else:
    st.warning("Ván chơi đã kết thúc. Hãy bắt đầu ván mới để chơi tiếp.")

    if st.button("🎮 Chơi lại ngay", use_container_width=True):
        new_game(difficulty)
        st.rerun()

# ==========================================
# 10. NHẬT KÝ TRÒ CHƠI
# ==========================================
st.markdown("---")
st.markdown("### 📜 Nhật ký trò chơi")

with st.expander("Xem lịch sử hành động", expanded=True):
    if st.session_state.log:
        for item in reversed(st.session_state.log[-10:]):
            st.write("• " + item)
    else:
        st.write("Chưa có hoạt động nào.")

# ==========================================
# 11. HƯỚNG DẪN
# ==========================================
with st.expander("❓ Hướng dẫn chơi"):
    st.markdown("""
    **Mục tiêu:** Đạt đủ điểm trước khi hết lượt.

    - 📚 **Tập trung làm bài:** Tăng điểm, tiêu hao thể lực.
    - 👀 **Quan sát giáo viên:** Giảm nhẹ mức nghi ngờ.
    - ☕ **Nghỉ ngơi:** Hồi phục thể lực.
    - 📖 **Xem tài liệu:** Có thể tăng điểm nhưng tăng nghi ngờ.
    - 🤝 **Trao đổi với bạn:** Có cơ hội tăng điểm nhưng có rủi ro.

    **Điều kiện chiến thắng:** Đạt mục tiêu điểm số.

    **Điều kiện thất bại:** Bị phát hiện, hết thể lực hoặc hết lượt mà chưa đạt mục tiêu.
    """)
```
