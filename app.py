
import random
import streamlit as st

# ==========================================
# 1. CAU HINH
# ==========================================
st.set_page_config(
    page_title="Dai chien phong thi",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS - PHONG CACH PIXEL ART
# ==========================================
st.markdown("""
<style>
.stApp {
    background: #07162f;
    color: #eef5ff;
}
.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}
h1, h2, h3, p, label {
    color: #eef5ff;
}
.pixel-title {
    background: linear-gradient(90deg, #102c59, #174780);
    border: 3px solid #428bff;
    border-radius: 10px;
    padding: 14px;
    color: white;
    font-size: 27px;
    font-weight: 900;
    text-align: center;
    text-shadow: 2px 2px #07162f;
    box-shadow: 0 5px 0 #061025;
}
.game-panel {
    background: #10294d;
    border: 3px solid #397bd2;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 4px 0 #061025;
}
.room {
    background: #e9b77c;
    border: 6px solid #8a4f32;
    border-radius: 4px;
    padding: 10px;
    color: #183153;
    text-align: center;
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 38px,
            rgba(120,65,32,0.16) 39px,
            rgba(120,65,32,0.16) 42px
        );
}
.blackboard {
    background: #155743;
    color: #f5f4d5;
    border: 8px solid #92592e;
    padding: 18px 8px;
    margin: 4px auto 12px auto;
    max-width: 520px;
    font-size: 22px;
    font-weight: 900;
    box-shadow: 0 5px 0 #57371f;
}
.teacher-area {
    background: #dca16a;
    border: 3px solid #94562e;
    padding: 8px;
    margin: 8px auto;
    max-width: 300px;
}
.student-row {
    display: flex;
    justify-content: space-around;
    gap: 6px;
    margin: 12px 0;
}
.student {
    background: #ffda9a;
    border: 3px solid #87502d;
    padding: 8px 3px;
    flex: 1;
    font-size: 24px;
    box-shadow: 0 4px 0 #89552f;
}
.student-name {
    color: #183153;
    font-size: 12px;
    font-weight: 900;
}
.desk {
    background: #bc753c;
    border: 3px solid #77431f;
    color: white;
    padding: 8px;
    margin: 5px 0;
    box-shadow: 0 4px 0 #77431f;
}
.pixel-button {
    background: #153967;
    border: 2px solid #539cff;
    padding: 10px;
    border-radius: 5px;
    color: white;
    text-align: center;
    font-weight: bold;
}
.event-box {
    background: #e7f0ff;
    color: #17355e;
    border: 3px solid #5a9df2;
    border-radius: 6px;
    padding: 12px;
    font-weight: bold;
}
.small-text {
    color: #c7dcff;
    font-size: 13px;
}
div.stButton > button {
    width: 100%;
    min-height: 48px;
    border: 2px solid #5799ef;
    border-radius: 5px;
    background: #173967;
    color: white;
    font-weight: bold;
    box-shadow: 0 3px 0 #061025;
}
div.stButton > button:hover {
    background: #285a9d;
    border-color: #a4d4ff;
    color: white;
}
div[data-testid="stMetric"] {
    background: #10294d;
    border: 2px solid #397bd2;
    padding: 10px;
    border-radius: 6px;
}
div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"] {
    color: #eef5ff;
}
.stProgress > div > div > div > div {
    background-color: #48d597;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. TAO GAME MOI
# ==========================================
def new_game(level):
    settings = {
        "Dễ": {"target": 50, "turns": 15, "risk": 10},
        "Trung bình": {"target": 70, "turns": 12, "risk": 20},
        "Khó": {"target": 90, "turns": 10, "risk": 35}
    }
    config = settings[level]

    st.session_state.level = level
    st.session_state.score = 0
    st.session_state.suspicion = 0
    st.session_state.energy = 100
    st.session_state.target = config["target"]
    st.session_state.max_turns = config["turns"]
    st.session_state.risk = config["risk"]
    st.session_state.turn = 1
    st.session_state.status = "playing"
    st.session_state.last_action = "Chưa thực hiện"
    st.session_state.last_event = "Chuông báo giờ kiểm tra đã vang lên!"
    st.session_state.teacher_alert = False
    st.session_state.log = [
        "🔔 Bắt đầu ván chơi!"
    ]


if "status" not in st.session_state:
    new_game("Dễ")

# Dam bao cac bien ton tai
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
    "last_action": "Chưa thực hiện",
    "last_event": "",
    "teacher_alert": False,
    "log": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# 4. LOGIC HANH DONG
# ==========================================
def do_action(action):
    if st.session_state.status != "playing":
        return

    score = st.session_state.score
    suspicion = st.session_state.suspicion
    energy = st.session_state.energy
    risk = st.session_state.risk

    event = ""
    alert = False

    if action == "Tập trung làm bài":
        gain = random.randint(8, 15)
        score += gain
        energy -= random.randint(4, 9)
        suspicion = max(0, suspicion - 2)
        event = f"📚 Bạn tập trung làm bài và tăng {gain} điểm."

    elif action == "Quan sát giáo viên":
        energy -= 2
        suspicion = max(0, suspicion - random.randint(1, 5))
        event = "👀 Bạn quan sát tình hình trong lớp."

    elif action == "Nghỉ ngơi":
        recovery = random.randint(10, 20)
        energy = min(100, energy + recovery)
        event = f"☕ Bạn nghỉ ngơi và hồi phục {recovery} thể lực."

    elif action == "Xem tài liệu":
        gain = random.randint(10, 20)
        score += gain
        suspicion += random.randint(5, risk)
        energy -= 4
        event = f"📖 Bạn tăng {gain} điểm nhưng mức nghi ngờ tăng."

    elif action == "Trao đổi với bạn":
        energy -= 5
        if random.random() < 0.6:
            gain = random.randint(8, 16)
            score += gain
            event = f"🤝 Bạn nhận được gợi ý và tăng {gain} điểm."
        else:
            suspicion += random.randint(10, risk + 5)
            event = "😰 Cuộc trao đổi khiến bạn bị chú ý."

    score = max(0, score)
    suspicion = min(100, max(0, suspicion))
    energy = min(100, max(0, energy))

    # Kiem tra muc nghi ngo
    if suspicion >= 100:
        alert = True
        status = "lost"
        event += " 🚨 Giáo viên phát hiện bạn!"
    elif suspicion >= 70 and random.random() < 0.5:
        alert = True
        event += " 👀 Giáo viên đang chú ý đến bạn!"
        status = "playing"
    else:
        status = "playing"

    # Cap nhat trang thai
    st.session_state.score = score
    st.session_state.suspicion = suspicion
    st.session_state.energy = energy
    st.session_state.last_action = action
    st.session_state.last_event = event
    st.session_state.teacher_alert = alert
    st.session_state.status = status

    # Kiem tra thang/thua
    if st.session_state.status == "playing":
        if score >= st.session_state.target:
            st.session_state.status = "won"
            st.session_state.last_event += " 🏆 Đạt mục tiêu!"
        elif energy <= 0:
            st.session_state.status = "lost"
            st.session_state.last_event += " 😵 Bạn đã hết thể lực!"
        elif st.session_state.turn >= st.session_state.max_turns:
            st.session_state.status = "lost"
            st.session_state.last_event += " ⏰ Đã hết lượt chơi!"

    st.session_state.log.append(
        f"Lượt {st.session_state.turn}: {st.session_state.last_event}"
    )

    # Chi tang luot neu van tiep tuc
    if st.session_state.status == "playing":
        st.session_state.turn += 1

# ==========================================
# 5. TIEU DE GAME
# ==========================================
st.markdown(
    '<div class="pixel-title">📝 ĐẠI CHIẾN PHÒNG THI<br>'
    '<span style="font-size:15px;">'
    'GAME 2D PIXEL ART • QUẢN LÝ ĐIỂM SỐ • THỂ LỰC • NGHI NGỜ'
    '</span></div>',
    unsafe_allow_html=True
)

st.write("")

# ==========================================
# 6. CHON DO KHO
# ==========================================
top1, top2, top3 = st.columns([2, 2, 1])

with top1:
    levels = ["Dễ", "Trung bình", "Khó"]
    current = st.session_state.level
    if current not in levels:
        current = "Dễ"

    selected_level = st.selectbox(
        "🎯 Độ khó",
        levels,
        index=levels.index(current)
    )

with top2:
    st.markdown(
        f"**🏆 Mục tiêu:** {st.session_state.target} điểm"
    )
    st.markdown(
        f"**🎮 Lượt:** {st.session_state.turn}/{st.session_state.max_turns}"
    )

with top3:
    if st.button("🔄 Chơi mới", use_container_width=True):
        new_game(selected_level)
        st.rerun()

if selected_level != st.session_state.level:
    st.info("Bạn đã chọn độ khó khác. Nhấn **Chơi mới** để áp dụng.")

# ==========================================
# 7. KHUNG GAME VA BANG DIEU KHIEN
# ==========================================
left, right = st.columns([2.2, 1], gap="medium")

with left:
    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 🏫 Phòng thi 2D")

    st.markdown('<div class="room">', unsafe_allow_html=True)

    st.markdown(
        '<div class="blackboard">'
        'KỲ THI<br>'
        '<span style="font-size:13px;">'
        'TỰ TIN • BÌNH TĨNH • LÀM BÀI TỐT'
        '</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="teacher-area">'
        '<div style="font-size:32px;">👩‍🏫</div>'
        '<b style="color:#183153;">GIÁO VIÊN</b><br>'
        '<span style="color:#183153;font-size:12px;">'
        'Đang giám sát phòng thi'
        '</span></div>',
        unsafe_allow_html=True
    )

    if st.session_state.teacher_alert:
        st.markdown(
            '<div style="background:#ffbaba;color:#820000;'
            'border:3px solid #a40000;padding:8px;font-weight:bold;">'
            '🚨 GIÁO VIÊN ĐANG CHÚ Ý ĐẾN BẠN!'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="student-row">'
        '<div class="student">🧑‍🎓<div class="student-name">BẠN A</div></div>'
        '<div class="student">👩‍🎓<div class="student-name">BẠN B</div></div>'
        '<div class="student">👨‍🎓<div class="student-name">BẠN C</div></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="student-row">'
        '<div class="desk">🪑<br>📄 Bài thi</div>'
        '<div class="desk">🪑<br>✏️ Bút</div>'
        '<div class="desk">🪑<br>📄 Bài thi</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="student-row">'
        '<div class="student">🧑‍🎓<div class="student-name">HỌC SINH</div></div>'
        '<div class="student">🧑‍🎓<div class="student-name">BẠN</div></div>'
        '<div class="student">🧑‍🎓<div class="student-name">HỌC SINH</div></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="background:#b66d3b;color:white;padding:8px;'
        'border:3px solid #77431f;">'
        '🪟 CỬA SỔ　　　🪴 CÂY XANH　　　🚪 CỬA RA VÀO'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chi so nhan vat
    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 🎮 Chỉ số người chơi")

    a, b, c = st.columns(3)
    with a:
        st.metric("⭐ Điểm", st.session_state.score)
    with b:
        st.metric("👀 Nghi ngờ", f"{st.session_state.suspicion}/100")
    with c:
        st.metric("⚡ Thể lực", f"{st.session_state.energy}/100")

    st.markdown("**Tiến độ điểm số**")
    st.progress(
        min(st.session_state.score / max(st.session_state.target, 1), 1.0)
    )

    st.markdown("**Mức nghi ngờ**")
    st.progress(st.session_state.suspicion / 100)

    st.markdown("**Thể lực**")
    st.progress(st.session_state.energy / 100)

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 🕹️ Hành động")

    if st.session_state.status == "playing":
        if st.button("📚 Tập trung làm bài", use_container_width=True):
            do_action("Tập trung làm bài")
            st.rerun()

        if st.button("👀 Quan sát giáo viên", use_container_width=True):
            do_action("Quan sát giáo viên")
            st.rerun()

        if st.button("☕ Nghỉ ngơi", use_container_width=True):
            do_action("Nghỉ ngơi")
            st.rerun()

        if st.button("📖 Xem tài liệu", use_container_width=True):
            do_action("Xem tài liệu")
            st.rerun()

        if st.button("🤝 Trao đổi với bạn", use_container_width=True):
            do_action("Trao đổi với bạn")
            st.rerun()
    else:
        if st.session_state.status == "won":
            st.success("🏆 CHIẾN THẮNG!")
            st.write("Bạn đã đạt mục tiêu điểm số.")
        else:
            st.error("❌ GAME OVER")
            st.write("Bạn chưa hoàn thành mục tiêu.")

        if st.button("🎮 Chơi lại", use_container_width=True):
            new_game(selected_level)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 📜 Nhật ký")

    for entry in reversed(st.session_state.log[-7:]):
        st.markdown(
            f'<div class="small-text" '
            f'style="border-bottom:1px solid #345477;padding:7px 0;">'
            f'• {entry}</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 💬 Sự kiện gần nhất")
    st.markdown(
        f'<div class="event-box">{st.session_state.last_event}</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. HUONG DAN
# ==========================================
with st.expander("❓ Hướng dẫn chơi"):
    st.markdown("""
    - **Tập trung làm bài:** Tăng điểm, tiêu hao thể lực.
    - **Quan sát giáo viên:** Giảm nhẹ mức nghi ngờ.
    - **Nghỉ ngơi:** Hồi phục thể lực.
    - **Xem tài liệu:** Có thể tăng điểm nhưng tăng nghi ngờ.
    - **Trao đổi với bạn:** Có cơ hội tăng điểm nhưng có rủi ro.

    **Chiến thắng:** Đạt đủ điểm mục tiêu trước khi hết lượt.

    **Thất bại:** Mức nghi ngờ đạt 100, hết thể lực hoặc hết lượt chơi.
    """)
