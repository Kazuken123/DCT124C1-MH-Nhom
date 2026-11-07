#!/usr/bin/env python3
"""Build midterm presentation slides for DCT124C1 Machine Learning Project.

File: BaoCao_TienDo_GiuaKy_Nhom10.pptx
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette: Clean Academic Navy Theme
    COLOR_PRIMARY = RGBColor(24, 43, 73)      # Navy
    COLOR_SECONDARY = RGBColor(41, 128, 185)  # Muted Blue
    COLOR_ACCENT = RGBColor(230, 126, 34)     # Orange Accent
    COLOR_BG_LIGHT = RGBColor(248, 249, 250)  # Light gray
    COLOR_TEXT_DARK = RGBColor(44, 62, 80)    # Dark gray text
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_GRAY = RGBColor(127, 140, 141)

    def add_header(slide, title_text, category="BÁO CÁO TIẾN ĐỘ GIỮA KỲ"):
        # Header banner box
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        banner.fill.solid()
        banner.fill.fore_color.rgb = COLOR_PRIMARY
        banner.line.color.rgb = COLOR_PRIMARY

        # Category pill
        tf_cat = banner.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = Inches(0.8)
        tf_cat.margin_top = Inches(0.15)
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

        # Title
        p_title = tf_cat.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

        # Footer line
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.1), Inches(13.333), Inches(0.4))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = COLOR_BG_LIGHT
        footer_line.line.color.rgb = COLOR_BG_LIGHT
        
        tf_foot = footer_line.text_frame
        tf_foot.margin_left = Inches(0.8)
        tf_foot.margin_top = Inches(0.08)
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Môn học: Máy học (DCT124C1) | Đề tài: Dự đoán nguy cơ bỏ học sinh viên (UCI 697) | Nhóm 10"
        p_foot.font.size = Pt(10)
        p_foot.font.color.rgb = COLOR_GRAY

    # ==========================================================
    # SLIDE 1: Title Slide
    # ==========================================================
    slide_layout = prs.slide_layouts[6] # Blank
    s1 = prs.slides.add_slide(slide_layout)

    # Background panel
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY
    bg1.line.color.rgb = COLOR_PRIMARY

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.5), Inches(0.2), Inches(4.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_ACCENT
    bar.line.color.rgb = COLOR_ACCENT

    # Title text box
    tb1 = s1.shapes.add_textbox(Inches(1.6), Inches(1.5), Inches(10.5), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "TRƯỜNG ĐẠI HỌC SÀI GÒN - KHOA CÔNG NGHỆ THÔNG TIN"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACCENT

    p1 = tf1.add_paragraph()
    p1.text = "BÁO CÁO TIẾN ĐỘ GIỮA KỲ MÔN MÁY HỌC"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Đề tài: Dự đoán nguy cơ bỏ học và kết quả học tập của sinh viên"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(189, 195, 199)
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Predict Students' Dropout and Academic Success (Dataset UCI 697)"
    p3.font.size = Pt(14)
    p3.font.italic = True
    p3.font.color.rgb = RGBColor(149, 165, 166)
    p3.space_before = Pt(4)

    p4 = tf1.add_paragraph()
    p4.text = "Nhóm thực hiện: Nhóm 10 | Lớp học phần: DCT124C1\nThành viên: Dương Gia Phát (Trưởng nhóm), Lê Văn Hiếu, Văn Nguyễn Thành Đạt, Cái Trần Minh Tiến\nThời gian báo cáo: Tháng 11/2026"
    p4.font.size = Pt(13)
    p4.font.color.rgb = COLOR_WHITE
    p4.space_before = Pt(25)

    # ==========================================================
    # SLIDE 2: Bối cảnh & Mục tiêu bài toán
    # ==========================================================
    s2 = prs.slides.add_slide(slide_layout)
    add_header(s2, "1. Bối cảnh, Mục tiêu & Loại bài toán Machine Learning")

    # Box Left: Bối cảnh & Ý nghĩa
    box_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = COLOR_BG_LIGHT
    box_l.line.color.rgb = RGBColor(220, 224, 230)
    tfl = box_l.text_frame
    tfl.word_wrap = True
    tfl.margin_left = Inches(0.4)
    tfl.margin_top = Inches(0.3)
    
    pl0 = tfl.paragraphs[0]
    pl0.text = "BỐI CẢNH & Ý NGHĨA THỰC TIỄN"
    pl0.font.bold = True
    pl0.font.size = Pt(16)
    pl0.font.color.rgb = COLOR_PRIMARY

    items_l = [
        "Thực trạng: Tỷ lệ sinh viên đại học thôi học hoặc chậm tiến độ gây lãng phí nguồn lực đào tạo và ảnh hưởng lớn đến tương lai người học.",
        "Mục tiêu cốt lõi: Xây dựng hệ thống học máy phát hiện sớm sinh viên có nguy cơ bỏ học ngay trong năm học thứ nhất.",
        "Ý nghĩa ứng dụng: Giúp phòng đào tạo và cố vấn học tập chủ động can thiệp kịp thời (hỗ trợ học bổng, tư vấn tâm lý, gia hạn học phí) trước khi sinh viên quyết định thôi học.",
        "Thời điểm ứng dụng thực tế: Cuối học kỳ 2 năm thứ nhất (khi đã có kết quả học tập ban đầu)."
    ]
    for it in items_l:
        p = tfl.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(12)

    # Box Right: Định nghĩa bài toán ML
    box_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = COLOR_BG_LIGHT
    box_r.line.color.rgb = RGBColor(220, 224, 230)
    tfr = box_r.text_frame
    tfr.word_wrap = True
    tfr.margin_left = Inches(0.4)
    tfr.margin_top = Inches(0.3)

    pr0 = tfr.paragraphs[0]
    pr0.text = "ĐẶC TẢ BÀI TOÁN HỌC MÁY"
    pr0.font.bold = True
    pr0.font.size = Pt(16)
    pr0.font.color.rgb = COLOR_PRIMARY

    items_r = [
        "Loại bài toán: Phân loại đa lớp có giám sát (Supervised Multi-class Classification).",
        "Đầu vào (Input): 36 đặc trưng bao gồm nhân khẩu học, kinh tế xã hội, điểm thi đầu vào và điểm số/tín chỉ tích lũy HK1 & HK2.",
        "Đầu ra (Output / Target): Dự đoán 1 trong 3 trạng thái của sinh viên:\n  1. Graduate (Tốt nghiệp)\n  2. Dropout (Thôi học / Bỏ học)\n  3. Enrolled (Còn đang theo học / nợ môn)",
        "Thách thức kỹ thuật lớn nhất: Mất cân bằng lớp và sự nhập nhằng ranh giới thuộc tính của nhóm sinh viên Enrolled."
    ]
    for it in items_r:
        p = tfr.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(12)

    # ==========================================================
    # SLIDE 3: Mô tả dữ liệu & Phân phối biến mục tiêu
    # ==========================================================
    s3 = prs.slides.add_slide(slide_layout)
    add_header(s3, "2. Mô tả dữ liệu & Kiểm toán toàn vẹn (UCI 697)")

    # Left: Data description
    box_d = s3.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.4))
    tfd = box_d.text_frame
    tfd.word_wrap = True
    
    pd0 = tfd.paragraphs[0]
    pd0.text = "ĐẶC ĐIỂM BỘ DỮ LIỆU GỐC"
    pd0.font.bold = True
    pd0.font.size = Pt(16)
    pd0.font.color.rgb = COLOR_PRIMARY

    d_items = [
        "Nguồn dữ liệu: Kho học thuật UCI Machine Learning Repository (Dataset ID: 697, DOI: 10.24432/C5MC89).",
        "Quy mô: 4.424 mẫu quan sát, 36 thuộc tính đầu vào và 1 cột nhãn Target.",
        "Chất lượng dữ liệu: 0 giá trị khuyết thiếu (0 missing value), 0 bản ghi trùng lặp.",
        "Phân loại 36 đặc trưng:\n  - 18 biến số liên tục/rời rạc (điểm số, số tín chỉ, độ tuổi...)\n  - 10 biến phân loại danh mục (ngành học, nghề nghiệp bố mẹ...)\n  - 8 biến nhị phân (giới tính, học bổng, nợ học phí...)",
        "Kiểm toán toàn vẹn dữ liệu: Mã băm SHA-256 cố định chống sai lệch dữ liệu: 3ef126de...4c45ae.",
        "Phân phối mục tiêu lệch lớp: Graduate chiếm 49,93%, Dropout chiếm 32,12%, Enrolled chiếm 17,95%."
    ]
    for it in d_items:
        p = tfd.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(8)

    # Right: Chart Image 1
    if os.path.exists("figures_report/fig1_target_distribution.png"):
        s3.shapes.add_picture("figures_report/fig1_target_distribution.png", Inches(6.8), Inches(1.6), width=Inches(5.8))

    # ==========================================================
    # SLIDE 4: Khám phá dữ liệu EDA & Insights then chốt
    # ==========================================================
    s4 = prs.slides.add_slide(slide_layout)
    add_header(s4, "3. Khám phá dữ liệu (EDA) & Các phát hiện then chốt")

    box_eda = s4.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))
    tf_eda = box_eda.text_frame
    tf_eda.word_wrap = True

    p_eda0 = tf_eda.paragraphs[0]
    p_eda0.text = "CÁC PHÁT HIỆN THỰC NGHIỆM TRÊN TẬP HUẤN LUYỆN"
    p_eda0.font.bold = True
    p_eda0.font.size = Pt(16)
    p_eda0.font.color.rgb = COLOR_PRIMARY

    eda_items = [
        "Điểm số học tập quyết định sống còn: Sinh viên có điểm số trung bình học kỳ 2 bằng 0 có tỷ lệ bỏ học lên tới 83,40%. Tín chỉ tích lũy HK2 là đặc trưng có lực phân tách mạnh nhất.",
        "Yếu tố tài chính (Nợ học phí): Sinh viên nợ học phí có tỷ lệ Dropout lên tới 64,01% (so với chỉ 28,19% ở nhóm đóng học phí đầy đủ).",
        "Tương quan điểm số chặt chẽ: Điểm số và số tín chỉ đạt giữa HK1 và HK2 có hệ số tương quan Pearson từ r = 0,84 đến 0,94.",
        "Quyết định tiền xử lý ngoại lệ (Outliers): Nhóm giữ nguyên 100% các giá trị ngoại lệ (tính theo 1.5 IQR) vì đây là các trường hợp sinh viên học xuất sắc hoặc học kém thực tế.",
        "Đề xuất tạo đặc trưng mới (Feature Engineering):\n  - Tỷ lệ tín chỉ hoàn thành HK1 và HK2 (approved / enrolled)\n  - Độ chênh lệch điểm trung bình giữa hai học kỳ (grade diff)"
    ]
    for it in eda_items:
        p = tf_eda.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(8)

    # Right: Chart Image 2
    if os.path.exists("figures_report/fig2_eda_correlation.png"):
        s4.shapes.add_picture("figures_report/fig2_eda_correlation.png", Inches(6.9), Inches(1.7), width=Inches(5.7))

    # ==========================================================
    # SLIDE 5: Pipeline tiền xử lý & Chiến lược kiểm định
    # ==========================================================
    s5 = prs.slides.add_slide(slide_layout)
    add_header(s5, "4. Pipeline tiền xử lý & Chiến lược thẩm định chống rò rỉ")

    # 3 Column Cards
    col_w = Inches(3.7)
    gap = Inches(0.3)
    
    # Card 1: Data split
    c1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), col_w, Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_BG_LIGHT
    c1.line.color.rgb = RGBColor(220, 224, 230)
    t1 = c1.text_frame
    t1.word_wrap = True
    t1.margin_left = Inches(0.3)
    t1.margin_top = Inches(0.3)
    p = t1.paragraphs[0]
    p.text = "PHÂN CHIA DỮ LIỆU"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_PRIMARY
    
    t1_items = [
        "Phân chia phân tầng (Stratified) theo biến mục tiêu Target.",
        "Tập huấn luyện (Train): 3.539 mẫu (80%).",
        "Tập kiểm tra (Test): 885 mẫu (20%) cố định Seed 42.",
        "Cam kết liêm chính: Tập Test được bảo lưu hoàn toàn kín, chưa đụng tới ở giữa kỳ.",
        "Toàn bộ lựa chọn tham số chỉ thực hiện trên tập Train."
    ]
    for it in t1_items:
        pi = t1.add_paragraph()
        pi.text = "• " + it
        pi.font.size = Pt(12)
        pi.space_before = Pt(8)

    # Card 2: Preprocessing pipeline
    c2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + col_w + gap, Inches(1.5), col_w, Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_BG_LIGHT
    c2.line.color.rgb = RGBColor(220, 224, 230)
    t2 = c2.text_frame
    t2.word_wrap = True
    t2.margin_left = Inches(0.3)
    t2.margin_top = Inches(0.3)
    p = t2.paragraphs[0]
    p.text = "TIỀN XỬ LÝ (PIPELINE)"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_PRIMARY

    t2_items = [
        "Đóng gói hoàn toàn trong scikit-learn Pipeline.",
        "Chuẩn hóa biến số (StandardScaler): fit độc lập trên từng fold huấn luyện, chống rò rỉ dữ liệu.",
        "Mã hóa biến danh mục: OneHotEncoder (bỏ qua giá trị lạ).",
        "Biến nhị phân: passthrough giữ nguyên giá trị 0/1.",
        "Feature Engineering: 3 đặc trưng tỷ lệ qua môn và chênh lệch điểm (an toàn mẫu số = 0)."
    ]
    for it in t2_items:
        pi = t2.add_paragraph()
        pi.text = "• " + it
        pi.font.size = Pt(12)
        pi.space_before = Pt(8)

    # Card 3: Validation Strategy
    c3 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (col_w + gap)*2, Inches(1.5), col_w, Inches(5.2))
    c3.fill.solid()
    c3.fill.fore_color.rgb = COLOR_BG_LIGHT
    c3.line.color.rgb = RGBColor(220, 224, 230)
    t3 = c3.text_frame
    t3.word_wrap = True
    t3.margin_left = Inches(0.3)
    t3.margin_top = Inches(0.3)
    p = t3.paragraphs[0]
    p.text = "CHIẾN LƯỢC KIỂM ĐỊNH"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_PRIMARY

    t3_items = [
        "5-Fold Stratified Cross-Validation dùng chung cho mọi mô hình.",
        "Độ đo đánh giá trọng tâm: Macro-F1 (đánh giá công bằng giữa các lớp lệch nhau).",
        "Độ đo bổ trợ: Accuracy, Precision/Recall riêng từng lớp, ma trận nhầm lẫn Out-of-fold.",
        "Độ lệch chuẩn: tính thống nhất với bậc tự do ddof=0.",
        "Kiểm soát Overfitting qua chỉ số chênh lệch Train-Validation Gap."
    ]
    for it in t3_items:
        pi = t3.add_paragraph()
        pi.text = "• " + it
        pi.font.size = Pt(12)
        pi.space_before = Pt(8)

    # ==========================================================
    # SLIDE 6: Bảng so sánh kết quả 12 lượt chạy thực nghiệm
    # ==========================================================
    s6 = prs.slides.add_slide(slide_layout)
    add_header(s6, "5. Kết quả thực nghiệm: Bảng so sánh 12 lượt chạy mô hình")

    # Table of models
    table_shape = s6.shapes.add_table(13, 7, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    table = table_shape.table

    # Column widths
    widths = [Inches(0.6), Inches(3.2), Inches(1.2), Inches(1.4), Inches(1.3), Inches(1.4), Inches(2.6)]
    for idx, w in enumerate(widths):
        table.columns[idx].width = w

    headers = ["STT", "Mô hình & Phiên bản", "Macro-F1", "Độ lệch chuẩn", "Accuracy", "Recall Dropout", "Đặc điểm cấu hình chính"]
    for idx, text in enumerate(headers):
        cell = table.cell(0, idx)
        cell.text = text
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    data = [
        ["1", "DummyClassifier v1 (Majority)", "0,2220", "0,0002", "49,93%", "0,00%", "Gán toàn bộ lớp Graduate"],
        ["2", "DummyClassifier v2 (Stratified)", "0,3383", "0,0092", "39,19%", "34,65%", "Ngẫu nhiên theo phân phối lớp"],
        ["3", "Decision Tree v1 (Gốc)", "0,6472", "0,0230", "73,69%", "70,10%", "Gini, max_depth=5, leaf=10"],
        ["4", "Decision Tree v2 (One-Hot)", "0,6586", "0,0186", "74,09%", "69,83%", "Thêm OneHotEncoder vào Pipeline"],
        ["5", "Decision Tree v2 (Nested Tuned)", "0,6783", "0,0097", "73,58%", "69,65%", "Nested CV: depth=7, ccp_alpha=0.002"],
        ["6", "Decision Tree v3 (Nông)", "0,6603", "0,0272", "73,64%", "65,61%", "Kế thừa v1, giảm max_depth=3"],
        ["7", "Random Forest v1 (100 cây)", "0,6852", "0,0239", "76,91%", "76,52%", "Mặc định không giới hạn độ sâu"],
        ["8", "Logistic Regression v1 (Chuẩn)", "0,6997", "0,0099", "77,54%", "77,48%", "C=1, L2, lbfgs, không trọng số"],
        ["9", "Logistic Regression v2 (Balanced)", "0,7067", "0,0143", "74,85%", "73,61%", "MÔ HÌNH TỐT NHẤT (class_weight='balanced')"],
        ["10", "XGBoost v1 (100 cây)", "0,6994", "0,0046", "77,71%", "76,07%", "100 cây, depth=3, lr=0.1, hist"],
        ["11", "LR Ablation B (Bỏ toàn bộ HK2)", "0,6578", "0,0149", "74,62%", "75,28%", "Đối chứng: F1 giảm 0.042 khi mất HK2"],
        ["12", "LR Ablation C (Thêm 3 đặc trưng)", "0,7031", "0,0110", "77,71%", "77,74%", "Thêm tỷ lệ qua môn và chênh lệch điểm"]
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, val in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if col_idx in [0, 2, 3, 4, 5]:
                p.alignment = PP_ALIGN.CENTER
            if row_idx == 9: # Best model
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(234, 250, 234)
                p.font.bold = True

    # ==========================================================
    # SLIDE 7: Trực quan hóa so sánh Macro-F1 & Nhận xét
    # ==========================================================
    s7 = prs.slides.add_slide(slide_layout)
    add_header(s7, "6. Trực quan hóa kết quả so sánh giữa các thuật toán")

    # Left: Image
    if os.path.exists("figures_report/fig3_model_macro_f1_comparison.png"):
        s7.shapes.add_picture("figures_report/fig3_model_macro_f1_comparison.png", Inches(0.8), Inches(1.5), width=Inches(6.8))

    # Right: Key insights
    box_s7 = s7.shapes.add_textbox(Inches(7.8), Inches(1.5), Inches(4.8), Inches(5.2))
    tfs7 = box_s7.text_frame
    tfs7.word_wrap = True

    p0 = tfs7.paragraphs[0]
    p0.text = "NHẬN XÉT ĐÁNH GIÁ CHÍNH"
    p0.font.bold = True
    p0.font.size = Pt(16)
    p0.font.color.rgb = COLOR_PRIMARY

    s7_items = [
        "Vượt trội hoàn toàn so với Baseline: Cả 4 họ thuật toán (LR, DT, RF, XGB) đều vượt xa mức sàn 0,2220 của DummyClassifier.",
        "Mô hình hiệu quả nhất: Logistic Regression v2 (class_weight='balanced') đạt Macro-F1 cao nhất (0,7067), vượt qua cả các mô hình phi tuyến và ensemble.",
        "Sức mạnh của XGBoost: Đạt Macro-F1 0,6994 với độ lệch chuẩn nhỏ nhất (0,0046), chứng tỏ tính ổn định cực cao giữa các fold.",
        "Cải tiến Decision Tree: Tinh chỉnh lồng nhau (Nested CV) giúp nâng Macro-F1 từ 0,6472 lên 0,6783 (+0,0311 điểm) và giảm độ phân tán từ 0,0230 xuống 0,0097."
    ]
    for it in s7_items:
        p = tfs7.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(12)
        p.space_before = Pt(10)

    # ==========================================================
    # SLIDE 8: Phân tích ma trận nhầm lẫn & Điểm nghẽn Enrolled
    # ==========================================================
    s8 = prs.slides.add_slide(slide_layout)
    add_header(s8, "7. Phân tích ma trận nhầm lẫn & Điểm nghẽn lớp Enrolled")

    # Left: Image
    if os.path.exists("figures_report/fig4_confusion_matrix_lr_v1_v2.png"):
        s8.shapes.add_picture("figures_report/fig4_confusion_matrix_lr_v1_v2.png", Inches(0.8), Inches(1.6), width=Inches(6.8))

    # Right: Breakdown
    box_s8 = s8.shapes.add_textbox(Inches(7.8), Inches(1.5), Inches(4.8), Inches(5.2))
    tfs8 = box_s8.text_frame
    tfs8.word_wrap = True

    p0 = tfs8.paragraphs[0]
    p0.text = "VÌ SAO ENROLLED LÀ ĐIỂM NGHẼN?"
    p0.font.bold = True
    p0.font.size = Pt(16)
    p0.font.color.rgb = COLOR_PRIMARY

    s8_items = [
        "Vùng chồng lấn thuộc tính: Sinh viên Enrolled có số tín chỉ tích lũy và điểm số nằm ở khoảng giao thoa giữa nhóm bỏ học và nhóm tốt nghiệp (rất khó phân định ranh giới).",
        "Hiệu năng trên mô hình tiêu chuẩn (LR v1): Chỉ nhận diện đúng 240/635 mẫu Enrolled (Recall chỉ đạt 37,80%), bỏ sót hơn 62% sinh viên đang gặp nguy cơ.",
        "Bước đột phá của LR v2 (Balanced): Bổ sung trọng số phạt đã tăng số ca đoán đúng lên 377 ca (Recall tăng vọt từ 37,80% lên 59,37%).",
        "Đánh đổi thực tế: Khi ưu tiên lớp Enrolled, số ca đoán nhầm giữa Dropout và Graduate có xu hướng tăng nhẹ. Đây là bài toán đánh đổi kinh điển trong học máy."
    ]
    for it in s8_items:
        p = tfs8.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(12)
        p.space_before = Pt(10)

    # ==========================================================
    # SLIDE 9: Kiểm toán Overfitting & Thí nghiệm đối chứng
    # ==========================================================
    s9 = prs.slides.add_slide(slide_layout)
    add_header(s9, "8. Kiểm toán học quá khớp (Overfitting) & Đối chứng Ablation")

    # Left: Image
    if os.path.exists("figures_report/fig5_train_val_gap_overfitting.png"):
        s9.shapes.add_picture("figures_report/fig5_train_val_gap_overfitting.png", Inches(0.8), Inches(1.6), width=Inches(6.5))

    # Right: Analysis
    box_s9 = s9.shapes.add_textbox(Inches(7.5), Inches(1.5), Inches(5.1), Inches(5.2))
    tfs9 = box_s9.text_frame
    tfs9.word_wrap = True

    p0 = tfs9.paragraphs[0]
    p0.text = "CẢNH BÁO QUÁ KHỚP & VAI TRÒ DỮ LIỆU"
    p0.font.bold = True
    p0.font.size = Pt(16)
    p0.font.color.rgb = COLOR_PRIMARY

    s9_items = [
        "Báo động Overfitting ở Random Forest v1:\n  - Trên tập Train: Macro-F1 = 1,0000 (Accuracy 100%)\n  - Trên tập Validation: Macro-F1 = 0,6852\n  -> Khoảng cách Train-Val Gap lên tới 31,48% (học vẹt dữ liệu do cây phát triển không giới hạn).",
        "Kiểm soát thành công ở Decision Tree:\n  - Cây gốc v1: Gap = 4,05%\n  - Cây tinh chỉnh v2: Gap = 3,05% (nhờ ccp_alpha)\n  - Cây nông v3 (depth=3): Gap gần như bằng 0.",
        "Ý nghĩa thực nghiệm Ablation Study:\n  - Thí nghiệm bỏ HK2 (Ablation B) khiến Macro-F1 giảm từ 0,6997 xuống 0,6578 (-0,0420 điểm).\n  - Kết luận: Không thể triển khai mô hình ngay lúc tân sinh viên nhập học mà bắt buộc phải chờ kết quả HK2."
    ]
    for it in s9_items:
        p = tfs9.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(11.5)
        p.space_before = Pt(8)

    # ==========================================================
    # SLIDE 10: Đánh giá tiến độ & Khó khăn hạn chế
    # ==========================================================
    s10 = prs.slides.add_slide(slide_layout)
    add_header(s10, "9. Đánh giá tiến độ giữa kỳ & Khó khăn hạn chế")

    box_ok = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    box_ok.fill.solid()
    box_ok.fill.fore_color.rgb = RGBColor(235, 247, 238)
    box_ok.line.color.rgb = RGBColor(163, 221, 179)
    tf_ok = box_ok.text_frame
    tf_ok.word_wrap = True
    tf_ok.margin_left = Inches(0.4)
    tf_ok.margin_top = Inches(0.3)
    p = tf_ok.paragraphs[0]
    p.text = "CÔNG VIỆC ĐÃ HOÀN THÀNH (100%)"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(39, 174, 96)

    ok_items = [
        "Thu thập và kiểm toán toàn vẹn dữ liệu gốc UCI 697.",
        "Thiết lập bộ chia 5 fold phân tầng chống rò rỉ dữ liệu.",
        "Hoàn thành khám phá EDA sâu và trực quan hóa chi tiết.",
        "Xây dựng xong 2 Baseline và 4 họ thuật toán (LR, DT, RF, XGB) với 12 lượt chạy thực nghiệm.",
        "Tinh chỉnh siêu tham số lồng nhau Nested CV thành công.",
        "Xây dựng script tự động run_all.py kiểm chứng toàn bộ chỉ trong 18 giây.",
        "Hoàn thành Báo cáo tiến độ Word 8 mục đạt chuẩn A4."
    ]
    for it in ok_items:
        pi = tf_ok.add_paragraph()
        pi.text = "✔ " + it
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = COLOR_TEXT_DARK
        pi.space_before = Pt(7)

    box_diff = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    box_diff.fill.solid()
    box_diff.fill.fore_color.rgb = RGBColor(254, 249, 231)
    box_diff.line.color.rgb = RGBColor(249, 231, 159)
    tf_diff = box_diff.text_frame
    tf_diff.word_wrap = True
    tf_diff.margin_left = Inches(0.4)
    tf_diff.margin_top = Inches(0.3)
    p = tf_diff.paragraphs[0]
    p.text = "KHÓ KHĂN & HẠN CHẾ THỰC TẾ"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(211, 84, 0)

    diff_items = [
        "Mất cân bằng lớp nghiêm trọng: Nhóm Enrolled chiếm tỷ lệ thấp (17,95%) khiến phần lớn mô hình khó nhận diện đúng nếu không can thiệp trọng số.",
        "Quá khớp ở Random Forest: Cần tinh chỉnh độ sâu max_depth và min_samples_leaf ở giai đoạn cuối kỳ để kéo train-val gap về mức an toàn.",
        "Phụ thuộc mốc thời gian học kỳ 2: Mô hình chưa thể ứng dụng sớm tại thời điểm nhập học.",
        "Tập kiểm tra 885 mẫu chưa chấm điểm: Cần giữ nguyên tắc đến cuối kỳ mới mở đánh giá độc lập một lần duy nhất."
    ]
    for it in diff_items:
        pi = tf_diff.add_paragraph()
        pi.text = "⚠ " + it
        pi.font.size = Pt(12)
        pi.font.color.rgb = COLOR_TEXT_DARK
        pi.space_before = Pt(12)

    # ==========================================================
    # SLIDE 11: Kế hoạch hoàn thành đề tài cuối kỳ
    # ==========================================================
    s11 = prs.slides.add_slide(slide_layout)
    add_header(s11, "10. Kế hoạch triển khai giai đoạn cuối kỳ")

    # 4 Phase Horizontal Cards
    card_w = Inches(2.7)
    card_gap = Inches(0.2)
    start_x = Inches(0.8)

    phases = [
        ("GIAI ĐOẠN 1", "08/11/2026", "Nộp Báo cáo giữa kỳ", [
            "Hoàn thiện file Word .docx",
            "Slide thuyết trình .pptx",
            "Đóng gói tệp zip nộp Classroom",
            "Cả nhóm thực hiện"
        ], COLOR_SECONDARY),
        ("GIAI ĐOẠN 2", "09/11 - 15/11", "Tối ưu hóa mô hình", [
            "Tinh chỉnh sâu Random Forest",
            "Tối ưu siêu tham số XGBoost",
            "Xử lý mất cân bằng SMOTE",
            "Tiến & Đạt phụ trách"
        ], COLOR_PRIMARY),
        ("GIAI ĐOẠN 3", "16/11 - 25/11", "Học kết hợp & Ngưỡng", [
            "Mô hình Stacking / Voting",
            "Tối ưu ngưỡng xác suất quyết định",
            "Cải thiện dứt điểm Recall Enrolled",
            "Phát & Hiếu phụ trách"
        ], COLOR_PRIMARY),
        ("GIAI ĐOẠN 4", "26/11 - 10/12", "Nghiệm thu & Demo", [
            "Mở tập Test 885 mẫu đánh giá",
            "Xây dựng Web Demo Streamlit",
            "Viết báo cáo tổng kết 5 chương",
            "Bảo vệ đồ án cuối kỳ"
        ], COLOR_ACCENT)
    ]

    for idx, (p_name, p_time, p_title, p_tasks, p_col) in enumerate(phases):
        x = start_x + idx * (card_w + card_gap)
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), card_w, Inches(5.2))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_BG_LIGHT
        c.line.color.rgb = p_col
        c.line.width = Pt(2)
        
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = p_name
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = p_col

        p = tf.add_paragraph()
        p.text = p_time
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_GRAY
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.space_before = Pt(8)

        for task in p_tasks:
            p = tf.add_paragraph()
            p.text = "• " + task
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_DARK
            p.space_before = Pt(6)

    # ==========================================================
    # SLIDE 12: Phân công nhiệm vụ & Đóng góp
    # ==========================================================
    s12 = prs.slides.add_slide(slide_layout)
    add_header(s12, "11. Bảng phân công nhiệm vụ & Đóng góp thành viên")

    t_team_shape = s12.shapes.add_table(5, 5, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.0))
    t_team = t_team_shape.table

    t_team.columns[0].width = Inches(2.2)
    t_team.columns[1].width = Inches(1.3)
    t_team.columns[2].width = Inches(1.5)
    t_team.columns[3].width = Inches(5.5)
    t_team.columns[4].width = Inches(1.2)

    t_headers = ["Họ và tên", "MSSV", "Vai trò", "Nhiệm vụ chuyên môn thực hiện", "Tiến độ"]
    for idx, text in enumerate(t_headers):
        cell = t_team.cell(0, idx)
        cell.text = text
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    members = [
        ["Dương Gia Phát", "3124411212", "Trưởng nhóm", "Feature engineering, thực nghiệm đối chứng Ablation A/B/C, script tự động run_all.py, ghép báo cáo Word và quản lý Git repo.", "100%"],
        ["Lê Văn Hiếu", "3124411091", "Thành viên", "Thu thập dữ liệu thô UCI 697, mã băm SHA256, pipeline tiền xử lý StandardScaler/OneHot, mô hình Dummy v1, LR v1 và DT v3.", "100%"],
        ["Văn Nguyễn Thành Đạt", "3124411067", "Thành viên", "Khám phá dữ liệu EDA, phân tích nợ học phí/điểm số, mô hình Decision Tree v1, Dummy v2, Logistic Regression v2 và XGBoost v1.", "100%"],
        ["Cái Trần Minh Tiến", "3124411309", "Thành viên", "Mô hình Random Forest v1, kiểm toán quá khớp train-val gap, Decision Tree v2 (Nested CV tuning) và đồng bộ nhật ký thực nghiệm.", "100%"]
    ]

    for r_idx, r_data in enumerate(members, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_team.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            if c_idx in [1, 2, 4]:
                p.alignment = PP_ALIGN.CENTER
            if c_idx == 4:
                p.font.bold = True
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(235, 247, 238)

    # Save presentation
    output_path = "BaoCao_TienDo_GiuaKy_Nhom10.pptx"
    prs.save(output_path)
    print(f"Presentation generated successfully: {output_path}")

if __name__ == "__main__":
    create_deck()
