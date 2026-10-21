import random
import streamlit as st
import streamlit.components.v1 as components


==========================================
st.set_page_config(
page_title="Dai chien phong thi",
page_icon="📝",
layout="wide"
)
==========================================
2. AM THANH TAO BANG TRINH DUYET
==========================================
def sound_effect(kind):
sounds = {
"click": (660, 0.08),
"bell": (880, 0.35),
"win": (1040, 0.45),
"lose": (180, 0.55),
"alert": (330, 0.30),
"rest": (520, 0.20),
}

    frequency, duration = sounds.get(kind, (440, 0.15))

html = f"""
    <html>
    <body style="margin:0;background:transparent">
    <button id="playSound"
        style="padding:8px 12px;border:1px solid #4b90e2;
        border-radius:5px;background:#12345c;color:white;
        cursor:pointer;font-weight:bold;">
        🔊 Phát âm thanh
    </button>
    <script>
    const button = document.getElementById("playSound");
    button.addEventListener("click", function() {{
        const AudioContextClass =
            window.AudioContext || window.webkitAudioContext;
        if (!AudioContextClass) return;

const ctx = new AudioContextClass();
        const oscillator = ctx.createOscillator();
        const gain = ctx.createGain();

oscillator.type = "square";
        oscillator.frequency.value = {frequency};
        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            0.001, ctx.currentTime + {duration}
        );

oscillator.connect(gain);
        gain.connect(ctx.destination);
        oscillator.start();
        oscillator.stop(ctx.currentTime + {duration});
        oscillator.onended = () => ctx.close();
    }});
    </script>
    </body>
    </html>
    """
    components.html(html, height=48)
==========================================
3. CSS PIXEL ART
==========================================
st.markdown("""

<style>
.stApp {
    background: #07162f;
    color: #eef5ff;
}
.block-container {
    max-width: 1450px;
    padding-top: 1rem;
}
.pixel-title {
    background: #102c59;
    border: 3px solid #428bff;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    font-size: 30px;
    font-weight: 900;
    color: white;
    box-shadow: 0 5px 0 #061025;
}
.game-panel {
    background: #10294d;
    border: 3px solid #397bd2;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
}
.room {
    background-color: #e9b77c;
    border: 6px solid #8a4f32;
    padding: 10px;
    text-align: center;
    color: #183153;
    background-image: repeating-linear-gradient(
        0deg, transparent, transparent 35px,
        rgba(120,65,32,.16) 36px, rgba(120,65,32,.16) 39px
    );
}
.blackboard {
    background: #155743;
    color: white;
    border: 7px solid #92592e;
    padding: 20px 5px;
    margin: 4px auto 14px;
    max-width: 520px;
    font-size: 24px;
    font-weight: bold;
}
.teacher {
    background: #f8d7da;
    border: 3px solid #842029;
    padding: 10px;
    margin: 8px auto;
    max-width: 220px;
    font-size: 27px;
}
.students {
    display: flex;
    justify-content: space-around;
    gap: 5px;
    margin: 10px 0;
}
.student {
    background: #ffda9a;
    border: 3px solid #87502d;
    padding: 10px 2px;
    flex: 1;
    font-size: 24px;
}
.desk {
    background: #bc753c;
    border: 3px solid #77431f;
    padding: 8px;
    color: white;
    margin: 5px;
}
.warning {
    background: #ffbaba;
    color: #820000;
    border: 3px solid #a40000;
    padding: 10px;
    font-weight: bold;
}
div.stButton > button {
    width: 100%;
    min-height: 45px;
    background: #173967;
    color: white;
    border: 2px solid #5799ef;
    border-radius: 5px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #285a9d;
    color: white;
}
div[data-testid="stMetric"] {
    background: #10294d;
    border: 2px solid #397bd2;
    padding: 8px;
    border-radius: 5px;
}
</style>


""", unsafe_allow_html=True)
==========================================
4. TAO GAME MOI
==========================================
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
    st.session_state.last_event = "Chuông báo giờ thi đã vang lên!"
    st.session_state.teacher_alert = False
    st.session_state.log = ["🔔 Bắt đầu ván chơi!"]

if "status" not in st.session_state:
    new_game("Dễ")
==========================================
5. XU LY HANH DONG
==========================================
def do_action(action):
if st.session_state.status != "playing":
return

