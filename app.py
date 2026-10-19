
import random
import html
import streamlit as st

st.set_page_config(
    page_title="Gian lận trong thi - Pixel Classroom",
    page_icon="📝",
    layout="wide",
)

# =====================================================
# 1. GIAO DIỆN PIXEL ART VÀ HIỆU ỨNG
# =====================================================

st.markdown("""
<style>
.stApp {
    background: #101827;
    color: #f4f7ff;
}
h1, h2, h3, p, label {
    color: #f4f7ff;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
div.stButton > button {
    min-height: 58px;
    border: 2px solid #5c96ed;
    border-radius: 7px;
    background: #203b60;
    color: white;
    font-weight: bold;
    transition: transform .15s, background .15s;
}
div.stButton > button:hover {
    transform: translateY(-3px);
    background: #315786;
    border-color: #ffda66;
    color: #ffda66;
}
.pixel-panel {
    background: #172b45;
    border: 3px solid #4d8bdf;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 4px 4px 0 #091321;
}
.action-effect {
    animation: pixel-pop .35s ease-out,
               pixel-flash .7s ease-in-out 1;
    border: 3px solid #ffd166;
    border-radius: 8px;
    padding: 12px;
    margin: 12px 0;
    background: #243d60;
    text-align: center;
    box-shadow: 4px 4px 0 #091321;
}
.action-effect .big-icon {
    font-size: 42px;
    line-height: 1.3;
    animation: pixel-float .4s ease-out;
}
.action-effect p {
    margin-bottom: 0;
}
.action-alert {
    border-color: #ff5b6e;
    background: #602839;
}
.action-success {
    border-color: #55e6a5;
    background: #174b43;
}
@keyframes pixel-pop {
    0% { transform: scale(.85); opacity: .2; }
    70% { transform: scale(1.04); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes pixel-flash {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.5); }
}
@keyframes pixel-float {
    from { transform: translateY(12px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
@keyframes teacher-move {
    0% { transform: translateX(-5px); }
    50% { transform: translateX(5px); }
    100% { transform: translateX(-5px); }
}
.teacher-sprite {
    animation: teacher-move 1.5s steps(4, end) infinite;
    transform-box: fill-box;
    transform-origin: center;
}
.player-sprite {
    animation: pixel-pop .25s steps(3, end);
}
.scene-caption {
    padding: 10px 12px;
    border-left: 4px solid #ffd166;
    background: #172b45;
    margin-top: 8px;
    border-radius: 4px;
}
div[data-testid="stMetric"] {
    background: #172b45;
    border: 1px solid #315786;
    border-radius: 8px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📝 GIAN LẬN TRONG THI")
st.caption("PIXEL CLASSROOM • 2D TOP-DOWN • Mô phỏng phòng thi")


# =====================================================
# 2. CẤU HÌNH GAME
# =====================================================

LEVELS = {
    "Dễ": {
        "suspicion": 5,
        "energy": 100,
        "target": 50,
        "risk": 0.10,
    },
    "Trung bình": {
        "suspicion": 15,
        "energy": 90,
        "target": 70,
        "risk": 0.25,
    },
    "Khó": {
        "suspicion": 25,
        "energy": 80,
        "target": 90,
        "risk": 0.40,
    },
}

SCENES = [
    "Giám thị đang đi quanh lớp.",
    "Cả phòng thi im lặng, đồng hồ tích tắc.",
    "Giám thị dừng lại gần một dãy bàn.",
    "Một bạn học sinh đang loay hoay với đề thi.",
    "Tiếng bước chân vang lên ở cuối lớp.",
    "Bạn cần bình tĩnh hoàn thành bài thi.",
]

ACTIONS = {
    "📖 Tự làm bài nghiêm túc": {
        "icon": "✍️",
        "pose": "write",
        "title": "Bạn tập trung làm bài!",
        "description": "Bút chạy trên giấy thi. Bạn đang cố gắng làm bài.",
    },
    "🧠 Bình tĩnh suy nghĩ": {
        "icon": "💭",
        "pose": "think",
        "title": "Bạn đang suy nghĩ!",
        "description": "Một bong bóng suy nghĩ xuất hiện trên đầu bạn.",
    },
    "👀 Lén xem tài liệu": {
        "icon": "⚠️",
        "pose": "sneak",
        "title": "Bạn lén xem tài liệu!",
        "description": "Bạn hành động lén lút. Giám thị có thể chú ý.",
    },
    "☕ Nghỉ ngơi lấy sức": {
        "icon": "⚡",
        "pose": "rest",
        "title": "Bạn đang nghỉ ngơi!",
        "description": "Bạn thư giãn và hồi phục thể lực.",
    },
}


def new_game(level):
    settings = LEVELS[level]
    st.session_state.level = level
    st.session_state.score = 0
    st.session_state.suspicion = settings["suspicion"]
    st.session_state.energy = settings["energy"]
    st.session_state.target = settings["target"]
    st.session_state.risk = settings["risk"]
    st.session_state.turn = 1
    st.session_state.max_turns = 8
    st.session_state.status = "playing"
    st.session_state.scene = "Tiếng trống vang lên! Kỳ thi bắt đầu."
    st.session_state.log = ["🔔 Kỳ thi bắt đầu!"]
    st.session_state.last_action = ""
    st.session_state.last_event = ""
    st.session_state.last_icon = "🔔"
    st.session_state.teacher_alert = False


if "status" not in st.session_state:
    new_game("Dễ")


# =====================================================
# 3. VẼ NHÂN VẬT PIXEL ART BẰNG SVG
# =====================================================

def draw_classroom():
    """Tạo cảnh lớp học và nhân vật theo trạng thái hiện tại."""

    turn = st.session_state.turn
    action = st.session_state.last_action
    status = st.session_state.status
    alert = st.session_state.teacher_alert

    # Giám thị đổi vị trí qua từng lượt.
    teacher_positions = [100, 230, 360, 500, 570, 440, 300, 150]
    teacher_x = teacher_positions[(turn - 1) % len(teacher_positions)]

    # Vị trí cố định của người chơi.
    px, py = 300, 245

    # Tư thế mặc định.
    pose = "idle"
    if action in ACTIONS:
        pose = ACTIONS[action]["pose"]

    # Tư thế đầu và thân.
    head_y = py - 16 if pose == "write" else py - 21
    body_y = py - 2

    if pose == "rest":
        head_y = py - 12
        body_y = py + 1

    shirt = "#ffbd4a" if pose == "sneak" else "#4789d8"
    if status == "caught":
        shirt = "#d94b5b"

    # Biểu tượng nổi trên nhân vật.
    bubble = ""
    if pose == "write":
        bubble = f"""
        <g class="player-sprite">
          <rect x="{px+18}" y="{py-57}" width="42" height="28"
                rx="3" fill="#fff0c5" stroke="#493021" stroke-width="3"/>
          <path d="M{px+25} {py-48}h25 M{px+25} {py-41}h17"
                stroke="#7b6a57" stroke-width="2"/>
          <path d="M{px+14} {py-19}l13 8"
                stroke="#ffe8a3" stroke-width="4"/>
        </g>
        """
    elif pose == "think":
        bubble = f"""
        <g class="player-sprite">
          <rect x="{px+20}" y="{py-65}" width="42" height="27"
                rx="8" fill="#e6f5ff" stroke="#315786" stroke-width="3"/>
          <circle cx="{px+25}" cy="{py-33}" r="5" fill="#e6f5ff"/>
          <text x="{px+41}" y="{py-47}" text-anchor="middle"
                font-size="17">?</text>
        </g>
        """
    elif pose == "sneak":
        bubble = f"""
        <g class="player-sprite">
          <path d="M{px+15} {py-62}l12 -12l12 12z"
                fill="#ffdf57" stroke="#8a382f" stroke-width="3"/>
          <text x="{px+27}" y="{py-62}" text-anchor="middle"
                font-size="13" font-weight="bold" fill="#8a382f">!</text>
          <rect x="{px-25}" y="{py-3}" width="24" height="18"
                fill="#fff0c5" stroke="#493021" stroke-width="2"/>
        </g>
        """
    elif pose == "rest":
        bubble = f"""
        <g class="player-sprite">
          <text x="{px+24}" y="{py-48}" font-size="18">Z</text>
          <text x="{px+39}" y="{py-61}" font-size="13">z</text>
        </g>
        """

    teacher_bubble = ""
    if alert or status == "caught":
        teacher_bubble = f"""
        <g>
          <rect x="{teacher_x-12}" y="78" width="35" height="28"
                rx="4" fill="#ff5964" stroke="#6c1e2b" stroke-width="3"/>
          <text x="{teacher_x+5}" y="98" text-anchor="middle"
                font-size="19" font-weight="bold" fill="white">!</text>
        </g>
        """

    svg = [
        '<div style="width:100%;overflow-x:auto;">',
        """
        <svg xmlns="http://www.w3.org/2000/svg"
             viewBox="0 0 680 410"
             style="width:100%;height:auto;display:block;
                    image-rendering:pixelated;
                    border:4px solid #4d8bdf;border-radius:6px;">
          <defs>
            <pattern id="floor" width="48" height="36"
                     patternUnits="userSpaceOnUse">
              <rect width="48" height="36" fill="#b99a76"/>
              <path d="M0 0H48 M0 36H48 M24 0V18 M0 18H48"
                    stroke="#8c7158" stroke-width="1"/>
            </pattern>
          </defs>
          <rect width="680" height="410" fill="url(#floor)"/>
          <rect x="0" y="0" width="680" height="57" fill="#674b3d"/>
          <rect x="0" y="49" width="680" height="9" fill="#dfb88b"/>

          <!-- Cửa sổ -->
          <rect x="12" y="7" width="68" height="38"
                fill="#8bd8f5" stroke="#f5d8a8" stroke-width="5"/>
          <path d="M46 7V45 M12 26H80" stroke="#e7f3ff" stroke-width="4"/>

          <!-- Bảng đen -->
          <rect x="174" y="5" width="320" height="53"
                fill="#5c3827" stroke="#d6a36d" stroke-width="4"/>
          <rect x="182" y="12" width="304" height="39" fill="#185b45"/>
          <path d="M200 23h58m-30 10h80m80-8h55m-190 12h90"
                stroke="#c8e5bb" stroke-width="2" stroke-dasharray="12 5"/>

          <!-- Cửa lớp -->
          <rect x="604" y="5" width="62" height="50"
                fill="#64432f" stroke="#e8c69c" stroke-width="4"/>
          <rect x="612" y="11" width="46" height="38" fill="#a4d8f4"/>
          <circle cx="650" cy="31" r="3" fill="#f9dc75"/>

          <!-- Bàn giáo viên -->
          <rect x="255" y="64" width="170" height="31"
                fill="#86502d" stroke="#50301f" stroke-width="4"/>
          <rect x="263" y="69" width="154" height="9" fill="#c58b4b"/>

          <!-- Giáo viên -->
          <g class="teacher-sprite">
            <rect x="{tx}" y="72" width="25" height="22"
                  fill="#e9b18b" stroke="#342b38" stroke-width="3"/>
          </g>
        """.replace("{tx}", str(teacher_x)),
        f"""
          <rect x="{teacher_x+4}" y="76" width="4" height="4" fill="#30263a"/>
          <rect x="{teacher_x+15}" y="76" width="4" height="4" fill="#30263a"/>
          <rect x="{teacher_x-2}" y="94" width="30" height="17"
                fill="#315ba8" stroke="#342b38" stroke-width="3"/>
          {teacher_bubble}
        """,
    ]

    # Bàn học sinh thành lưới 4 cột x 3 hàng.
    xs = [65, 210, 355, 500]
    ys = [145, 220, 295]

    for row, y in enumerate(ys):
        for col, x in enumerate(xs):
            is_player = row == 1 and col == 1

            # Vẽ vùng nổi bật quanh bàn người chơi.
            if is_player:
                svg.append(f"""
                <rect x="{x-10}" y="{y-32}" width="96" height="80"
                      rx="4" fill="#ffe36e" opacity=".25"/>
                <rect x="{x-10}" y="{y-32}" width="96" height="80"
                      rx="4" fill="none" stroke="#ffdb4d" stroke-width="4"/>
                """)

                # Nhân vật người chơi.
                svg.append(f"""
                <g class="player-sprite">
                  <rect x="{px+5}" y="{head_y}" width="22" height="19"
                        fill="#f0b58b" stroke="#342b38" stroke-width="3"/>
                  <rect x="{px+3}" y="{head_y-4}" width="26" height="8"
                        fill="#382b30"/>
                  <rect x="{px+9}" y="{head_y+6}" width="3" height="3"
                        fill="#30263a"/>
                  <rect x="{px+20}" y="{head_y+6}" width="3" height="3"
                        fill="#30263a"/>
                  <rect x="{px}" y="{body_y}" width="32" height="21"
                        fill="{shirt}" stroke="#342b38" stroke-width="3"/>
                  <rect x="{px+3}" y="{body_y+19}" width="9" height="8"
                        fill="#292c42"/>
                  <rect x="{px+19}" y="{body_y+19}" width="9" height="8"
                        fill="#292c42"/>
                </g>
                {bubble}
                <rect x="{x+8}" y="{y+31}" width="60" height="15"
                      fill="#172b45" stroke="#ffdb4d" stroke-width="2"/>
                <text x="{x+38}" y="{y+42}" text-anchor="middle"
                      font-size="10" font-weight="bold" fill="#ffeb8a">BẠN</text>
                """)
            else:
                hair = random.choice(["#382b30", "#222b3a", "#573a2b"])
                shirt_other = random.choice(
                    ["#477ecb", "#e16b52", "#399d7c", "#8058b5"]
                )
                svg.append(f"""
                <rect x="{x+27}" y="{y-24}" width="20" height="19"
                      fill="{hair}"/>
                <rect x="{x+30}" y="{y-21}" width="14" height="14"
                      fill="#f0b58b"/>
                <rect x="{x+32}" y="{y-16}" width="3" height="3" fill="#30263a"/>
                <rect x="{x+40}" y="{y-16}" width="3" height="3" fill="#30263a"/>
                <rect x="{x+25}" y="{y-5}" width="24" height="19"
                      fill="{shirt_other}" stroke="#49342b" stroke-width="2"/>
                <rect x="{x+28}" y="{y+13}" width="7" height="8" fill="#33364a"/>
                <rect x="{x+40}" y="{y+13}" width="7" height="8" fill="#33364a"/>
                """)

            # Bàn, chân bàn và giấy thi.
            svg.append(f"""
            <rect x="{x}" y="{y+2}" width="76" height="34"
                  fill="#80502f" stroke="#493021" stroke-width="3"/>
            <rect x="{x+4}" y="{y+5}" width="68" height="24" fill="#d8a36b"/>
            <rect x="{x+25}" y="{y+9}" width="25" height="15"
                  fill="#fff2ce" stroke="#7c624b" stroke-width="1"/>
            <path d="M{x+29} {y+13}h16 M{x+29} {y+17}h12"
                  stroke="#8b8172" stroke-width="1"/>
            <rect x="{x+6}" y="{y+36}" width="5" height="8" fill="#493021"/>
            <rect x="{x+65}" y="{y+36}" width="5" height="8" fill="#493021"/>
            """)

    # Hiệu ứng phủ toàn màn hình khi kết thúc.
    if status == "caught":
        svg.append("""
        <rect x="0" y="0" width="680" height="410"
              fill="#c51f3a" opacity=".25"/>
        <rect x="165" y="155" width="350" height="65"
              rx="5" fill="#6a182b" stroke="#ff5b6e" stroke-width="5"/>
        <text x="340" y="196" text-anchor="middle"
              font-size="25" font-weight="bold" fill="white">
              BỊ PHÁT HIỆN!
        </text>
        """)
    elif status == "finished" and st.session_state.score >= st.session_state.target:
        svg.append("""
        <rect x="175" y="155" width="330" height="65"
              rx="5" fill="#174b43" stroke="#55e6a5" stroke-width="5"/>
        <text x="340" y="196" text-anchor="middle"
              font-size="25" font-weight="bold" fill="white">
              CHIẾN THẮNG!
        </text>
        """)

    svg.append("</svg></div>")
    st.markdown("".join(svg), unsafe_allow_html=True)


# =====================================================
# 4. XỬ LÝ HÀNH ĐỘNG VÀ SỰ KIỆN
# =====================================================

def take_action(action):
    risk = st.session_state.risk
    event = ""
    icon = ACTIONS[action]["icon"]

    st.session_state.last_action = action
    st.session_state.last_icon = icon
    st.session_state.teacher_alert = False

    if action == "📖 Tự làm bài nghiêm túc":
        points = random.randint(8, 15)
        st.session_state.score += points
        st.session_state.energy -= 12
        event = f"✍️ Bạn tập trung làm bài và được +{points} điểm."

    elif action == "🧠 Bình tĩnh suy nghĩ":
        points = random.randint(4, 10)
        st.session_state.score += points
        st.session_state.energy -= 6
        st.session_state.suspicion -= 5
        event = f"💭 Bạn suy nghĩ cẩn thận và được +{points} điểm."

    elif action == "👀 Lén xem tài liệu":
        points = random.randint(12, 23)
        st.session_state.score += points
        st.session_state.energy -= 8
        increase = random.randint(12, 24)
        st.session_state.suspicion += increase
        event = (
            f"⚠️ Bạn được +{points} điểm nhưng mức nghi ngờ "
            f"tăng {increase}."
        )

        if random.random() < risk + 0.15:
            st.session_state.teacher_alert = True
            event += " 🚨 Giám thị chú ý đến bạn!"

    elif action == "☕ Nghỉ ngơi lấy sức":
        recovery = random.randint(15, 24)
        st.session_state.energy += recovery
        st.session_state.suspicion -= 3
        event = f"⚡ Bạn nghỉ ngơi và hồi phục {recovery} thể lực."

    # Sự kiện bất ngờ.
    if random.random() < risk:
        increase = random.randint(4, 10)
        st.session_state.suspicion += increase
        st.session_state.teacher_alert = True
        event += f" 👁️ Sự kiện bất ngờ: nghi ngờ tăng {increase}!"

    # Giới hạn chỉ số.
    st.session_state.suspicion = max(
        0, min(100, st.session_state.suspicion)
    )
    st.session_state.energy = max(
        0, min(100, st.session_state.energy)
    )

    st.session_state.last_event = event
    st.session_state.log.insert(0, event)

    # Điều kiện kết thúc.
    if st.session_state.suspicion >= 100:
        st.session_state.status = "caught"
    elif st.session_state.energy <= 0:
        st.session_state.status = "exhausted"
    elif st.session_state.turn >= st.session_state.max_turns:
        st.session_state.status = "finished"
    else:
        st.session_state.turn += 1
        st.session_state.scene = random.choice(SCENES)


# =====================================================
# 5. THANH CÀI ĐẶT VÀ CHỈ SỐ
# =====================================================

with st.sidebar:
    st.header("⚙️ CÀI ĐẶT")

    selected_level = st.selectbox(
        "Chọn độ khó cho ván mới",
        ["Dễ", "Trung bình", "Khó"],
        index=["Dễ", "Trung bình", "Khó"].index(
            st.session_state.level
        ),
    )

    st.write("### 📜 Luật chơi")
    st.write("- Một ván có tối đa 8 lượt.")
    st.write("- Đạt mục tiêu điểm để thắng.")
    st.write("- Nghi ngờ chạm 100: bị phát hiện.")
    st.write("- Thể lực về 0: hết sức.")
    st.write("- Mỗi hành động có thể tạo sự kiện bất ngờ.")

    if st.button("🔄 BẮT ĐẦU VÁN MỚI", use_container_width=True):
        new_game(selected_level)
        st.rerun()

m1, m2, m3, m4 = st.columns(4)
m1.metric("📚 ĐIỂM SỐ", st.session_state.score)
m2.metric("👀 NGHI NGỜ", f"{st.session_state.suspicion}/100")
m3.metric("⚡ THỂ LỰC", f"{st.session_state.energy}/100")
m4.metric("⏱️ LƯỢT", f"{min(st.session_state.turn, 8)}/8")

st.progress(st.session_state.suspicion / 100)
st.caption(
    f"Độ khó: {st.session_state.level} • "
    f"Mục tiêu: {st.session_state.target} điểm"
)


# =====================================================
# 6. LỚP HỌC VÀ NHẬT KÝ
# =====================================================

left, right = st.columns([2.1, 1])

with left:
    st.subheader("🏫 LỚP HỌC 2D PIXEL ART")
    draw_classroom()

    if st.session_state.last_action:
        action_info = ACTIONS[st.session_state.last_action]
        alert_class = (
            "action-alert"
            if st.session_state.teacher_alert
            or st.session_state.status == "caught"
            else "action-success"
            if st.session_state.last_action == "☕ Nghỉ ngơi lấy sức"
            else ""
        )

        st.markdown(
            f"""
            <div class="action-effect {alert_class}">
                <div class="big-icon">{action_info["icon"]}</div>
                <h3>{action_info["title"]}</h3>
                <p>{action_info["description"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="scene-caption">'
        f'🔔 {html.escape(st.session_state.scene)}'
        f'</div>',
        unsafe_allow_html=True,
    )

with right:
    st.subheader("📋 NHẬT KÝ PHÒNG THI")

    with st.container(border=True):
        for item in st.session_state.log[:7]:
            st.write("• " + item)

    st.subheader("🎯 NHIỆM VỤ")
    st.write(f"Đạt ít nhất **{st.session_state.target} điểm**.")
    st.progress(
        min(st.session_state.score / st.session_state.target, 1.0)
    )
    st.write(
        f"Tiến độ: {st.session_state.score}/"
        f"{st.session_state.target} điểm"
    )

    st.subheader("👨‍🏫 GIÁM THỊ")
    if st.session_state.status == "caught":
        st.error("Bạn đã bị phát hiện!")
    elif st.session_state.teacher_alert:
        st.warning("Giám thị đang chú ý đến bạn!")
    else:
        st.success("Giám thị chưa phát hiện điều bất thường.")


# =====================================================
# 7. NÚT ĐIỀU KHIỂN VÀ KẾT QUẢ
# =====================================================

st.divider()
st.subheader("🎮 BẠN MUỐN LÀM GÌ TRONG LƯỢT NÀY?")

if st.session_state.status == "playing":
    action_names = list(ACTIONS.keys())
    cols = st.columns(4)

    for i, action in enumerate(action_names):
        with cols[i]:
            if st.button(
                action,
                key=f"action_button_{i}",
                use_container_width=True,
            ):
                take_action(action)
                st.rerun()

else:
    if st.session_state.status == "caught":
        st.error("🚨 BẠN ĐÃ BỊ GIÁM THỊ PHÁT HIỆN!")
    elif st.session_state.status == "exhausted":
        st.warning("😵 Bạn đã hết thể lực trước khi hoàn thành kỳ thi.")
    elif st.session_state.score >= st.session_state.target:
        st.success("🏆 CHIẾN THẮNG! Bạn đã đạt mục tiêu điểm.")
    else:
        st.warning("📘 Kỳ thi kết thúc nhưng bạn chưa đạt mục tiêu điểm.")

    st.write(f"**Tổng điểm:** {st.session_state.score}")
    st.write(f"**Mức nghi ngờ:** {st.session_state.suspicion}/100")
    st.write(f"**Độ khó:** {st.session_state.level}")

    if st.button("🔁 CHƠI LẠI", type="primary"):
        new_game(st.session_state.level)
        st.rerun()

st.divider()
st.caption(
    "GIAN LẬN TRONG THI • PIXEL CLASSROOM 2D • Phiên bản 2.0"
)
