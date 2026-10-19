
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
    "Dễ": {
        "suspicion": 10,
        "energy": 100,
        "target": 50,
        "risk": 0.15
    },
    "Trung bình": {
        "suspicion": 20,
        "energy": 85,
        "target": 70,
        "risk": 0.30
    },
    "Khó": {
        "suspicion": 35,
        "energy": 70,
        "target": 90,
        "risk": 0.45
    }
}



def new_game(level):
    settings = LEVELS[level]
    st.session_state.level = level
    st.session_state.score = 0
    st.session_state.suspicion = settings["suspicion"]
    st.session_state.energy = settings["energy"]
    st.session_state.turn = 1
    st.session_state.target = settings["target"]
    st.session_state.risk = settings["risk"]
    st.session_state.log = [
        "🔔 Tiếng trống vang lên! Kỳ thi bắt đầu."
    ]
    st.session_state.status = "playing"


if "status" not in st.session_state:
    new_game("Dễ")


with st.sidebar:
    st.header("⚙️ Cài đặt")
    selected_level = st.selectbox(
        "Chọn độ khó",
        list(LEVELS.keys()),
        index=list(LEVELS.keys()).index(
            st.session_state.level
        ),
        disabled=st.session_state.status == "playing"
    )

    st.write("**Luật chơi**")
    st.write("- Điểm càng cao càng tốt.")
    st.write("- Nghi ngờ đạt 100: bị phát hiện.")
    st.write("- Thể lực về 0: hết khả năng hành động.")
    st.write("- Hoàn thành 8 lượt để kết thúc kỳ thi.")

    if st.button("🔄 Chơi lại từ đầu", use_container_width=True):
        new_game(selected_level)
        st.rerun()


st.subheader(f"🎯 Độ khó: {st.session_state.level}")

col1, col2, col3 = st.columns(3)
col1.metric("📚 Điểm số", st.session_state.score)
col2.metric("👀 Nghi ngờ", f"{st.session_state.suspicion}/100")
col3.metric("⚡ Thể lực", f"{st.session_state.energy}/100")

st.progress(min(st.session_state.suspicion, 100) / 100)
st.caption("Thanh nghi ngờ càng đầy, nguy cơ bị giám thị phát hiện càng cao.")

if st.session_state.status == "playing":
    st.subheader(f"📖 Lượt {st.session_state.turn}/8")

    st.info(
        random.choice([
            "Giám thị đang đi quanh lớp.",
            "Một bạn bên cạnh đang loay hoay với đề thi.",
            "Cả phòng thi đang im lặng.",
            "Giám thị vừa nhìn về phía cuối lớp.",
            "Bạn cần bình tĩnh để hoàn thành bài thi."
        ])
        if "scene_turn" not in st.session_state
        or st.session_state.scene_turn != st.session_state.turn
        else st.session_state.scene
    )

    if (
        "scene_turn" not in st.session_state
        or st.session_state.scene_turn != st.session_state.turn
    ):
        st.session_state.scene = random.choice([
            "Giám thị đang đi quanh lớp.",
            "Một bạn bên cạnh đang loay hoay với đề thi.",
            "Cả phòng thi đang im lặng.",
            "Giám thị vừa nhìn về phía cuối lớp.",
            "Bạn cần bình tĩnh để hoàn thành bài thi."
        ])
        st.session_state.scene_turn = st.session_state.turn
        st.rerun()

    action = st.radio(
        "Bạn muốn làm gì trong lượt này?",
        [
            "📖 Tự làm bài nghiêm túc",
            "🧠 Bình tĩnh suy nghĩ",
            "👀 Quan sát tình hình",
            "☕ Nghỉ ngơi lấy sức"
        ]
    )

    if st.button("▶️ Thực hiện hành động", type="primary",
                 use_container_width=True):
        risk = st.session_state.risk
        event = ""

        if action == "📖 Tự làm bài nghiêm túc":
            points = random.randint(8, 16)
            st.session_state.score += points
            st.session_state.energy -= 12
            event = f"Bạn tập trung làm bài và được +{points} điểm."

        elif action == "🧠 Bình tĩnh suy nghĩ":
            points = random.randint(5, 12)
            st.session_state.score += points
            st.session_state.energy -= 7
            st.session_state.suspicion = max(
                0, st.session_state.suspicion - 5
            )
            event = f"Bạn suy nghĩ cẩn thận, được +{points} điểm và giảm nghi ngờ."

        elif action == "👀 Quan sát tình hình":
            if random.random() < risk:
                increase = random.randint(10, 22)
                st.session_state.suspicion += increase
                event = f"Giám thị chú ý đến bạn! Nghi ngờ tăng {increase}."
            else:
                st.session_state.suspicion = max(
                    0, st.session_state.suspicion - 8
                )
                event = "Bạn bình tĩnh trở lại. Mức nghi ngờ giảm 8."
            st.session_state.energy -= 5

        else:
            recovery = random.randint(12, 22)
            st.session_state.energy = min(
                100, st.session_state.energy + recovery
            )
            st.session_state.suspicion = max(
                0, st.session_state.suspicion - 3
            )
            event = f"Bạn nghỉ ngơi, hồi phục {recovery} thể lực."

        if random.random() < risk:
            extra = random.randint(3, 10)
            st.session_state.suspicion += extra
            event += f" Sự kiện bất ngờ: nghi ngờ tăng thêm {extra}."

        st.session_state.suspicion = min(
            100, max(0, st.session_state.suspicion)
        )
        st.session_state.energy = max(
            0, min(100, st.session_state.energy)
        )
        st.session_state.log.insert(0, event)

        if st.session_state.suspicion >= 100:
            st.session_state.status = "caught"
        elif st.session_state.energy <= 0:
            st.session_state.status = "exhausted"
        elif st.session_state.turn >= 8:
            st.session_state.status = "finished"
        else:
            st.session_state.turn += 1

        st.rerun()

else:
    st.subheader("🏁 Kết quả kỳ thi")

    if st.session_state.status == "caught":
        st.error("Bạn đã bị giám thị phát hiện!")
    elif st.session_state.status == "exhausted":
        st.warning("Bạn đã hết thể lực trước khi hoàn thành kỳ thi.")
    elif st.session_state.score >= st.session_state.target:
        st.success("🎉 Chúc mừng! Bạn đã hoàn thành kỳ thi với kết quả tốt.")
    else:
        st.warning("Bạn đã hoàn thành kỳ thi nhưng chưa đạt mục tiêu điểm.")

    st.write(f"**Tổng điểm:** {st.session_state.score}")
    st.write(f"**Mục tiêu:** {st.session_state.target} điểm")
    st.write(f"**Độ khó:** {st.session_state.level}")

    if st.button("🔁 Chơi lại", type="primary"):
        new_game(st.session_state.level)
        st.rerun()


st.divider()
st.subheader("📜 Nhật ký phòng thi")

for item in st.session_state.log[:8]:
    st.write("•", item)

st.caption("Đại chiến phòng thi — phiên bản 1.0")