score = st.session_state.score
    suspicion = st.session_state.suspicion
    energy = st.session_state.energy
    risk = st.session_state.risk
    event = ""
    alert = False

if action == "Làm bài":
        gain = random.randint(8, 15)
        score += gain
        energy -= random.randint(4, 9)
        suspicion = max(0, suspicion - 2)
        event = f"📚 Bạn tập trung làm bài, tăng {gain} điểm."

elif action == "Quan sát":
        energy -= 2
        suspicion = max(0, suspicion - random.randint(1, 5))
        event = "👀 Bạn quan sát giáo viên."

elif action == "Nghỉ ngơi":
        recovery = random.randint(10, 20)
        energy = min(100, energy + recovery)
        event = f"☕ Bạn hồi phục {recovery} thể lực."

elif action == "Tài liệu":
        gain = random.randint(10, 20)
        score += gain
        suspicion += random.randint(5, risk)
        energy -= 4
        event = f"📖 Bạn tăng {gain} điểm, nhưng nghi ngờ tăng."

elif action == "Trao đổi":
        energy -= 5
        if random.random() < 0.6:
            gain = random.randint(8, 16)
            score += gain
            event = f"🤝 Bạn nhận gợi ý, tăng {gain} điểm."
        else:
            suspicion += random.randint(10, risk + 5)
            event = "😰 Cuộc trao đổi khiến bạn bị chú ý."

score = max(0, score)
    suspicion = max(0, min(100, suspicion))
    energy = max(0, min(100, energy))

if suspicion >= 100:
        status = "lost"
        alert = True
        event += " 🚨 Giáo viên phát hiện bạn!"
    else:
        status = "playing"
        if suspicion >= 70 and random.random() < 0.5:
            alert = True
            event += " 👀 Giáo viên đang chú ý!"

st.session_state.score = score
    st.session_state.suspicion = suspicion
    st.session_state.energy = energy
    st.session_state.last_action = action
    st.session_state.last_event = event
    st.session_state.teacher_alert = alert
    st.session_state.status = status

if st.session_state.status == "playing":
        if score >= st.session_state.target:
            st.session_state.status = "won"
            st.session_state.last_event += " 🏆 Bạn chiến thắng!"
        elif energy <= 0:
            st.session_state.status = "lost"
            st.session_state.last_event += " 😵 Bạn hết thể lực!"
        elif st.session_state.turn >= st.session_state.max_turns:
            st.session_state.status = "lost"
            st.session_state.last_event += " ⏰ Hết lượt chơi!"

st.session_state.log.append(
        f"Lượt {st.session_state.turn}: {st.session_state.last_event}"
    )

if st.session_state.status == "playing":
        st.session_state.turn += 1
==========================================
6. TIEU DE VA DO KHO
==========================================
st.markdown(
'<div class="pixel-title">📝 ĐẠI CHIẾN PHÒNG THI<br>'
'<span style="font-size:15px;">'
'2D PIXEL ART • ĐIỂM SỐ • THỂ LỰC • NGHI NGỜ'
'</span></div>',
unsafe_allow_html=True
)

st.write("")
levels = ["Dễ", "Trung bình", "Khó"]
current_level = st.session_state.level
if current_level not in levels:
    current_level = "Dễ"

c1, c2 = st.columns([2, 1])
with c1:
    selected_level = st.selectbox(
        "🎯 Chọn độ khó",
        levels,
        index=levels.index(current_level)
    )
with c2:
    st.write("")
    if st.button("🔄 Chơi mới", use_container_width=True):
        new_game(selected_level)
        st.rerun()
==========================================
7. BAN DO LOP HOC
==========================================
left, right = st.columns([2.2, 1])

with left:
    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 🏫 Phòng thi Pixel Art")
    st.markdown('<div class="room">', unsafe_allow_html=True)

st.markdown(
        '<div class="blackboard">KỲ THI<br>'
        '<span style="font-size:13px;">'
        'TỰ TIN • BÌNH TĨNH • LÀM BÀI TỐT'
        '</span></div>',
        unsafe_allow_html=True
    )

st.markdown(
        '<div class="teacher">👩‍🏫<br>'
        '<span style="font-size:14px;color:#183153;">GIÁO VIÊN</span></div>',
        unsafe_allow_html=True
    )

if st.session_state.teacher_alert:
        st.markdown(
            '<div class="warning">🚨 GIÁO VIÊN ĐANG CHÚ Ý!</div>',
            unsafe_allow_html=True
        )

