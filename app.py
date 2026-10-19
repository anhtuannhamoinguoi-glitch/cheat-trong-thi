
import random
import streamlit as st

st.set_page_config(
    page_title="Gian lận trong thi",
    page_icon="📝",
    layout="wide"
)

# =========================
# 1. GIAO DIỆN PIXEL ART
# =========================

st.markdown("""
/* Hiệu ứng hoạt ảnh khi thực hiện hành động */
@keyframes pixel-pop {
    0%   { transform: scale(0.65); opacity: 0; }
    65%  { transform: scale(1.08); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}

@keyframes pixel-flash {
    0%, 100% { filter: brightness(1); }
    50%      { filter: brightness(1.8); }
}

@keyframes pixel-float {
    0%   { transform: translateY(12px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}

.action-effect {
    animation: pixel-pop 0.45s ease-out,
               pixel-flash 0.8s ease-in-out 2;
    border: 3px solid #ffd166;
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    background: #243d60;
    text-align: center;
    box-shadow: 4px 4px 0 #091321;
}

.action-effect .big-icon {
    font-size: 48px;
    animation: pixel-float 0.4s ease-out;
}

.action-effect p {
    margin-bottom: 0;
}

.action-alert {
    border-color: #ff5555;
    background: #632b3b;
}

.action-success {
    border-color: #55e6a5;
    background: #174b43;
}

<style>
.stApp {
    background: #101b2b;
    color: #f4f7ff;
}
h1, h2, h3, p, label {
    color: #f4f7ff;
}
div.stButton > button {
    min-height: 54px;
    border: 2px solid #6fa8ff;
    border-radius: 7px;
    font-weight: bold;
    background: #203c63;
    color: white;
}
div.stButton > button:hover {
    border-color: #ffd166;
    color: #ffd166;
}
.pixel-panel {
    background: #172b45;
    border: 3px solid #4d8bdf;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 4px 4px 0 #091321;
}
.pixel-note {
    color: #c4d8f5;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("📝 GIAN LẬN TRONG THI")
st.caption(
    "PIXEL CLASSROOM • 2D TOP-DOWN • "
    "Game mô phỏng vui nhộn"
)

LEVELS = {
    "Dễ": {
        "suspicion": 5,
        "energy": 100,
        "target": 50,
        "risk": 0.12
    },
    "Trung bình": {
        "suspicion": 15,
        "energy": 90,
        "target": 70,
        "risk": 0.25
    },
    "Khó": {
        "suspicion": 25,
        "energy": 80,
        "target": 90,
        "risk": 0.40
    }
}

SCENES = [
    "Giám thị đang đi quanh lớp.",
    "Cả phòng thi im lặng. Bạn nghe tiếng đồng hồ tích tắc.",
    "Giám thị dừng lại gần một dãy bàn.",
    "Một bạn học sinh đang loay hoay với đề thi.",
    "Tiếng bước chân vang lên ở cuối lớp.",
    "Bạn cần bình tĩnh để hoàn thành bài thi."
]


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
    st.session_state.scene = random.choice(SCENES)
    st.session_state.log = [
        "🔔 Tiếng trống vang lên! Kỳ thi bắt đầu."
    ]


def draw_classroom():
    # Vẽ phòng học bằng các hình khối pixel.
    parts = []

    parts.append("""
    <div style="width:100%;overflow-x:auto;">
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 680 390"
         style="width:100%;height:auto;display:block;
                image-rendering:pixelated;border:4px solid #4d8bdf;
                border-radius:5px;">
      <defs>
        <pattern id="floor" width="48" height="36"
                 patternUnits="userSpaceOnUse">
          <rect width="48" height="36" fill="#b99a76"/>
          <path d="M0 0H48 M0 36H48 M24 0V18 M0 18H48"
                stroke="#8c7158" stroke-width="1"/>
        </pattern>
      </defs>

      <rect width="680" height="390" fill="url(#floor)"/>

      <!-- Tường trên lớp -->
      <rect x="0" y="0" width="680" height="54"
            fill="#674b3d"/>
      <rect x="0" y="48" width="680" height="10"
            fill="#dfb88b"/>

      <!-- Cửa sổ -->
      <rect x="12" y="8" width="66" height="38"
            fill="#8bd8f5" stroke="#f5d8a8" stroke-width="5"/>
      <path d="M45 8V46 M12 27H78"
            stroke="#e7f3ff" stroke-width="4"/>

      <!-- Bảng đen -->
      <rect x="174" y="7" width="320" height="52"
            fill="#5c3827" stroke="#d6a36d" stroke-width="4"/>
      <rect x="182" y="13" width="304" height="39"
            fill="#185b45"/>
      <path d="M200 24h58m-30 10h80m80-8h55m-190 12h90"
            stroke="#c8e5bb" stroke-width="2"
            stroke-dasharray="12 5"/>

      <!-- Cửa lớp -->
      <rect x="600" y="5" width="65" height="49"
            fill="#64432f" stroke="#e8c69c" stroke-width="4"/>
      <rect x="608" y="11" width="49" height="37"
            fill="#a4d8f4"/>
      <circle cx="649" cy="31" r="3" fill="#f9dc75"/>

      <!-- Bàn giáo viên -->
      <rect x="270" y="66" width="150" height="35"
            fill="#86502d" stroke="#50301f" stroke-width="4"/>
      <rect x="278" y="70" width="134" height="10"
            fill="#c58b4b"/>

      <!-- Giáo viên -->
      <rect x="328" y="54" width="24" height="23"
            fill="#e9b18b" stroke="#342b38" stroke-width="3"/>
      <rect x="324" y="51" width="32" height="10"
            fill="#30263a"/>
      <rect x="322" y="76" width="36" height="16"
            fill="#315ba8" stroke="#342b38" stroke-width="3"/>
      <rect x="325" y="91" width="9" height="8" fill="#292c42"/>
      <rect x="346" y="91" width="9" height="8" fill="#292c42"/>
      <rect x="334" y="62" width="4" height="4" fill="#30263a"/>
      <rect x="344" y="62" width="4" height="4" fill="#30263a"/>

    """)

    # Bàn học sinh theo lưới 4 cột x 3 hàng.
    xs = [65, 210, 355, 500]
    ys = [145, 220, 295]

    for row, y in enumerate(ys):
        for col, x in enumerate(xs):
            is_player = row == 1 and col == 1

            if is_player:
                parts.append(
                    f'<rect x="{x-7}" y="{y-28}" '
                    f'width="92" height="78" rx="4" '
                    f'fill="#ffe36e" opacity="0.35"/>'
                )
                parts.append(
                    f'<rect x="{x-7}" y="{y-28}" '
                    f'width="92" height="78" rx="4" '
                    f'fill="none" stroke="#ffdb4d" '
                    f'stroke-width="4"/>'
                )

            # Đầu và thân học sinh.
            skin = "#f0b58b"
            hair = "#382b30"
            shirt = (
                "#f6a23c" if is_player
                else random.choice([
                    "#477ecb", "#e16b52",
                    "#399d7c", "#8058b5"
                ])
            )

            parts.append(f"""
              <rect x="{x+27}" y="{y-24}"
                    width="20" height="19"
                    fill="{hair}"/>
              <rect x="{x+30}" y="{y-21}"
                    width="14" height="14"
                    fill="{skin}"/>
              <rect x="{x+32}" y="{y-16}"
                    width="3" height="3"
                    fill="#30263a"/>
              <rect x="{x+40}" y="{y-16}"
                    width="3" height="3"
                    fill="#30263a"/>
              <rect x="{x+25}" y="{y-5}"
                    width="24" height="19"
                    fill="{shirt}"
                    stroke="#49342b" stroke-width="2"/>
              <rect x="{x+28}" y="{y+13}"
                    width="7" height="8" fill="#33364a"/>
              <rect x="{x+40}" y="{y+13}"
                    width="7" height="8" fill="#33364a"/>
            """)

            # Mặt bàn và quyển đề thi.
            parts.append(f"""
              <rect x="{x}" y="{y+2}"
                    width="76" height="34"
                    fill="#80502f"
                    stroke="#493021" stroke-width="3"/>
              <rect x="{x+4}" y="{y+5}"
                    width="68" height="24"
                    fill="#d8a36b"/>
              <rect x="{x+25}" y="{y+9}"
                    width="25" height="15"
                    fill="#fff2ce"
                    stroke="#7c624b" stroke-width="1"/>
              <path d="M{x+29} {y+13}h16 M{x+29} {y+17}h12"
                    stroke="#8b8172" stroke-width="1"/>
              <rect x="{x+6}" y="{y+36}"
                    width="5" height="8" fill="#493021"/>
              <rect x="{x+65}" y="{y+36}"
                    width="5" height="8" fill="#493021"/>
            """)

    # Nhãn nhân vật người chơi.
    parts.append("""
      <rect x="204" y="187" width="88" height="20"
            fill="#172b45" stroke="#ffdb4d" stroke-width="2"/>
      <text x="248" y="201" text-anchor="middle"
            font-size="11" font-weight="bold"
            fill="#ffeb8a">BẠN</text>
      <rect x="320" y="111" width="40" height="15"
            fill="#173f32"/>
      <text x="340" y="122" text-anchor="middle"
            font-size="9" fill="#ffffff">GV</text>
    </svg>
    </div>
    """)

    st.markdown("".join(parts), unsafe_allow_html=True)


# =========================
# 2. KHỞI TẠO VÁN CHƠI
# =========================

if "status" not in st.session_state:
    new_game("Dễ")


# =========================
# 3. THANH CÀI ĐẶT
# =========================

with st.sidebar:
    st.header("⚙️ CÀI ĐẶT GAME")

    selected_level = st.selectbox(
        "Chọn độ khó",
        ["Dễ", "Trung bình", "Khó"],
        index=["Dễ", "Trung bình", "Khó"].index(
            st.session_state.level
        ),
        key="level_choice"
    )

    st.write("### 📜 Luật chơi")
    st.write("- Một ván có 8 lượt.")
    st.write("- Điểm đạt mục tiêu để thắng.")
    st.write("- Nghi ngờ chạm 100: bị phát hiện.")
    st.write("- Thể lực về 0: không thể tiếp tục.")
    st.write("- Mỗi hành động đều có thể tạo ra sự kiện.")

    if st.button("🔄 Bắt đầu ván mới", use_container_width=True):
        new_game(selected_level)
        st.rerun()


# =========================
# 4. THANH TRẠNG THÁI
# =========================

m1, m2, m3, m4 = st.columns(4)

m1.metric("📚 ĐIỂM SỐ", st.session_state.score)
m2.metric("👀 NGHI NGỜ", f"{st.session_state.suspicion}/100")
m3.metric("⚡ THỂ LỰC", f"{st.session_state.energy}/100")
m4.metric(
    "⏱️ LƯỢT",
    f"{min(st.session_state.turn, 8)}/8"
)

st.progress(st.session_state.suspicion / 100)
st.caption(
    f"Độ khó: {st.session_state.level} "
    f"• Mục tiêu: {st.session_state.target} điểm"
)


# =========================
# 5. KHÔNG GIAN LỚP HỌC
# =========================

left, right = st.columns([2.2, 1])

with left:
    st.subheader("🏫 LỚP HỌC 2D PIXEL ART")
    draw_classroom()

    st.markdown(
        f'<div class="pixel-panel">'
        f'<b>🔔 Tình huống hiện tại</b><br>'
        f'<span class="pixel-note">{st.session_state.scene}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

with right:
    st.subheader("📋 NHẬT KÝ")

    with st.container(border=True):
        for item in st.session_state.log[:7]:
            st.write("• " + item)

    st.subheader("🎯 NHIỆM VỤ")

    st.write(
        f"Đạt ít nhất **{st.session_state.target} điểm** "
        "trước khi kết thúc kỳ thi."
    )

    st.progress(
        min(
            st.session_state.score / st.session_state.target,
            1.0
        )
    )

    st.write(
        f"Tiến độ: {st.session_state.score}/"
        f"{st.session_state.target} điểm"
    )


# =========================
# 6. XỬ LÝ HÀNH ĐỘNG
# =========================

def take_action(action):
    risk = st.session_state.risk
    event = ""

    if action == "Tự làm bài nghiêm túc":
        points = random.randint(8, 15)
        st.session_state.score += points
        st.session_state.energy -= 12
        event = f"Bạn tập trung làm bài, được +{points} điểm."

    elif action == "Bình tĩnh suy nghĩ":
        points = random.randint(4, 10)
        st.session_state.score += points
        st.session_state.energy -= 6
        st.session_state.suspicion -= 5
        event = f"Bạn suy nghĩ cẩn thận, được +{points} điểm."

    elif action == "Lén xem tài liệu":
        points = random.randint(12, 23)
        st.session_state.score += points
        st.session_state.energy -= 8

        increase = random.randint(12, 24)
        st.session_state.suspicion += increase
        event = (
            f"Bạn kiếm được +{points} điểm, "
            f"nhưng mức nghi ngờ tăng {increase}."
        )

    elif action == "Nghỉ ngơi lấy sức":
        recovery = random.randint(15, 24)
        st.session_state.energy += recovery
        st.session_state.suspicion -= 3
        event = f"Bạn nghỉ ngơi và hồi phục {recovery} thể lực."

    # Sự kiện bất ngờ trong phòng thi.
    if random.random() < risk:
        increase = random.randint(5, 12)
        st.session_state.suspicion += increase
        event += f" Sự kiện bất ngờ: nghi ngờ tăng {increase}."

    # Giới hạn chỉ số trong khoảng hợp lệ.
    st.session_state.suspicion = max(
        0, min(100, st.session_state.suspicion)
    )
    st.session_state.energy = max(
        0, min(100, st.session_state.energy)
    )

    st.session_state.log.insert(0, event)

    # Kiểm tra điều kiện kết thúc.
    if st.session_state.suspicion >= 100:
        st.session_state.status = "caught"

    elif st.session_state.energy <= 0:
        st.session_state.status = "exhausted"

    elif st.session_state.turn >= st.session_state.max_turns:
        st.session_state.status = "finished"

    else:
        st.session_state.turn += 1
        st.session_state.scene = random.choice(SCENES)


# =========================
# 7. CÁC NÚT ĐIỀU KHIỂN
# =========================

st.divider()
st.subheader("🎮 BẠN MUỐN LÀM GÌ TRONG LƯỢT NÀY?")

if st.session_state.status == "playing":
    actions = [
        ("📖", "Tự làm bài nghiêm túc"),
        ("🧠", "Bình tĩnh suy nghĩ"),
        ("👀", "Lén xem tài liệu"),
        ("☕", "Nghỉ ngơi lấy sức")
    ]

    cols = st.columns(4)

    for i, (emoji, action) in enumerate(actions):
        with cols[i]:
            if st.button(
                f"{emoji}\n{action}",
                key=f"action_{i}",
                use_container_width=True
            ):
                take_action(action)
                st.rerun()

else:
    if st.session_state.status == "caught":
        st.error("🚨 Bạn đã bị giám thị phát hiện!")

    elif st.session_state.status == "exhausted":
        st.warning("😵 Bạn đã hết thể lực!")

    elif st.session_state.score >= st.session_state.target:
        st.success("🏆 Chiến thắng! Bạn đã đạt mục tiêu điểm!")

    else:
        st.warning(
            "📘 Kỳ thi kết thúc. Bạn chưa đạt mục tiêu điểm."
        )

    st.write(f"**Tổng điểm:** {st.session_state.score}")
    st.write(f"**Mức nghi ngờ:** {st.session_state.suspicion}/100")

    if st.button("🔁 CHƠI LẠI", type="primary"):
        new_game(st.session_state.level)
        st.rerun()


st.divider()
st.caption(
    "GIAN LẬN TRONG THI • Phiên bản 2D Pixel Art 1.0"
)
