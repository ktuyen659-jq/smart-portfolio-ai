import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import streamlit as st

# Cấu hình trang Web App
st.set_page_config(
    page_title="SmartPortfolio AI - XSTK & QTKD", page_icon="📊", layout="wide"
)

# Tiêu đề ứng dụng
st.title("📊 SmartPortfolio AI: Ứng Dụng Xác Suất Thống Kê Trong QTKD")
st.caption(
    "Hệ thống Tối ưu hóa Danh mục Đầu tư & Thư viện Trực quan hóa Khái niệm XSTK"
)

# Thanh điều hướng các Tab chức năng
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Bộ Tính Toán & Tối Ưu (QTKD)",
    "📈 Biểu Đồ Phân Phối Chuẩn",
    "🤖 Thư Viện Prompt AI (File 2)",
    "📄 Slide & Báo Cáo Chi Tiết (File 1 & 3)",
])

# ==========================================
# TAB 1: BỘ TÍNH TOÁN & TỐI ƯU HÓA DANH MỤC
# ==========================================
with tab1:
  st.header("1. Bài Toán Tối Ưu Hóa Danh Mục Đầu Tư Liên Thị Trường")
  st.write(
      "Nhập các tham số thị trường để tính toán Z-score, Xác suất an toàn và"
      " Tỷ trọng vốn tối ưu giúp tối thiểu hóa rủi ro."
  )

  col_in1, col_in2 = st.columns(2)
  with col_in1:
    st.subheader("🔹 Thị trường A")
    er_a = st.number_input("Lợi nhuận kỳ vọng E(R_A) (%)", value=19.0, step=0.5)
    std_a = st.number_input(
        "Độ lệch chuẩn / Rủi ro Sigma_A (%)", value=6.0, step=0.5
    )

  with col_in2:
    st.subheader("🔹 Thị trường B")
    er_b = st.number_input("Lợi nhuận kỳ vọng E(R_B) (%)", value=22.0, step=0.5)
    std_b = st.number_input(
        "Độ lệch chuẩn / Rủi ro Sigma_B (%)", value=10.0, step=0.5
    )

  st.markdown("---")
  col_m1, col_m2 = st.columns(2)
  with col_m1:
    r_target = st.number_input(
        "🎯 Mức lợi nhuận mục tiêu tối thiểu (%)", value=10.0, step=0.5
    )
  with col_m2:
    rho_ab = st.slider(
        "🔗 Hệ số tương quan giữa 2 thị trường (Rho_AB)",
        min_value=-1.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
    )

  # Tính toán Thống kê cho từng thị trường đơn lẻ
  z_a = (r_target - er_a) / std_a
  prob_a = (1 - stats.norm.cdf(z_a)) * 100

  z_b = (r_target - er_b) / std_b
  prob_b = (1 - stats.norm.cdf(z_b)) * 100

  # Tính toán Tối ưu hóa Danh mục (Min Variance Portfolio)
  var_a = std_a**2
  var_b = std_b**2
  cov_ab = rho_ab * std_a * std_b

  denom = var_a + var_b - 2 * cov_ab
  if denom != 0:
    w_a = (var_b - cov_ab) / denom
    w_a = max(0.0, min(1.0, w_a))
  else:
    w_a = 0.5
  w_b = 1 - w_a

  er_p = w_a * er_a + w_b * er_b
  var_p = (w_a**2) * var_a + (w_b**2) * var_b + 2 * w_a * w_b * cov_ab
  std_p = np.sqrt(var_p) if var_p > 0 else 0.0

  z_p = (r_target - er_p) / std_p if std_p > 0 else 0.0
  prob_p = (1 - stats.norm.cdf(z_p)) * 100

  st.subheader("🏆 KẾT QUẢ TỐI ƯU HÓA TỔNG HỢP")
  kpi1, kpi2, kpi3, kpi4 = st.columns(4)
  kpi1.metric("Tỷ trọng Thị trường A", f"{w_a*100:.2f}%")
  kpi2.metric("Lợi nhuận Kỳ vọng E(R_p)", f"{er_p:.2f}%")
  kpi3.metric("Rủi ro Danh mục (Sigma_p)", f"{std_p:.2f}%")
  kpi4.metric("Xác suất An toàn (>=10%)", f"{prob_p:.2f}%")

  st.markdown("### 📋 Bảng So Sánh Chỉ Số Đối Chiếu")
  data_table = {
      "Chỉ tiêu Phân tích": [
          "Lợi nhuận kỳ vọng E(R)",
          "Độ lệch chuẩn / Rủi ro (Sigma)",
          "Giá trị chuẩn hóa Z-score",
          "Xác suất An toàn (>= 10%)",
      ],
      "Thị trường A (100% A)": [
          f"{er_a:.2f}%",
          f"{std_a:.2f}%",
          f"Z_A = {z_a:.2f}",
          f"{prob_a:.2f}%",
      ],
      "Thị trường B (100% B)": [
          f"{er_b:.2f}%",
          f"{std_b:.2f}%",
          f"Z_B = {z_b:.2f}",
          f"{prob_b:.2f}%",
      ],
      f"Danh mục Tối ưu ({w_a*100:.0f}% A + {w_b*100:.0f}% B)": [
          f"{er_p:.2f}%",
          f"{std_p:.2f}% (Rủi ro thấp nhất)",
          f"Z_p = {z_p:.2f}",
          f"{prob_p:.2f}% (An toàn nhất)",
      ],
  }
  st.table(data_table)