st.markdown(
        '<div class="students">'
        '<div class="student">🧑‍🎓<br><small>BẠN A</small></div>'
        '<div class="student">👩‍🎓<br><small>BẠN B</small></div>'
        '<div class="student">👨‍🎓<br><small>BẠN C</small></div>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown(
        '<div class="students">'
        '<div class="desk">🪑<br>📄 Bài thi</div>'
        '<div class="desk">🪑<br>✏️ Bút</div>'
        '<div class="desk">🪑<br>📄 Bài thi</div>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown(
        '<div class="students">'
        '<div class="student">🧑‍🎓<br><small>HỌC SINH</small></div>'
        '<div class="student">🧑‍🎓<br><small>🟡 BẠN</small></div>'
        '<div class="student">🧑‍🎓<br><small>HỌC SINH</small></div>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown(
        '<div class="desk">🪟 CỬA SỔ　 🪴 CÂY XANH　 🚪 CỬA RA VÀO</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
Bang chi so
st.markdown('<div class="game-panel">', unsafe_allow_html=True)
st.markdown("### 📊 Chỉ số người chơi")
a, b, c = st.columns(3)
a.metric("⭐ Điểm", st.session_state.score)
b.metric("👀 Nghi ngờ", f"{st.session_state.suspicion}/100")
c.metric("⚡ Thể lực", f"{st.session_state.energy}/100")

st.caption("Tiến độ mục tiêu")
    st.progress(min(st.session_state.score / st.session_state.target, 1.0))
    st.caption("Mức nghi ngờ")
    st.progress(st.session_state.suspicion / 100)
    st.caption("Thể lực")
    st.progress(st.session_state.energy / 100)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 🎮 Hành động")

if st.session_state.status == "playing":
        if st.button("📚 Tập trung làm bài", use_container_width=True):
            do_action("Làm bài")
            st.rerun()

if st.button("👀 Quan sát giáo viên", use_container_width=True):
            do_action("Quan sát")
            st.rerun()

if st.button("☕ Nghỉ ngơi", use_container_width=True):
            do_action("Nghỉ ngơi")
            st.rerun()

if st.button("📖 Xem tài liệu", use_container_width=True):
            do_action("Tài liệu")
            st.rerun()

if st.button("🤝 Trao đổi với bạn", use_container_width=True):
            do_action("Trao đổi")
            st.rerun()
    else:
        if st.session_state.status == "won":
            st.success("🏆 CHIẾN THẮNG!")
        else:
            st.error("❌ GAME OVER!")

if st.button("🎮 Chơi lại", use_container_width=True):
            new_game(selected_level)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 📜 Nhật ký")
    for entry in reversed(st.session_state.log[-7:]):
        st.write("• " + entry)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.markdown("### 💬 Sự kiện gần nhất")
    st.info(st.session_state.last_event)
    st.markdown('</div>', unsafe_allow_html=True)
==========================================
8. KHU VUC AM THANH
==========================================
st.markdown("---")
st.markdown("## 🔊 Trung tâm âm thanh")
st.write(
"Bấm nút phát âm thanh bên dưới. "
"Trình duyệt có thể yêu cầu tương tác trực tiếp trước khi phát."
)

s1, s2, s3 = st.columns(3)

with s1:
st.markdown("🔔 Chuông báo")
sound_effect("bell")

with s2:
st.markdown("🖱️ Tiếng bấm")
sound_effect("click")

with s3:
st.markdown("🏆 Âm thanh chiến thắng")
sound_effect("win")
==========================================
9. HUONG DAN
==========================================
with st.expander("❓ Hướng dẫn chơi"):
st.markdown("""
- 📚 Tập trung làm bài: Tăng điểm, tiêu hao thể lực.
- 👀 Quan sát giáo viên: Giảm nhẹ mức nghi ngờ.
- ☕ Nghỉ ngơi: Hồi phục thể lực.
- 📖 Xem tài liệu: Có thể tăng điểm nhưng tăng nghi ngờ.
- 🤝 Trao đổi với bạn: Có cơ hội tăng điểm nhưng cũng có rủi ro.

Chiến thắng: Đạt mục tiêu điểm số.

Thất bại: Bị phát hiện, hết thể lực hoặc hết lượt chơi.
""")
