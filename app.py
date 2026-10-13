import io
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import streamlit as st
from gtts import gTTS

# Cấu hình trang Web App
st.set_page_config(
    page_title="SmartPortfolio AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS cho Hiệu ứng Banner & Card
st.markdown(
    """
<style>
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}
.banner {
    animation: pulse 3s infinite ease-in-out;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.user-card {
    background-color: #f0f2f6;
    padding: 15px 22px;
    border-radius: 10px;
    border-left: 5px solid #2a5298;
    margin-bottom: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)


# Hàm hỗ trợ phát âm giọng nói Tiếng Việt
def play_voice(text):
  try:
    tts = gTTS(text=text, lang="vi")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format="audio/mp3", autoplay=True)
  except Exception as e:
    st.warning("⚠️ Không thể phát giọng nói (Cần có kết nối Internet).")


# Session State quản lý Đăng nhập
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "user_role" not in st.session_state:
  st.session_state.user_role = "Sinh viên - QTKD"

# ==========================================
# GIAO DIỆN ĐĂNG NHẬP (USER LOGIN)
# ==========================================
if not st.session_state.logged_in:
  st.markdown(
      """
    <div class="banner">
        <h1>🤖 SMARTPORTFOLIO AI</h1>
        <h3>Trợ lý AI - Xác suất Thống kê & Quản trị Kinh doanh</h3>
    </div>
    """,
      unsafe_allow_html=True,
  )
  st.write("")

  col1, col2 = st.columns(2)
  with col1:
    st.info("""
        ### 👋 CHÀO MỪNG BẠN ĐẾN VỚI SMARTPORTFOLIO AI!
        
        ✨ **Tính năng mới cập nhật:**
        1. 🔑 **Đăng nhập tên người dùng** cá nhân hóa.
        2. 🖼️ **Giao diện hiệu ứng chuyển động (Animation Banner)**.
        3. 🔊 **Giao tiếp trả lời bằng Giọng nói AI (Vietnamese Voice)**.
        4. 📌 **Các Danh mục chính tích hợp trọn bộ 3 File theo yêu cầu của Thầy**.
        """)

  with col2:
    st.subheader("🔑 Đăng nhập Người dùng")
    u_name = st.text_input(
        "👤 Nhập Tên Người Dùng / Họ & Tên:", value="Nguyễn Văn A"
    )
    u_role = st.selectbox(
        "🎓 Vai trò / Ngành học:",
        [
            "Sinh viên - QTKD",
            "Sinh viên - Tài chính Ngân hàng",
            "Giảng viên",
            "Nhà nghiên cứu",
        ],
    )
    u_id = st.text_input("🆔 Mã Sinh Viên / Lớp:", value="QTKD-2026")

    if st.button(
        "🚀 BẮT ĐẦU TRẢI NGHIỆM WEB APP", type="primary", use_container_width=True
    ):
      if u_name.strip():
        st.session_state.logged_in = True
        st.session_state.username = u_name.strip()
        st.session_state.user_role = u_role
        st.rerun()
      else:
        st.error("Vui lòng nhập tên người dùng để tiếp tục!")

else:
  # ==========================================
  # KHU VỰC CHÍNH KHI ĐÃ ĐĂNG NHẬP
  # ==========================================
  st.sidebar.markdown(f"### 👤 Xin chào, **{st.session_state.username}**!")
  st.sidebar.caption(f"🎓 {st.session_state.user_role}")
  if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

  st.sidebar.markdown("---")
  st.sidebar.header("📌 CÁC DANH MỤC CHÍNH")
  nav = st.sidebar.radio(
      "Chọn danh mục trải nghiệm:",
      [
          "🏠 Trang chủ & Thống kê",
          "📘 Sản phẩm 1: AI & Khái niệm XSTK",
          "📊 Sản phẩm 2: QTKD & Tối ưu Danh mục Đầu tư",
          "🤖 Thư viện Prompt AI (File 2)",
          "📄 Slide & Báo cáo Chi tiết (File 1 & 3)",
      ],
  )

  st.markdown(
      f"""
    <div class="user-card">
        <h3>👋 Chào mừng <b>{st.session_state.username}</b> đến với SmartPortfolio AI!</h3>
        <p>Hệ thống đã sẵn sàng. Hãy chọn các danh mục chính bên thanh Menu để trải nghiệm tính năng Giọng nói AI và Tối ưu hóa Thống kê.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # 1. Trang chủ
  if nav == "🏠 Trang chủ & Thống kê":
    st.header("🏠 Tổng Quan Hệ Thống AI & XSTK")
    st.write("""
        Hệ thống **SmartPortfolio AI** tích hợp giao tiếp bằng giọng nói AI và phân tích XSTK ứng dụng trong Quản trị Kinh doanh:
        - **Sản phẩm 1 (AI -> XSTK):** Trợ lý AI giải thích khái niệm lý thuyết và **đọc lời thoại bằng giọng nói Tiếng Việt**.
        - **Sản phẩm 2 (AI -> QTKD):** Ứng dụng Phân phối Chuẩn & Cực trị Phương sai để tối ưu hóa danh mục đầu tư A & B.
        """)

    st.subheader("🔊 Trải nghiệm Trả lời bằng Giọng nói AI")
    welcome_text = (
        f"Xin chào {st.session_state.username}. Chào mừng bạn đến với ứng dụng"
        " Smart Portfolio AI. Hôm nay chúng ta sẽ cùng nghiên cứu ứng dụng xác"
        " suất thống kê vào quản trị kinh doanh."
    )
    if st.button("🎙️ Bấm để nghe AI Chào mừng & Giới thiệu"):
      play_voice(welcome_text)

  # 2. Sản phẩm 1
  elif nav == "📘 Sản phẩm 1: AI & Khái niệm XSTK":
    st.header("📘 Sản Phẩm 1: AI Trợ Giúp Học Khái Niệm XSTK")
    st.caption(
        "Khái niệm trọng tâm: Biến Ngẫu Nhiên, Kỳ vọng, Phương sai & Phân phối"
        " Chuẩn"
    )

    concept = st.selectbox(
        "Chọn khái niệm muốn học:",
        [
            "1. Biến ngẫu nhiên & Phân loại",
            "2. Kỳ vọng E(X) - Điểm cân bằng",
            "3. Phương sai Var(X) - Thước đo rủi ro",
            "4. Phân phối Chuẩn N(mu, sigma^2) & Z-score",
        ],
    )

    if "1. Biến" in concept:
      msg = (
          "Biến ngẫu nhiên là quy tắc gán mỗi kết quả của phép thử với một giá"
          " trị số. Gồm biến rời rạc đếm được và biến liên tục."
      )
      st.info(msg)
      if st.button("🔊 Nghe AI giải thích Biến ngẫu nhiên"):
        play_voice(msg)
    elif "2. Kỳ vọng" in concept:
      msg = (
          "Kỳ vọng E(X) đại diện cho giá trị trung bình dài hạn mà biến ngẫu"
          " nhiên đạt được. Trong kinh doanh, đó là lợi nhuận bình quân dự kiến."
      )
      st.success(msg)
      if st.button("🔊 Nghe AI giải thích Kỳ vọng E(X)"):
        play_voice(msg)
    elif "3. Phương sai" in concept:
      msg = (
          "Phương sai Var(X) đo lường độ phân tán quanh kỳ vọng. Trong tài"
          " chính, phương sai đại diện cho biên độ biến động và rủi ro."
      )
      st.warning(msg)
      if st.button("🔊 Nghe AI giải thích Phương sai & Rủi ro"):
        play_voice(msg)
    else:
      msg = (
          "Phân phối chuẩn có đồ thị dạng đường cong hình chuông đối xứng qua"
          " mu. Quy tắc Z-score giúp chuẩn hóa về phân phối chuẩn tắc N(0,1)."
      )
      st.error(msg)
      if st.button("🔊 Nghe AI giải thích Phân phối Chuẩn & Z-score"):
        play_voice(msg)

  # 3. Sản phẩm 2
  elif nav == "📊 Sản phẩm 2: QTKD & Tối ưu Danh mục Đầu tư":
    st.header("📊 Sản Phẩm 2: Tối Ưu Hóa Danh Mục Đầu Tư Liên Thị Trường")

    c1, c2 = st.columns(2)
    with c1:
      st.subheader("🔹 Thị trường A")
      er_a = st.number_input(
          "Lợi nhuận kỳ vọng E(R_A) (%)", value=19.0, step=0.5
      )
      std_a = st.number_input(
          "Độ lệch chuẩn / Rủi ro Sigma_A (%)", value=6.0, step=0.5
      )
    with c2:
      st.subheader("🔹 Thị trường B")
      er_b = st.number_input(
          "Lợi nhuận kỳ vọng E(R_B) (%)", value=22.0, step=0.5
      )
      std_b = st.number_input(
          "Độ lệch chuẩn / Rủi ro Sigma_B (%)", value=10.0, step=0.5
      )

    r_target = st.number_input(
        "🎯 Mức lợi nhuận an toàn mục tiêu (%):", value=10.0, step=0.5
    )

    # Tính toán
    z_a = (r_target - er_a) / std_a
    prob_a = (1 - stats.norm.cdf(z_a)) * 100

    z_b = (r_target - er_b) / std_b
    prob_b = (1 - stats.norm.cdf(z_b)) * 100

    var_a = std_a**2
    var_b = std_b**2
    w_a = var_b / (var_a + var_b)
    w_b = 1 - w_a

    er_p = w_a * er_a + w_b * er_b
    var_p = (w_a**2) * var_a + (w_b**2) * var_b
    std_p = np.sqrt(var_p)

    z_p = (r_target - er_p) / std_p
    prob_p = (1 - stats.norm.cdf(z_p)) * 100

    st.subheader("🏆 KẾT QUẢ TỐI ƯU HÓA DANH MỤC")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tỷ trọng Thị trường A", f"{w_a*100:.2f}%")
    k2.metric("Lãi Kỳ vọng Danh mục", f"{er_p:.2f}%")
    k3.metric("Rủi ro Danh mục (Sigma)", f"{std_p:.2f}%")
    k4.metric("Xác suất An toàn (>=10%)", f"{prob_p:.2f}%")

    # Vẽ biểu đồ Phân phối chuẩn
    fig, ax = plt.subplots(figsize=(9, 4))
    x_axis = np.linspace(0, 35, 500)
    ax.plot(
        x_axis,
        stats.norm.pdf(x_axis, er_a, std_a),
        label=f"Thị trường A ({er_a:.0f}%, {std_a:.0f}%)",
        color="blue",
    )
    ax.plot(
        x_axis,
        stats.norm.pdf(x_axis, er_b, std_b),
        label=f"Thị trường B ({er_b:.0f}%, {std_b:.0f}%)",
        color="red",
    )
    ax.plot(
        x_axis,
        stats.norm.pdf(x_axis, er_p, std_p),
        label=f"Danh mục Tối ưu ({er_p:.2f}%, {std_p:.2f}%)",
        color="green",
        linewidth=2.5,
    )
    ax.axvline(
        r_target, color="black", linestyle="--", label=f"Mục tiêu ({r_target}%)"
    )
    ax.set_title("Đường Cong Phân Phối Chuẩn & Vùng Xác Suất An Toàn")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    speech_result = (
        f"Phân bổ {w_a*100:.0f}% vốn vào thị trường A và {w_b*100:.0f}% vào thị"
        " trường B giúp giảm rủi ro danh mục xuống mức thấp nhất là"
        f" {std_p:.2f}%, đồng thời đạt xác suất an toàn lên tới {prob_p:.2f}%."
    )
    if st.button("🎙️ Nghe AI đọc báo cáo kết quả tối ưu hóa"):
      play_voice(speech_result)