# ==========================================
# TAB 2: BIỂU ĐỒ PHÂN PHỐI CHUẨN
# ==========================================
with tab2:
  st.header("2. Trực Quan Hóa Đồ Thị Phân Phối Chuẩn N(mu, sigma^2)")

  fig, ax = plt.subplots(figsize=(10, 5))
  x = np.linspace(0, 35, 1000)

  y_a = stats.norm.pdf(x, er_a, std_a)
  y_b = stats.norm.pdf(x, er_b, std_b)
  y_p = stats.norm.pdf(x, er_p, std_p)

  ax.plot(x, y_a, label=f"Thị trường A N({er_a:.0f}, {std_a:.0f}^2)", color="blue")
  ax.plot(x, y_b, label=f"Thị trường B N({er_b:.0f}, {std_b:.0f}^2)", color="red")
  ax.plot(
      x,
      y_p,
      label=f"Danh mục Tối ưu N({er_p:.2f}, {std_p:.2f}^2)",
      color="green",
      linewidth=2.5,
  )

  ax.axvline(
      r_target,
      color="black",
      linestyle="--",
      label=f"Mục tiêu an toàn ({r_target}%)",
  )
  ax.fill_between(
      x,
      y_p,
      where=(x >= r_target),
      color="green",
      alpha=0.2,
      label="Xác suất an toàn Danh mục Tối ưu",
  )

  ax.set_title(
      "Đường Cong Phân Phối Chuẩn Lợi Nhuận & Vùng Xác Suất An Toàn", fontsize=12
  )
  ax.set_xlabel("Tỷ suất sinh lời (%)")
  ax.set_ylabel("Mật độ xác suất f(R)")
  ax.legend()
  ax.grid(True, alpha=0.3)

  st.pyplot(fig)

# ==========================================
# TAB 3: THƯ VIỆN PROMPT AI (FILE 2)
# ==========================================
with tab3:
  st.header("3. Thư Viện Prompt AI (Đáp ứng yêu cầu File 2 của Thầy)")
  st.write(
      "Bộ các câu lệnh Prompt thực tế đã sử dụng để chỉ đạo AI phân tích và"
      " biên soạn sản phẩm."
  )

  st.subheader("🤖 Group 1: Prompt Sản phẩm 1 (AI -> Khái niệm XSTK)")
  st.code(
      """
[PROMPT 1: Dùng ẩn dụ giải thích Kỳ vọng E(X) & Phương sai Var(X)]
Bạn là một giảng viên XSTK xuất sắc. Hãy giải thích khái niệm 'Kỳ vọng E(X)' và 'Phương sai Var(X)' cho sinh viên bằng ẩn dụ thực tế. Nêu rõ ý nghĩa phương sai trong đo lường rủi ro và cho 1 ví dụ số cụ thể.

[PROMPT 2: Giải thích Phân phối Chuẩn & Code Python]
Hãy giải thích khái niệm Phân phối chuẩn N(mu, sigma^2) và quy tắc chuẩn hóa Z-score. Viết đoạn code Python dùng matplotlib vẽ đồ thị hình chuông và tô màu vùng xác suất P(X >= a).
""",
      language="text",
  )

  st.subheader("🤖 Group 2: Prompt Sản phẩm 2 (AI -> Ngành QTKD)")
  st.code(
      """
[PROMPT 1: Phân tích Xác suất An toàn Z-score]
Cho Thị trường A (E=19%, std=6%) và Thị trường B (E=22%, std=10%). Dùng phân phối chuẩn N(mu, sigma^2) tính xác suất đạt lợi nhuận >= 10% của từng thị trường và rút ra nhận xét quản trị.

[PROMPT 2: Tối ưu hóa Tỷ trọng Vốn Min Variance]
Lập hàm phương sai danh mục kết hợp sigma_p^2 = w_A^2 * 36 + (1-w_A)^2 * 100. Dùng đạo hàm d(sigma_p^2)/dw_A = 0 để tìm tỷ trọng vốn w_A tối ưu giúp tối thiểu hóa rủi ro.

[PROMPT 3: Viết Báo cáo Quản trị Danh mục Markowitz]
Viết bản báo cáo hoàn chỉnh cho giảng viên tổng hợp bài học quản trị kinh doanh: Đa dạng hóa danh mục giúp triệt tiêu rủi ro phi hệ thống mà vẫn giữ mức sinh lời tối ưu.
""",
      language="text",
  )

# ==========================================
# TAB 4: SLIDE & BÁO CÁO CHI TIẾT (FILE 1 & 3)
# ==========================================
with tab4:
  st.header("4. Trung Tâm Tài Liệu Báo Cáo & Slide Thuyết Trình")

  st.subheader("📄 Dàn Ý Slide Thuyết Trình (Đáp ứng File Slide)")
  st.markdown("""
    * **Slide 1:** Tiêu đề Đề tài: Ứng dụng XSTK & Phân phối chuẩn trong Quản trị Danh mục Đầu tư.
    * **Slide 2:** Bối cảnh Kinh doanh & Dữ liệu Đầu vào (Thị trường A & B).
    * **Slide 3:** Phân tích Xác suất An toàn Z-score ($P(R \ge 10\%)$).
    * **Slide 4:** Mô hình Tối ưu hóa Tỷ trọng Vốn ($w_A^* = 74\%$, $w_B^* = 26\%$).
    * **Slide 5:** Bảng So sánh Chỉ số & Kết luận Quản trị Markowitz.
    """)

  st.markdown("---")
  st.subheader("📝 Tóm Tắt Bài Báo Cáo Quản Trị (Đáp ứng File Sản Phẩm Cụ Thể)")
  st.info("""
    **Kết luận Quản trị Thực tiễn:**
    1. **Khi đầu tư đơn lẻ:** Thị trường A an toàn hơn Thị trường B (93.32% > 88.49%) do biến động nhỏ hơn (6% < 10%).
    2. **Đa dạng hóa vốn:** Phối hợp 74% A + 26% B kéo rủi ro xuống chỉ còn **5.15%** (thấp hơn cả thị trường A), đồng thời nâng xác suất an toàn lên **97.13%**.
    """)