import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set padding inside a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top='single', bottom='single', left='single', right='single', color='CCCCCC', sz='4'):
    """Set cell borders with specific style, color and thickness."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for b_name, b_val in borders.items():
        node = OxmlElement(f'w:{b_name}')
        node.set(qn('w:val'), b_val)
        if b_val != 'none':
            node.set(qn('w:sz'), sz)
            node.set(qn('w:space'), '0')
            node.set(qn('w:color'), color)
        tcBorders.append(node)
    tcPr.append(tcBorders)

def set_cell_shading(cell, color='F2F2F2'):
    """Set background color of a cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    tcPr.append(shd)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(16, 44, 87) # Deep academic navy
    r.bold = True
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 60, 114)
    r.bold = True
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(40, 40, 40)
    r.bold = True
    return p

def add_body(doc, text, bold_prefix='', space_after=3.5, line_spacing=1.25):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_bullet(doc, text, bold_prefix='', space_after=2.5):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.italic = True
    return p

def add_image_safe(doc, img_path, width_cm=15.5, caption=''):
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run()
        run.add_picture(img_path, width=Cm(width_cm))
        if caption:
            add_caption(doc, caption)
    else:
        print(f"Warning: Image not found at {img_path}")

def format_table(table, headers, data, col_widths=None, align_center_cols=None):
    """Format table with standard academic black/white/gray styling."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    if align_center_cols is None:
        align_center_cols = [False] * len(headers)

    # Set row properties: cantSplit for all rows, tblHeader for header row
    for row_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(OxmlElement('w:cantSplit'))
        if row_idx == 0 and trPr.find(qn('w:tblHeader')) is None:
            trPr.append(OxmlElement('w:tblHeader'))

    # Header Row
    hdr_cells = table.rows[0].cells
    for j, h in enumerate(headers):
        cell = hdr_cells[j]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, 'F2F2F2')
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        set_cell_borders(cell, top='single', bottom='single', left='single', right='single', color='444444', sz='6')
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.bold = True
        if col_widths and j < len(col_widths):
            cell.width = Cm(col_widths[j])

    # Data Rows
    for i, row in enumerate(data):
        row_cells = table.rows[i + 1].cells
        for j, val in enumerate(row):
            cell = row_cells[j]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            set_cell_borders(cell, top='single', bottom='single', left='single', right='single', color='CCCCCC', sz='4')
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            # Align center if specified, or if STT column
            if align_center_cols[j]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            r = p.add_run(str(val))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if col_widths and j < len(col_widths):
                cell.width = Cm(col_widths[j])

def add_page_number_to_section(section):
    """Add dynamic page number to footer centered."""
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run()
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    
    r._r.append(fldChar1)
    r._r.append(instrText)
    r._r.append(fldChar2)
    r._r.append(fldChar3)

def build_document():
    doc = docx.Document()

    # Page setup for Section 0 (A4, Margins: Top 2cm, Bottom 2cm, Left 2.5cm, Right 2cm)
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.0)

    # First page different header/footer so cover has no page number
    sec.different_first_page_header_footer = True
    add_page_number_to_section(sec)

    # =========================================================
    # TRANG BÌA (COVER PAGE)
    # =========================================================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(0)
    p_uni.paragraph_format.space_after = Pt(2)
    r_uni = p_uni.add_run("TRƯỜNG ĐẠI HỌC SÀI GÒN\nKHOA CÔNG NGHỆ THÔNG TIN")
    r_uni.font.name = 'Times New Roman'
    r_uni.font.size = Pt(13)
    r_uni.bold = True

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(0)
    p_line.paragraph_format.space_after = Pt(36)
    r_line = p_line.add_run("-------------------***-------------------")
    r_line.font.name = 'Times New Roman'
    r_line.font.size = Pt(10)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(12)
    p_sub.paragraph_format.space_after = Pt(6)
    r_sub = p_sub.add_run("BÁO CÁO TIẾN ĐỘ GIỮA KỲ\nMÔN HỌC: MÁY HỌC\nLỚP HỌC PHẦN: DCT124C1")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(14)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(16, 44, 87)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(24)
    p_title.paragraph_format.space_after = Pt(36)
    r_title = p_title.add_run("ĐỀ TÀI:\nDỰ ĐOÁN NGUY CƠ BỎ HỌC VÀ KẾT QUẢ HỌC TẬP\nCỦA SINH VIÊN")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(16)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(180, 0, 0)

    # Info table on cover page
    info_table = doc.add_table(rows=6, cols=3)
    info_headers = ["Họ và tên", "Mã số sinh viên", "Vai trò và Nhiệm vụ phụ trách"]
    info_data = [
        ["Dương Gia Phát", "3124411212", "Trưởng nhóm - Xây dựng đặc trưng, nghiên cứu đối chứng Ablation"],
        ["Lê Văn Hiếu", "3124411091", "Thành viên - Thu thập dữ liệu, Pipeline tiền xử lý, mô hình tham chiếu"],
        ["Văn Nguyễn Thành Đạt", "3124411067", "Thành viên - Khám phá dữ liệu EDA, Decision Tree v1, XGBoost v1"],
        ["Cái Trần Minh Tiến", "3124411309", "Thành viên - Huấn luyện Random Forest v1, kiểm toán quá khớp, Nested CV"],
        ["Giảng viên hướng dẫn:", "TS. Đỗ Như Tài", "Khoa Công nghệ Thông tin - Trường Đại học Sài Gòn"]
    ]
    format_table(info_table, info_headers, info_data, [4.2, 3.2, 9.1], [False, True, False])

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(64)
    p_loc.paragraph_format.space_after = Pt(0)
    r_loc = p_loc.add_run("Thành phố Hồ Chí Minh, Tháng 11 năm 2026")
    r_loc.font.name = 'Times New Roman'
    r_loc.font.size = Pt(11.5)

    doc.add_page_break()

    # =========================================================
    # MỤC LỤC BÁO CÁO
    # =========================================================
    add_heading_1(doc, "MỤC LỤC TỔNG QUAN")
    
    toc_data = [
        ("1. THÔNG TIN ĐỀ TÀI", "Trang 3"),
        ("    1.1. Thông tin chung", "Trang 3"),
        ("    1.2. Danh sách thành viên nhóm", "Trang 3"),
        ("    1.3. Bảng phân công nhiệm vụ và tiến độ thực hiện", "Trang 3"),
        ("2. GIỚI THIỆU BÀI TOÁN", "Trang 4"),
        ("    2.1. Bối cảnh và ý nghĩa thực tiễn", "Trang 4"),
        ("    2.2. Mục tiêu nghiên cứu", "Trang 4"),
        ("    2.3. Dữ liệu đầu vào, đầu ra và loại bài toán máy học", "Trang 4"),
        ("    2.4. Phạm vi và thời điểm dự đoán", "Trang 4"),
        ("3. MÔ TẢ DỮ LIỆU", "Trang 5"),
        ("    3.1. Nguồn dữ liệu và quy mô", "Trang 5"),
        ("    3.2. Phân chia tập dữ liệu huấn luyện và kiểm tra", "Trang 5"),
        ("    3.3. Phân phối biến mục tiêu", "Trang 5"),
        ("    3.4. Phân nhóm các thuộc tính đầu vào", "Trang 6"),
        ("4. KHÁM PHÁ VÀ TIỀN XỬ LÝ DỮ LIỆU", "Trang 6"),
        ("    4.1. Kiểm tra tính toàn vẹn và giá trị khuyết thiếu", "Trang 6"),
        ("    4.2. Phân tích giá trị ngoại lệ theo quy tắc tứ phân vị", "Trang 6"),
        ("    4.3. 5 phát hiện chính từ quá trình khám phá dữ liệu", "Trang 7"),
        ("    4.4. Quy trình tiền xử lý dữ liệu và đóng gói đường ống", "Trang 7"),
        ("    4.5. Kỹ thuật tạo đặc trưng mới", "Trang 8"),
        ("5. PHƯƠNG PHÁP VÀ MÔ HÌNH HỌC MÁY", "Trang 8"),
        ("    5.1. Thiết kế thực nghiệm và chiến lược kiểm định chéo", "Trang 8"),
        ("    5.2. Các thuật toán học máy được triển khai", "Trang 8"),
        ("6. KẾT QUẢ THỰC NGHIỆM BƯỚC ĐẦU", "Trang 9"),
        ("    6.1. Bảng so sánh tổng thể 11 lượt chạy thực nghiệm", "Trang 9"),
        ("    6.2. Hiệu năng chi tiết theo từng lớp nhãn Out-Of-Fold", "Trang 10"),
        ("    6.3. Phân tích ma trận nhầm lẫn Out-Of-Fold", "Trang 10"),
        ("    6.4. Phân tích hiện tượng học quá khớp của Random Forest v1", "Trang 11"),
        ("    6.5. Phân tích nguyên nhân khó khăn nhận diện lớp Enrolled", "Trang 12"),
        ("    6.6. Kết quả nghiên cứu đối chứng loại bỏ thành phần Ablation Study", "Trang 12"),
        ("7. ĐÁNH GIÁ TIẾN ĐỘ", "Trang 13"),
        ("    7.1. Công việc đã hoàn thành", "Trang 13"),
        ("    7.2. Khó khăn và hạn chế thực tế", "Trang 13"),
        ("    7.3. Công việc còn lại", "Trang 14"),
        ("    7.4. Kế hoạch hoàn thành đề tài cuối kỳ", "Trang 14"),
        ("8. PHÂN CÔNG VÀ ĐÓNG GÓP CÁ NHÂN", "Trang 15")
    ]

    toc_table = doc.add_table(rows=len(toc_data), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page) in enumerate(toc_data):
        trPr = toc_table.rows[idx]._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(OxmlElement('w:cantSplit'))
        row_cells = toc_table.rows[idx].cells
        set_cell_margins(row_cells[0], top=40, bottom=40, left=60, right=60)
        set_cell_margins(row_cells[1], top=40, bottom=40, left=60, right=60)
        set_cell_borders(row_cells[0], top='none', bottom='none', left='none', right='none')
        set_cell_borders(row_cells[1], top='none', bottom='none', left='none', right='none')
        
        p0 = row_cells[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        if title.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
            r0.bold = True
            
        p1 = row_cells[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        
        row_cells[0].width = Cm(13.5)
        row_cells[1].width = Cm(3.0)

    doc.add_page_break()

    # =========================================================
    # MỤC 1. THÔNG TIN ĐỀ TÀI
    # =========================================================
    add_heading_1(doc, "1. Thông tin đề tài")

    add_heading_2(doc, "1.1. Thông tin chung")
    add_bullet(doc, "Máy học", bold_prefix="Tên môn học: ")
    add_bullet(doc, "DCT124C1", bold_prefix="Lớp học phần: ")
    add_bullet(doc, "Nhóm 10", bold_prefix="Nhóm thực hiện: ")
    add_bullet(doc, "Dự đoán nguy cơ bỏ học và kết quả học tập của sinh viên", bold_prefix="Tên đề tài: ")
    add_bullet(doc, "Predict Students' Dropout and Academic Success", bold_prefix="Tên tiếng Anh: ")
    add_bullet(doc, "Kho lưu trữ UCI Machine Learning Repository, mã định danh 697, DOI 10.24432/C5MC89", bold_prefix="Nguồn dữ liệu: ")
    add_bullet(doc, "https://github.com/Kazuken123/DCT124C1-MH-Nhom.git", bold_prefix="Kho lưu trữ mã nguồn Git: ")
    add_bullet(doc, "Google Sheets đồng bộ Weights and Biases", bold_prefix="Nhật ký thực nghiệm: ")

    add_heading_2(doc, "1.2. Danh sách thành viên nhóm")
    add_body(doc, "Nhóm gồm 4 sinh viên lớp DCT124C1 tham gia thực hiện đề tài với đầy đủ thông tin định danh như sau:")

    t1 = doc.add_table(rows=5, cols=5)
    t1_headers = ["STT", "Họ và tên", "Mã số sinh viên", "Vai trò trong nhóm", "Email định danh Git"]
    t1_data = [
        ["1", "Dương Gia Phát", "3124411212", "Trưởng nhóm", "giuaguy1234@gmail.com"],
        ["2", "Lê Văn Hiếu", "3124411091", "Thành viên", "levanhieuvip2006@gmail.com"],
        ["3", "Văn Nguyễn Thành Đạt", "3124411067", "Thành viên", "thanhdat.longanvn@gmail.com"],
        ["4", "Cái Trần Minh Tiến", "3124411309", "Thành viên", "caitranminhtien@gmail.com"]
    ]
    format_table(t1, t1_headers, t1_data, [1.2, 3.8, 2.8, 3.2, 5.5], [True, False, True, False, False])

    add_heading_2(doc, "1.3. Bảng phân công nhiệm vụ và tiến độ thực hiện")
    add_body(doc, "Căn cứ theo thế mạnh chuyên môn và kế hoạch phân chia khối lượng công việc, bảng phân công nhiệm vụ kỹ thuật và mức độ hoàn thành giai đoạn giữa kỳ như sau:")

    t2 = doc.add_table(rows=5, cols=4)
    t2_headers = ["Thành viên", "Nhiệm vụ kỹ thuật chính được phân công", "Trạng thái", "Tiến độ"]
    t2_data = [
        ["Dương Gia Phát", "Phụ trách xây dựng đặc trưng mới và thực nghiệm đối chứng loại bỏ thành phần Ablation Study A, B, C trên Logistic Regression; thiết lập cấu hình phân chia dữ liệu cố định có mã băm xác thực; kiểm soát chống rò rỉ dữ liệu; quản lý kho lưu trữ Git và giải quyết xung đột mã nguồn.", "Hoàn thành", "100%"],
        ["Lê Văn Hiếu", "Phụ trách thu thập dữ liệu nguồn UCI 697; lập mã băm SHA256 kiểm tra tính toàn vẹn; xây dựng đường ống tiền xử lý chuẩn hóa biến số và mã hóa biến danh mục; triển khai mô hình tham chiếu cơ sở DummyClassifier v1 và Logistic Regression v1 trên 5 fold kiểm định chung; đồng bộ nhật ký thực nghiệm Weights and Biases.", "Hoàn thành", "100%"],
        ["Văn Nguyễn Thành Đạt", "Phụ trách khám phá dữ liệu trên tập huấn luyện; phân tích phân phối nhãn, tương quan điểm số và liên hệ giữa nợ học phí với thôi học; xây dựng mô hình Decision Tree v1 và khảo sát tham số độ sâu; triển khai mô hình Logistic Regression v2 với trọng số cân bằng lớp, DummyClassifier v2 ngẫu nhiên phân tầng và XGBoost v1.", "Hoàn thành", "100%"],
        ["Cái Trần Minh Tiến", "Phụ trách huấn luyện mô hình Random Forest v1 gồm 100 cây; kiểm toán khoảng cách học quá khớp giữa tập huấn luyện và kiểm định; triển khai mô hình Decision Tree v2 kết hợp mã hóa One-Hot và thẩm định chéo lồng nhau Nested Cross-Validation với 24 ứng viên tham số; tổng hợp nhật ký thực nghiệm và biểu đồ kết quả.", "Hoàn thành", "100%"]
    ]
    format_table(t2, t2_headers, t2_data, [3.2, 9.8, 2.0, 1.5], [False, False, True, True])

    # =========================================================
    # MỤC 2. GIỚI THIỆU BÀI TOÁN
    # =========================================================
    add_heading_1(doc, "2. Giới thiệu bài toán")

    add_heading_2(doc, "2.1. Bối cảnh và ý nghĩa thực tiễn")
    add_body(doc, "Hiện tượng sinh viên thôi học, bỏ học giữa chừng hoặc kéo dài thời gian tốt nghiệp gây lãng phí lớn về thời gian, học phí của bản thân người học và làm hao tổn nguồn lực đào tạo của các cơ sở giáo dục đại học. Trong thực tế quản lý đào tạo, nhà trường thường chỉ phát hiện sinh viên bỏ học khi các em đã ngừng đóng học phí hoặc tự ý bỏ thi nhiều học kỳ liên tiếp. Lúc này, mọi nỗ lực vận động hay hỗ trợ thường không còn mang lại hiệu quả cao.")
    add_body(doc, "Nếu có thể xây dựng một công cụ máy học có khả năng phát hiện sớm các sinh viên mang nguy cơ học tập sa sút hoặc gặp khó khăn về tài chính, bộ phận cố vấn học tập và ban giám hiệu nhà trường có thể chủ động tiếp cận, cung cấp học bổng hỗ trợ khó khăn, tư vấn lộ trình học tập phù hợp hoặc giãn tiến độ trả nợ học phí. Điều này giúp nâng cao tỷ lệ duy trì sĩ số và đảm bảo quyền lợi học tập cho người học.")

    add_heading_2(doc, "2.2. Mục tiêu nghiên cứu")
    add_body(doc, "Mục tiêu của đề tài là xây dựng và đánh giá thực nghiệm các mô hình học máy phân loại trạng thái học tập của sinh viên dựa trên bộ dữ liệu chuẩn mực. Thông qua quá trình thực nghiệm giữa kỳ, nhóm tập trung trả lời 3 câu hỏi kỹ thuật cụ thể:")
    add_bullet(doc, "Mô hình học máy nào cho hiệu năng phân loại tổng thể cân bằng nhất giữa các lớp sinh viên?")
    add_bullet(doc, "Dữ liệu kết quả học tập ở học kỳ 2 đóng vai trò quan trọng ở mức độ nào đối với độ chính xác của hệ thống cảnh báo sớm?")
    add_bullet(doc, "Việc tạo thêm các đặc trưng tỷ lệ qua môn và xu hướng biến động điểm số có giúp cải thiện khả năng phân định của các thuật toán hay không?")

    add_heading_2(doc, "2.3. Dữ liệu đầu vào, đầu ra và loại bài toán máy học")
    add_bullet(doc, "Gồm 36 thuộc tính thu thập từ hồ sơ tuyển sinh ban đầu, điều kiện kinh tế xã hội gia đình và kết quả học tập trong 2 học kỳ của năm thứ nhất.", bold_prefix="Dữ liệu đầu vào: ")
    add_bullet(doc, "Biến phân loại gồm 3 trạng thái của sinh viên tại thời điểm khảo sát:", bold_prefix="Dữ liệu đầu ra: ")
    add_body(doc, "1. Dropout: Sinh viên đã thôi học hoặc bỏ học.", space_after=2)
    add_body(doc, "2. Enrolled: Sinh viên còn đang theo học tại trường, chưa tốt nghiệp và chưa bỏ học.", space_after=2)
    add_body(doc, "3. Graduate: Sinh viên đã hoàn thành chương trình đào tạo và tốt nghiệp.", space_after=3.5)
    add_bullet(doc, "Học có giám sát, cụ thể là bài toán phân loại đa lớp với 3 nhãn phân biệt. Nhóm giữ nguyên bài toán phân loại 3 lớp theo dữ liệu gốc, không đơn giản hóa thành bài toán nhị phân giữa bỏ học và tốt nghiệp.", bold_prefix="Loại bài toán máy học: ")

    add_heading_2(doc, "2.4. Phạm vi và thời điểm dự đoán")
    add_body(doc, "Do bộ dữ liệu có chứa thông tin kết quả học tập của cả học kỳ 1 và học kỳ 2, việc áp dụng mô hình đầy đủ 36 đặc trưng chỉ có thể thực hiện sau khi sinh viên đã hoàn thành trọn vẹn năm học thứ nhất. Để đánh giá tính khả thi của việc cảnh báo sớm hơn ở thời điểm kết thúc học kỳ 1, nhóm đã thiết kế riêng thực nghiệm loại bỏ thành phần dữ liệu học kỳ 2.")

    # =========================================================
    # MỤC 3. MÔ TẢ DỮ LIỆU
    # =========================================================
    add_heading_1(doc, "3. Mô tả dữ liệu")

    add_heading_2(doc, "3.1. Nguồn dữ liệu và quy mô")
    add_body(doc, "Đề tài sử dụng bộ dữ liệu Predict Students' Dropout and Academic Success được công bố bởi nhóm tác giả Valentim Realinho, Mónica V. Martins, Jorge Machado và Luís Baptista vào năm 2021 trên kho lưu trữ UCI Machine Learning Repository với mã định danh 697 và định danh số DOI 10.24432/C5MC89.")
    add_body(doc, "Bộ dữ liệu gồm tổng cộng 4.424 bản ghi sinh viên và 37 cột dữ liệu, trong đó có 36 thuộc tính đầu vào và 1 cột mục tiêu Target. Dữ liệu gốc được lưu trữ tại đường dẫn final/data/raw/data.csv với dấu phân cách là dấu chấm phẩy. Để đảm bảo tính toàn vẹn và ngăn chặn việc sửa đổi dữ liệu ngoài ý muốn, tệp dữ liệu đã được khóa mã băm SHA256 là 3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae được ghi nhận trong tệp final/data/source_manifest.json.")

    add_heading_2(doc, "3.2. Phân chia tập dữ liệu huấn luyện và kiểm tra")
    add_body(doc, "Nhóm thống nhất áp dụng quy tắc phân chia dữ liệu cố định với tỷ lệ 80% cho tập huấn luyện và 20% cho tập kiểm tra:")
    add_bullet(doc, "Gồm 3.539 mẫu sinh viên.", bold_prefix="Tập huấn luyện Train: ")
    add_bullet(doc, "Gồm 885 mẫu sinh viên.", bold_prefix="Tập kiểm tra Test: ")
    add_body(doc, "Quá trình phân chia sử dụng phương pháp phân tầng theo tỷ lệ lớp với giá trị hạt giống ngẫu nhiên seed bằng 42. Danh sách chỉ số dòng của tập huấn luyện và tập kiểm tra được lưu trữ cố định thành các tệp CSV tại thư mục final/configs/splits/student_dropout_seed42_v1/. Toàn bộ các thực nghiệm báo cáo trong giai đoạn giữa kỳ chỉ được thực hiện trên 3.539 mẫu của tập huấn luyện thông qua kỹ thuật thẩm định chéo phân tầng 5 lượt. Tập kiểm tra 885 mẫu được bảo lưu nguyên vẹn và không được sử dụng để lựa chọn thuật toán hay tinh chỉnh siêu tham số nhằm bảo vệ tính khách quan cho kỳ đánh giá cuối khóa.")

    add_heading_2(doc, "3.3. Phân phối biến mục tiêu")
    add_body(doc, "Dưới đây là bảng thống kê số lượng và tỷ lệ phân phối của biến mục tiêu trên toàn bộ tập dữ liệu, tập huấn luyện và tập kiểm tra:")

    t3 = doc.add_table(rows=4, cols=5)
    t3_headers = ["Trạng thái sinh viên", "Toàn bộ dữ liệu 4.424 mẫu", "Tập huấn luyện 3.539 mẫu", "Tập kiểm tra 885 mẫu", "Tỷ lệ phần trăm"]
    t3_data = [
        ["Graduate", "2.209", "1.767", "442", "49,93%"],
        ["Dropout", "1.421", "1.137", "284", "32,12%"],
        ["Enrolled", "794", "635", "159", "17,95%"]
    ]
    format_table(t3, t3_headers, t3_data, [4.5, 3.2, 3.2, 2.8, 2.8], [False, True, True, True, True])

    add_image_safe(doc, 'figures_report/fig1_target_distribution.png', width_cm=14.5, 
                   caption="Hình 1. Phân bố số lượng và tỷ lệ các lớp mục tiêu Target trên tập huấn luyện và tập kiểm tra")

    add_body(doc, "Số liệu cho thấy tập dữ liệu bị mất cân bằng lớp. Lớp sinh viên tốt nghiệp chiếm tỷ trọng lớn nhất với gần một nửa dữ liệu là 49,93%, trong khi lớp sinh viên còn đang theo học chỉ chiếm 17,95%. Số sinh viên tốt nghiệp cao gấp 2,78 lần số sinh viên đang học. Sự chênh lệch này đòi hỏi khi đánh giá chất lượng mô hình bắt buộc phải sử dụng thang đo Macro-F1 kết hợp với theo dõi Recall của từng lớp, không thể chỉ dựa vào chỉ số Accuracy đơn thuần.")

    add_heading_2(doc, "3.4. Phân nhóm các thuộc tính đầu vào")
    add_body(doc, "36 thuộc tính đầu vào của bộ dữ liệu được phân chia thành 4 nhóm nội dung chính:")
    add_bullet(doc, "Gồm 5 thuộc tính: Giới tính, độ tuổi khi nhập học, quốc tịch, tình trạng hôn nhân, tình trạng nhu cầu giáo dục đặc biệt.", bold_prefix="1. Nhóm nhân khẩu học: ")
    add_bullet(doc, "Gồm 7 thuộc tính: Trình độ học vấn của mẹ, trình độ học vấn của cha, nghề nghiệp của mẹ, nghề nghiệp của cha, tình trạng nợ học phí, tình trạng cập nhật đóng học phí đúng hạn, tình trạng được nhận học bổng.", bold_prefix="2. Nhóm hoàn cảnh kinh tế xã hội: ")
    add_bullet(doc, "Gồm 8 thuộc tính: Hình thức xét tuyển đầu vào, thứ tự nguyện vọng đăng ký ngành học, mã ngành học trúng tuyển, thời gian học ban ngày hay buổi tối, trình độ học vấn trước khi nhập học, điểm kết thúc bậc học trước, điểm xét tuyển đầu vào, các chỉ số kinh tế vĩ mô tại thời điểm nhập học gồm tỷ lệ thất nghiệp, tỷ lệ lạm phát và tỷ lệ tăng trưởng GDP.", bold_prefix="3. Nhóm tuyển sinh và bối cảnh đào tạo: ")
    add_bullet(doc, "Gồm 16 thuộc tính chia đều cho 2 học kỳ. Học kỳ 1 gồm 8 thuộc tính: Số tín chỉ được công nhận, số tín chỉ đăng ký, số lượt kiểm tra đánh giá, số tín chỉ đạt yêu cầu, điểm trung bình tín chỉ, số tín chỉ không qua đánh giá. Học kỳ 2 gồm 8 thuộc tính tương ứng với cấu trúc của học kỳ 1.", bold_prefix="4. Nhóm kết quả học tập năm thứ nhất: ")
    add_body(doc, "Về bản chất kiểu dữ liệu trong lập trình, 36 thuộc tính này gồm 18 biến số lượng liên tục hoặc rời rạc, 10 biến phân loại danh mục nhiều giá trị, và 8 biến nhị phân tự nhiên chỉ nhận giá trị 0 hoặc 1.")

    # =========================================================
    # MỤC 4. KHÁM PHÁ VÀ TIỀN XỬ LÝ DỮ LIỆU
    # =========================================================
    add_heading_1(doc, "4. Khám phá và tiền xử lý dữ liệu")

    add_heading_2(doc, "4.1. Kiểm tra tính toàn vẹn và giá trị khuyết thiếu")
    add_body(doc, "Kiểm tra lập trình trên toàn bộ 4.424 dòng dữ liệu và 37 cột xác nhận tập dữ liệu hoàn toàn không có giá trị khuyết thiếu, số lượng giá trị thiếu bằng 0. Do đó, quy trình tiền xử lý không cần áp dụng các kỹ thuật điền khuyết giá trị nhân tạo, bảo toàn nguyên vẹn tính chân thực của dữ liệu nguồn.")

    add_heading_2(doc, "4.2. Phân tích giá trị ngoại lệ theo quy tắc tứ phân vị")
    add_body(doc, "Nhóm áp dụng quy tắc 1,5 lần khoảng tứ phân vị IQR để rà soát các giá trị nằm ngoài biên bình thường trên tập huấn luyện 3.539 mẫu:")
    add_bullet(doc, "Có 358 sinh viên nằm ngoài biên trên, chiếm 10,12%, với trung vị là 20 tuổi, khoảng tứ phân vị từ 19 đến 25 tuổi và giá trị cao nhất lên tới 70 tuổi.", bold_prefix="Tuổi nhập học: ")
    add_bullet(doc, "Có 68 sinh viên nằm ngoài biên, chiếm 1,92%, với trung vị là 126 điểm và trung bình là 126,88 điểm.", bold_prefix="Điểm xét tuyển đầu vào: ")
    add_bullet(doc, "Có lần lượt 342 sinh viên chiếm 9,66% và 300 sinh viên chiếm 8,48% nằm ngoài biên bình thường do đăng ký vượt tải hoặc đăng ký quá ít môn.", bold_prefix="Số tín chỉ đăng ký học kỳ 1 và học kỳ 2: ")
    add_body(doc, "Kiểm tra hồ sơ thực tế xác nhận đây là hiện tượng thực tế trong đào tạo đại học gồm sinh viên học văn bằng hai, sinh viên lớn tuổi hoặc sinh viên học lại, không phải do sai sót nhập liệu. Vì vậy, nhóm quyết định giữ nguyên toàn bộ các mẫu ngoại lệ này, không xóa bỏ để mô hình học được tính đa dạng của đối tượng sinh viên.")

    add_heading_2(doc, "4.3. 5 phát hiện chính từ quá trình khám phá dữ liệu trên tập huấn luyện")
    add_body(doc, "Quá trình phân tích tương quan và trực quan hóa dữ liệu trên 3.539 mẫu tập huấn luyện đem lại 5 phát hiện then chốt sau:")
    add_bullet(doc, "Lớp sinh viên tốt nghiệp chiếm 49,93%, lớp bỏ học chiếm 32,13% và lớp đang học chiếm 17,94%. Mô hình cần được xử lý để không bị thiên vị về lớp chiếm đa số.", bold_prefix="Phát hiện 1 về sự lệch lớp: ")
    add_bullet(doc, "Có 705 trên 3.539 sinh viên có điểm trung bình học kỳ 2 bằng 0, chiếm 19,92%. Trong nhóm này, tỷ lệ sinh viên bỏ học lên tới 83,40%, so với tỷ lệ chỉ 19,37% ở nhóm sinh viên có điểm lớn hơn 0. Đây là dấu hiệu cảnh báo sớm quan trọng nhất về việc sinh viên đã ngừng việc học.", bold_prefix="Phát hiện 2 về điểm học kỳ 2 bằng 0: ")
    add_bullet(doc, "Trong 389 sinh viên đang nợ học phí, tỷ lệ bỏ học là 64,01%. Ngược lại, trong nhóm 3.150 sinh viên không nợ học phí, tỷ lệ bỏ học chỉ là 28,19%. Nợ học phí làm tăng nguy cơ thôi học gấp hơn 2,2 lần.", bold_prefix="Phát hiện 3 về tình trạng nợ học phí: ")
    add_bullet(doc, "Trong nhóm sinh viên được cấp học bổng, tỷ lệ bỏ học chỉ là 12,86%. Trong khi đó, ở nhóm sinh viên không nhận học bổng, tỷ lệ bỏ học là 38,64%. Học bổng gắn liền với sự kiên trì theo học của sinh viên.", bold_prefix="Phát hiện 4 về tình trạng nhận học bổng: ")
    add_bullet(doc, "Các biến cùng loại giữa học kỳ 1 và học kỳ 2 có tương quan tuyến tính rất cao. Hệ số tương quan Pearson đối với số tín chỉ đăng ký là r bằng 0,94; đối với số tín chỉ đạt yêu cầu là r bằng 0,91; và đối với điểm trung bình hai kỳ là r bằng 0,84. Điều này cho thấy thông tin giữa hai kỳ có sự kế thừa và phản ánh sự ổn định về năng lực học tập của sinh viên.", bold_prefix="Phát hiện 5 về sự trùng lặp thông tin giữa hai học kỳ: ")

    add_image_safe(doc, 'figures_report/fig2_eda_correlation.png', width_cm=15.0, 
                   caption="Hình 2. Tỷ lệ sinh viên bỏ học theo tình trạng điểm số học kỳ 2, nợ học phí và học bổng")

    add_heading_2(doc, "4.4. Quy trình tiền xử lý dữ liệu và đóng gói đường ống")
    add_body(doc, "Để xử lý các biến có thang đo khác nhau và kiểu dữ liệu khác nhau, nhóm xây dựng đường ống tiền xử lý thông qua công cụ ColumnTransformer của Scikit-learn:")
    add_bullet(doc, "Áp dụng chuẩn hóa StandardScaler để đưa giá trị về phân phối có giá trị trung bình bằng 0 và độ lệch chuẩn bằng 1. Điều này giúp các thuật toán nhạy cảm với độ lớn đặc trưng như Logistic Regression hội tụ ổn định và không bị áp đảo bởi các biến có khoảng giá trị lớn.", bold_prefix="Đối với 18 biến số lượng liên tục: ")
    add_bullet(doc, "Áp dụng mã hóa OneHotEncoder với tùy chọn handle_unknown='ignore' để chuyển đổi các mã ngành học, nghề nghiệp cha mẹ thành các cột nhị phân phân tách, đồng thời tự động bỏ qua nếu gặp giá trị danh mục mới trong tập kiểm định.", bold_prefix="Đối với 10 biến phân loại danh mục: ")
    add_bullet(doc, "Áp dụng tùy chọn passthrough để giữ nguyên định dạng 0 và 1 có sẵn.", bold_prefix="Đối với 8 biến nhị phân tự nhiên: ")
    add_body(doc, "Đường ống tiền xử lý được tích hợp trực tiếp vào đối tượng Pipeline cùng với bộ phân loại. Việc ước lượng tham số trung bình và độ lệch chuẩn chỉ được thực hiện trên tập huấn luyện của từng fold tương ứng, sau đó mới dùng các tham số này để biến đổi dữ liệu trên fold kiểm định, đảm bảo ngăn chặn triệt để hiện tượng rò rỉ thông tin dữ liệu.")

    add_heading_2(doc, "4.5. Kỹ thuật tạo đặc trưng mới")
    add_body(doc, "Dựa trên kiến thức chuyên môn về đào tạo đại học theo học chế tín chỉ, nhóm xây dựng thêm 3 đặc trưng tỷ lệ và xu hướng điểm số từ các thuộc tính gốc:")
    add_bullet(doc, "Bằng số môn đạt học kỳ 1 chia cho số môn đăng ký học kỳ 1 nếu số môn đăng ký lớn hơn 0; nếu số môn đăng ký bằng 0 thì gán giá trị bằng 0.0.", bold_prefix="1. Tỷ lệ môn đạt học kỳ 1: ")
    add_bullet(doc, "Bằng số môn đạt học kỳ 2 chia cho số môn đăng ký học kỳ 2 nếu số môn đăng ký lớn hơn 0; nếu số môn đăng ký bằng 0 thì gán giá trị bằng 0.0.", bold_prefix="2. Tỷ lệ môn đạt học kỳ 2: ")
    add_bullet(doc, "Bằng điểm trung bình học kỳ 2 trừ đi điểm trung bình học kỳ 1.", bold_prefix="3. Chênh lệch điểm trung bình giữa hai kỳ: ")
    add_body(doc, "Quá trình khảo sát dữ liệu cho thấy có 180 sinh viên đăng ký 0 môn ở học kỳ 1 và 180 sinh viên đăng ký 0 môn ở học kỳ 2. Nếu áp dụng phép chia số học thông thường sẽ gây lỗi chia cho 0 hoặc tạo ra giá trị vô cùng. Thuật toán kiểm tra điều kiện mẫu số lớn hơn 0 trước khi thực hiện phép tính; nếu mẫu số bằng 0 thì gán tỷ lệ đạt là 0.0, giúp bảo đảm an toàn dữ liệu tuyệt đối khi huấn luyện mô hình.")

    # =========================================================
    # MỤC 5. PHƯƠNG PHÁP VÀ MÔ HÌNH HỌC MÁY
    # =========================================================
    add_heading_1(doc, "5. Phương pháp và mô hình học máy")

    add_heading_2(doc, "5.1. Thiết kế thực nghiệm và chiến lược kiểm định chéo")
    add_body(doc, "Quy trình thực nghiệm được thiết kế theo đúng chuẩn mực khoa học máy học:")
    add_bullet(doc, "3.539 mẫu thuộc tập huấn luyện.", bold_prefix="Tập dữ liệu đánh giá: ")
    add_bullet(doc, "Thẩm định chéo phân tầng 5 lượt 5-Fold Stratified Cross-Validation. Phương pháp này chia tập huấn luyện thành 5 phần có tỷ lệ phân bố giữa 3 lớp nhãn hoàn toàn đồng đều. Ở mỗi lượt, 4 phần được dùng để huấn luyện và 1 phần được dùng để kiểm tra đánh giá độc lập.", bold_prefix="Chiến lược kiểm định: ")
    add_bullet(doc, "Điểm trung bình Macro-F1 trên 5 lượt kiểm định. Độ lệch chuẩn được tính toán với bậc tự do ddof bằng 0.", bold_prefix="Độ đo đánh giá chính: ")
    add_bullet(doc, "Độ chính xác tổng thể Accuracy, Precision, Recall và F1-score riêng của từng lớp nhãn, ma trận nhầm lẫn dự đoán ngoài tập Out-Of-Fold Confusion Matrix, và khoảng cách chênh lệch hiệu năng giữa tập huấn luyện và tập kiểm định Train-Validation Gap.", bold_prefix="Các độ đo bổ trợ: ")

    add_heading_2(doc, "5.2. Các thuật toán học máy được triển khai")
    add_body(doc, "Nhóm đã triển khai thực nghiệm trên 2 mô hình mốc tham chiếu và 4 thuật toán phân loại có giám sát:")
    add_bullet(doc, "Áp dụng chiến lược most_frequent. Mô hình luôn gán nhãn dự đoán cho mọi sinh viên là lớp chiếm đa số Graduate. Mô hình này thiết lập mức điểm sàn tối thiểu mà bất kỳ thuật toán máy học thực sự nào cũng phải vượt qua.", bold_prefix="1. Mô hình tham chiếu cơ sở 1 DummyClassifier v1: ")
    add_bullet(doc, "Áp dụng chiến lược stratified với seed bằng 42. Mô hình phát sinh nhãn dự đoán ngẫu nhiên theo đúng tỷ lệ phân phối thực tế của 3 lớp trong tập huấn luyện.", bold_prefix="2. Mô hình tham chiếu cơ sở 2 DummyClassifier v2: ")
    add_bullet(doc, "Mô hình hồi quy tuyến tính chuẩn hóa với hàm phạt L2, hệ số điều chuẩn C bằng 1.0, thuật toán tối ưu lbfgs, số vòng lặp tối đa 2000, ngưỡng dừng 0.0001, seed bằng 42 và không áp dụng trọng số lớp. Đây là mốc so sánh tuyến tính tiêu chuẩn của đề tài.", bold_prefix="3. Logistic Regression phiên bản 1: ")
    add_bullet(doc, "Giữ nguyên cấu hình tham số của phiên bản 1 nhưng áp dụng thêm tùy chọn class_weight='balanced'. Tùy chọn này tự động gán trọng số phạt lớn hơn cho các lớp có ít mẫu như lớp Enrolled và Dropout, nhằm đánh giá khả năng cải thiện tỷ lệ nhận diện cho các lớp thiểu số.", bold_prefix="4. Logistic Regression phiên bản 2: ")
    add_bullet(doc, "Cây quyết định cố định ban đầu sử dụng tiêu chí phân tách Gini, giới hạn độ sâu tối đa max_depth bằng 5, số lượng mẫu tối thiểu tại mỗi nút lá min_samples_leaf bằng 10, seed bằng 42 trên 36 đặc trưng gốc.", bold_prefix="5. Decision Tree phiên bản 1: ")
    add_bullet(doc, "Triển khai cải tiến kết hợp mã hóa One-Hot cho 17 biến danh mục và áp dụng phương pháp thẩm định chéo lồng nhau Nested Cross-Validation gồm 5 fold ngoài và 3 fold trong. Quá trình khảo sát ngẫu nhiên 24 tổ hợp tham số gồm max_depth trong khoảng từ 3 đến 10, min_samples_split trong khoảng từ 2 đến 20, min_samples_leaf trong khoảng từ 2 đến 20, và tham số cắt tỉa ccp_alpha trong khoảng từ 0.0 đến 0.005.", bold_prefix="6. Decision Tree phiên bản 2: ")
    add_bullet(doc, "Mô hình rừng ngẫu nhiên kết hợp 100 cây quyết định, tham số mặc định không giới hạn độ sâu cây với max_depth bằng None, min_samples_leaf bằng 1, seed bằng 42. Mô hình được dùng để kiểm tra năng lực của phương pháp học kết hợp và đo đạc mức độ học quá khớp.", bold_prefix="7. Random Forest phiên bản 1: ")
    add_bullet(doc, "Mô hình tăng cường độ dốc gồm 100 cây quyết định, giới hạn độ sâu cây max_depth bằng 3, tốc độ học learning_rate bằng 0,1, phương pháp phân chia nút tree_method='hist', seed bằng 42.", bold_prefix="8. XGBoost phiên bản 1: ")

    # =========================================================
    # MỤC 6. KẾT QUẢ THỰC NGHIỆM BƯỚC ĐẦU
    # =========================================================
    add_heading_1(doc, "6. Kết quả thực nghiệm bước đầu")

    add_heading_2(doc, "6.1. Bảng so sánh tổng thể 11 lượt chạy thực nghiệm trên tập huấn luyện")
    add_body(doc, "Dưới đây là bảng tổng hợp đầy đủ số liệu từ 11 lượt chạy thực nghiệm chính thức được trích xuất trực tiếp từ các tệp nhật ký final/experiments/results.csv, final/experiments/ablation.csv và các tệp cấu hình metrics.json:")

    t4 = doc.add_table(rows=12, cols=10)
    t4_headers = ["STT", "Tên mô hình và phiên bản", "Mã lần chạy", "Số biến", "Macro-F1", "Độ lệch chuẩn", "Accuracy", "Recall Drop", "Recall Enr", "Train-Val Gap"]
    t4_data = [
        ["1", "DummyClassifier v1", "m01_baseline_v1_6b66b3d6", "36", "0,2220", "0,0002", "49,93%", "0,00%", "0,00%", "0,0000"],
        ["2", "DummyClassifier v2", "m01_baseline_v2_ca767d56", "36", "0,3383", "0,0092", "39,19%", "34,65%", "16,69%", "-0,0078"],
        ["3", "Decision Tree v1", "m02_decision_tree_v1_6d8b7c85", "36", "0,6472", "0,0230", "73,69%", "70,10%", "29,76%", "0,0405"],
        ["4", "Decision Tree v2 One-Hot", "DT_V2_onehot_fixed", "36", "0,6586", "0,0186", "74,09%", "69,83%", "33,07%", "0,0346"],
        ["5", "Decision Tree v2 Tuned", "DT_V2_nested_tuned", "36", "0,6783", "0,0097", "73,58%", "69,65%", "47,09%", "0,0305"],
        ["6", "Random Forest v1", "m03_random_forest_v1_kaggle", "36", "0,6852", "0,0239", "76,91%", "76,52%", "Chưa có", "0,3148"],
        ["7", "Logistic Regression v1", "m05_logistic_regression_v1", "36", "0,6997", "0,0099", "77,54%", "77,48%", "37,80%", "0,0559"],
        ["8", "Logistic Regression v2 Balanced", "m05_logistic_regression_v2", "36", "0,7067", "0,0143", "74,85%", "73,61%", "59,37%", "0,0625"],
        ["9", "XGBoost v1", "m04_xgboost_v1_bc3ae52b", "36", "0,6994", "0,0046", "77,71%", "76,07%", "37,01%", "0,0714"],
        ["10", "LR Ablation B Bỏ HK2", "m05_lr_ablation_b", "30", "0,6578", "0,0149", "74,62%", "75,28%", "29,92%", "0,0612"],
        ["11", "LR Ablation C Thêm FE", "m05_lr_ablation_c", "39", "0,7031", "0,0110", "77,71%", "77,74%", "38,43%", "0,0527"]
    ]
    format_table(t4, t4_headers, t4_data, [0.8, 3.8, 2.5, 1.0, 1.4, 1.3, 1.4, 1.4, 1.4, 1.5], 
                 [True, False, False, True, True, True, True, True, True, True])

    add_image_safe(doc, 'figures_report/fig3_model_macro_f1_comparison.png', width_cm=15.5, 
                   caption="Hình 3. So sánh điểm trung bình Macro-F1 kiểm định chéo 5 fold giữa các mô hình học máy")

    add_heading_2(doc, "6.2. Hiệu năng chi tiết theo từng lớp nhãn Out-Of-Fold")
    add_body(doc, "Dưới đây là bảng thống kê chi tiết các độ đo Precision, Recall và F1-score trên toàn bộ 3.539 dự đoán ngoài tập của các mô hình đại diện:")

    t5 = doc.add_table(rows=9, cols=6)
    t5_headers = ["Mô hình", "Chỉ số đánh giá", "Lớp Dropout 1.137 mẫu", "Lớp Enrolled 635 mẫu", "Lớp Graduate 1.767 mẫu", "Macro-F1 OOF"]
    t5_data = [
        ["DummyClassifier v1", "Precision / Recall / F1", "0,0000 / 0,0000 / 0,0000", "0,0000 / 0,0000 / 0,0000", "0,4993 / 1,0000 / 0,6660", "0,2220"],
        ["Decision Tree v1", "Precision / Recall / F1", "0,8346 / 0,7010 / 0,7620", "0,4576 / 0,2976 / 0,3607", "0,7471 / 0,9179 / 0,8238", "0,6488"],
        ["Decision Tree v2 Tuned", "Precision / Recall / F1", "0,8462 / 0,6966 / 0,7641", "0,4333 / 0,4709 / 0,4513", "0,7909 / 0,8563 / 0,8223", "0,6792"],
        ["Random Forest v1", "Precision / Recall / F1", "0,8000 / 0,7700 / 0,7800", "0,5600 / 0,3400 / 0,4200", "0,7900 / 0,9300 / 0,8500", "0,6859"],
        ["Logistic Regression v1", "Precision / Recall / F1", "0,7980 / 0,7748 / 0,7863", "0,5742 / 0,3780 / 0,4558", "0,8047 / 0,9185 / 0,8578", "0,7000"],
        ["Logistic Regression v2", "Precision / Recall / F1", "0,8150 / 0,7361 / 0,7736", "0,4542 / 0,5937 / 0,5147", "0,8532 / 0,8121 / 0,8321", "0,7068"],
        ["XGBoost v1", "Precision / Recall / F1", "0,8270 / 0,7608 / 0,7925", "0,5649 / 0,3701 / 0,4472", "0,7944 / 0,9338 / 0,8585", "0,6994"],
        ["LR Ablation C Thêm FE", "Precision / Recall / F1", "0,7978 / 0,7775 / 0,7875", "0,5865 / 0,3843 / 0,4643", "0,8050 / 0,9179 / 0,8577", "0,7032"]
    ]
    format_table(t5, t5_headers, t5_data, [3.0, 2.5, 3.0, 3.0, 3.2, 1.8], [False, True, True, True, True, True])

    add_heading_2(doc, "6.3. Phân tích ma trận nhầm lẫn Out-Of-Fold")
    add_body(doc, "Dựa trên ma trận nhầm lẫn dự đoán ngoài tập trên 3.539 mẫu huấn luyện:")
    add_bullet(doc, "Đối với 1.137 sinh viên Dropout thực tế: Dự đoán đúng 881 trường hợp, đoán nhầm thành Enrolled 102 trường hợp, đoán nhầm thành Graduate 154 trường hợp. Tỷ lệ nhận diện đúng đạt 77,48%, bỏ sót 256 ca bỏ học. Đối với 635 sinh viên Enrolled thực tế: Dự đoán đúng 240 trường hợp, đoán nhầm thành Dropout 155 trường hợp, đoán nhầm thành Graduate 240 trường hợp. Tỷ lệ nhận diện đúng chỉ đạt 37,80%, bỏ sót hơn 62% sinh viên đang học. Đối với 1.767 sinh viên Graduate thực tế: Dự đoán đúng 1.623 trường hợp, đoán nhầm thành Dropout 68 trường hợp, đoán nhầm thành Enrolled 76 trường hợp. Tỷ lệ nhận diện đúng đạt 91,85%.", bold_prefix="Mô hình Logistic Regression phiên bản 1 chuẩn tắc mốc cơ sở: ")
    add_bullet(doc, "Đối với sinh viên Enrolled thực tế: Số ca dự đoán đúng tăng vọt từ 240 lên 377 trường hợp, tăng thêm 137 sinh viên, đưa Recall lớp này từ 37,80% lên 59,37%. Tuy nhiên, sự cải thiện này đi kèm việc tăng nhầm lẫn ở hai lớp còn lại: Số sinh viên Dropout bị đoán nhầm sang Enrolled tăng từ 102 lên 204 trường hợp; số sinh viên Graduate bị đoán nhầm sang Enrolled tăng từ 76 lên 249 trường hợp.", bold_prefix="Mô hình Logistic Regression phiên bản 2 áp dụng class_weight='balanced': ")
    add_bullet(doc, "Đối với Dropout: Dự đoán đúng 865 trường hợp, nhầm sang Enrolled 114 trường hợp, nhầm sang Graduate 158 trường hợp. Đối với Enrolled: Dự đoán đúng 235 trường hợp, nhầm sang Dropout 131 trường hợp, nhầm sang Graduate 269 trường hợp. Đối với Graduate: Dự đoán đúng 1.650 trường hợp, nhầm sang Dropout 50 trường hợp, nhầm sang Enrolled 67 trường hợp. Mô hình đạt độ chính xác lớp Graduate cao nhất nhóm với 93,38%.", bold_prefix="Mô hình XGBoost phiên bản 1: ")

    add_image_safe(doc, 'figures_report/fig4_confusion_matrix_lr_v1_v2.png', width_cm=16.0, 
                   caption="Hình 4. So sánh ma trận nhầm lẫn ngoài tập OOF giữa Logistic Regression v1 và v2")

    add_heading_2(doc, "6.4. Phân tích hiện tượng học quá khớp của Random Forest v1")
    add_body(doc, "Thực nghiệm kiểm toán độc lập tại tệp final/experiments/runs/m03_random_forest_v1_train_gap_20261105T045926Z/summary_train_gap.json chỉ ra hiện tượng học quá khớp nghiêm trọng ở mô hình Random Forest phiên bản 1:")
    add_bullet(doc, "Độ chính xác Accuracy đạt 100,0% và điểm Macro-F1 đạt 1,0000.", bold_prefix="Trên tập huấn luyện: ")
    add_bullet(doc, "Độ chính xác Accuracy chỉ đạt 76,91% và điểm Macro-F1 chỉ đạt 0,6852.", bold_prefix="Trên tập kiểm định chéo: ")
    add_bullet(doc, "Lên tới 0,3148 về Macro-F1, tương đương 31,48%, và 0,2309 về Accuracy, tương đương 23,09%.", bold_prefix="Khoảng cách chênh lệch Train-Validation Gap: ")
    add_body(doc, "Nguyên nhân kỹ thuật trực tiếp là do mô hình Random Forest v1 sử dụng cấu hình mặc định không giới hạn độ sâu max_depth=None, số mẫu tối thiểu ở nút lá min_samples_leaf bằng 1. Các cây con tự do phân nhánh cho đến khi mọi nút lá đều thuần nhất tuyệt đối, dẫn đến mô hình học vẹt toàn bộ các quan sát huấn luyện và mất đi tính khái quát hóa trên dữ liệu chưa nhìn thấy.")

    add_image_safe(doc, 'figures_report/fig5_train_val_gap_overfitting.png', width_cm=15.0, 
                   caption="Hình 5. Kiểm toán khoảng cách hiệu năng giữa tập huấn luyện và kiểm định")

    add_body(doc, "Ngược lại, ở Decision Tree v2 sau khi áp dụng Nested Cross-Validation để giới hạn độ sâu và cắt tỉa ccp_alpha bằng 0,002, khoảng cách chênh lệch Train-Validation Gap đã giảm từ 0,3836 xuống chỉ còn 0,0305, tức 3,05%. Ở các mô hình tuyến tính Logistic Regression v1 và v2, khoảng cách gap duy trì ở mức an toàn từ 0,0527 đến 0,0625 nhờ cơ chế điều chuẩn hàm phạt L2.")

    add_heading_2(doc, "6.5. Phân tích nguyên nhân khó khăn nhận diện lớp Enrolled")
    add_body(doc, "Trên toàn bộ các mô hình học máy chưa áp dụng điều chỉnh trọng số như Logistic Regression v1, Decision Tree v1, Random Forest v1, XGBoost v1, lớp sinh viên còn theo học Enrolled luôn là điểm nghẽn lớn nhất:")
    add_bullet(doc, "Điểm F1-score của lớp Enrolled chỉ dao động từ 0,3607 đến 0,4558; chỉ số Recall chỉ đạt từ 29,76% đến 37,80%. Hơn 60% sinh viên lớp Enrolled bị mô hình dự đoán nhầm sang hai lớp còn lại.", bold_prefix="Hiệu năng thấp: ")
    add_bullet(doc, "Enrolled là trạng thái trung gian chuyển tiếp trong quá trình đào tạo. Về mặt số liệu, sinh viên Enrolled có số tín chỉ tích lũy và điểm trung bình nằm ở khoảng giao thoa giữa nhóm bỏ học và nhóm tốt nghiệp. Một sinh viên Enrolled đạt 3 hoặc 4 môn học kỳ 2 có phân phối thuộc tính rất gần với sinh viên Graduate chậm tiến độ hoặc sinh viên chuẩn bị Dropout.", bold_prefix="Nguyên nhân khách quan: ")
    add_bullet(doc, "Khi áp dụng trọng số cân bằng lớp ở Logistic Regression v2, Recall của Enrolled tăng mạnh từ 37,80% lên 59,37%, nhưng độ chính xác Precision lại giảm từ 57,42% xuống 45,42% và làm Recall của lớp Dropout giảm từ 77,48% xuống 73,61%, bỏ sót thêm 44 trường hợp bỏ học. Đây là sự đánh đổi bắt buộc giữa độ nhạy của lớp thiểu số và độ chính xác tổng thể.", bold_prefix="Đánh đổi kỹ thuật: ")

    add_heading_2(doc, "6.6. Kết quả nghiên cứu đối chứng loại bỏ thành phần Ablation Study")
    add_body(doc, "Nghiên cứu đối chứng do Dương Gia Phát thực hiện trên mô hình cố định Logistic Regression với cùng 5 fold kiểm định đem lại hai kết luận kỹ thuật quan trọng:")
    add_bullet(doc, "Khi loại bỏ 6 biến học kỳ 2, tức chỉ sử dụng 30 thuộc tính trước và trong học kỳ 1, điểm Macro-F1 CV giảm mạnh từ 0,6997 xuống 0,6578, tương đương mức sụt giảm 0,0420 điểm F1, tức giảm 6,0%. Độ chính xác tổng thể giảm từ 77,54% xuống 74,62%. Lớp Enrolled bị ảnh hưởng nặng nề nhất khi Recall sụt giảm từ 37,80% xuống còn 29,92%, giảm 7,88 điểm phần trăm. Kết quả học kỳ 2 là điều kiện tiên quyết để mô hình đạt độ chính xác xấp xỉ 70% Macro-F1. Nếu chỉ dùng dữ liệu học kỳ 1, hệ thống chỉ đạt mức Macro-F1 khoảng 65,78%. Do đó, mô hình hiện tại chỉ phù hợp để triển khai cảnh báo vào thời điểm kết thúc năm học thứ nhất.", bold_prefix="1. Thực nghiệm Ablation B đo lường vai trò của dữ liệu học kỳ 2: ")
    add_bullet(doc, "Khi bổ sung 3 đặc trưng tỷ lệ qua môn và chênh lệch điểm vào 36 biến gốc, thành tổng số 39 thuộc tính, điểm Macro-F1 CV tăng từ 0,6997 lên 0,7031, tức tăng 0,0033 điểm F1, ghi nhận cải thiện trên 4 trong số 5 fold. Độ chính xác Accuracy tăng lên 77,71%; Recall lớp Dropout tăng từ 77,48% lên 77,74%; Recall lớp Enrolled tăng từ 37,80% lên 38,43%. Khoảng cách chênh lệch Train-Validation Gap giảm từ 0,0559 xuống 0,0527, chứng minh việc bổ sung các đặc trưng phi tuyến này giúp cung cấp thêm thông tin phân tách ranh giới sinh viên mà không làm mô hình bị học vẹt.", bold_prefix="2. Thực nghiệm Ablation C đo lường giá trị của 3 đặc trưng tạo mới: ")

    # =========================================================
    # MỤC 7. ĐÁNH GIÁ TIẾN ĐỘ
    # =========================================================
    add_heading_1(doc, "7. Đánh giá tiến độ")

    add_heading_2(doc, "7.1. Công việc đã hoàn thành")
    add_bullet(doc, "Đã thu thập trọn vẹn bộ dữ liệu gốc UCI 697, lưu trữ tại final/data/raw/data.csv và tạo mã băm SHA256 xác thực chống sửa đổi.")
    add_bullet(doc, "Đã thiết lập cấu hình phân chia dữ liệu cố định 80% tập huấn luyện gồm 3.539 mẫu và 20% tập kiểm tra gồm 885 mẫu với seed 42 và 5 fold kiểm định chéo phân tầng.")
    add_bullet(doc, "Đã hoàn thành khám phá dữ liệu trên 3.539 mẫu huấn luyện, chỉ ra được các đặc tính lệch lớp, vai trò của điểm số học kỳ 2 và tình trạng nợ học phí.")
    add_bullet(doc, "Đã xây dựng đường ống tiền xử lý chống rò rỉ dữ liệu, kết hợp chuẩn hóa biến số và mã hóa One-Hot biến danh mục.")
    add_bullet(doc, "Đã hoàn thành 11 lượt chạy thực nghiệm kiểm chứng trên 5 fold chung, bao gồm 2 mốc tham chiếu cơ sở, 4 thuật toán học máy phân loại và 2 cấu hình đối chứng loại bỏ thành phần.")
    add_bullet(doc, "Đã tinh chỉnh siêu tham số cho Decision Tree bằng phương pháp Nested Cross-Validation, giúp kiểm soát khoảng cách học quá khớp từ 0,3836 xuống 0,0305.")
    add_bullet(doc, "Đã thiết lập hệ thống truy vết thực nghiệm chi tiết bằng run ID, mã băm commit và các bảng kết quả CSV.")
    add_bullet(doc, "Đã xây dựng kịch bản tích hợp tự động một bước run_all.py và test_all.py, tự động kiểm toán toàn vẹn dữ liệu SHA256, chạy toàn bộ unit tests và kiểm chứng 5 fold cho các mô hình; đã khai báo đầy đủ gói xgboost trong requirements.txt và cập nhật tài liệu hướng dẫn tại README.md gốc.")

    add_heading_2(doc, "7.2. Khó khăn và hạn chế thực tế")
    add_body(doc, "Từ kết quả kiểm tra đối chiếu và thực nghiệm, nhóm thẳng thắn ghi nhận các khó khăn và hạn chế kỹ thuật cốt lõi cần tập trung giải quyết ở giai đoạn tiếp theo:")
    add_bullet(doc, "Dữ liệu bị mất cân bằng lớp nghiêm trọng. Lớp sinh viên đang theo học Enrolled có ranh giới thuộc tính mờ nhạt giữa bỏ học và tốt nghiệp, khiến các mô hình chưa áp dụng trọng số đều đạt điểm Recall lớp này rất thấp.", bold_prefix="1. Hạn chế về phân phối dữ liệu: ")
    add_bullet(doc, "Mô hình phụ thuộc lớn vào kết quả học tập học kỳ 2, khi bỏ học kỳ 2 thì Macro-F1 giảm 0,0420 điểm. Vì vậy, hệ thống hiện tại chỉ có thể ứng dụng dự đoán sau khi sinh viên đã hoàn thành năm thứ nhất, chưa thể triển khai cảnh báo ngay tại thời điểm tân sinh viên mới nhập học.", bold_prefix="2. Giới hạn về phạm vi ứng dụng: ")
    add_bullet(doc, "Phiên bản Random Forest v1 bị học quá khớp nặng với khoảng cách Train-Validation Gap lên tới 31,48% do chưa được tinh chỉnh giới hạn độ sâu cây và tham số lá trên quy trình chung.", bold_prefix="3. Hạn chế về thuật toán Random Forest: ")
    add_bullet(doc, "Trước đó kho lưu trữ còn thiếu kịch bản chạy tích hợp một bước và chưa khai báo thư viện xgboost; nhóm đã giải quyết dứt điểm các thiếu sót này bằng việc bổ sung run_all.py, test_all.py, cập nhật requirements.txt và bổ sung mô tả đề tài tại README.md gốc.", bold_prefix="4. Hoàn thiện hồ sơ mã nguồn: ")

    add_heading_2(doc, "7.3. Công việc còn lại")
    add_bullet(doc, "Soạn thảo bài thuyết trình định dạng .pptx tóm tắt các phát hiện và kết quả thực nghiệm chính của giai đoạn giữa kỳ.")
    add_bullet(doc, "Tiếp tục tinh chỉnh siêu tham số chuyên sâu cho Random Forest và XGBoost; thử nghiệm kết hợp trọng số lớp và điều chỉnh ngưỡng phân loại để nâng cao chỉ số Recall cho lớp Enrolled và Dropout.")
    add_bullet(doc, "Mở tập kiểm tra độc lập 885 mẫu để đánh giá mô hình tối ưu ở giai đoạn nghiệm thu cuối kỳ.")
    add_bullet(doc, "Xây dựng ứng dụng web demo minh họa bằng Streamlit phục vụ báo cáo bảo vệ đồ án.")
    add_bullet(doc, "Đóng gói toàn bộ sản phẩm thành tệp nén theo đúng quy định nộp bài.")

    add_heading_2(doc, "7.4. Kế hoạch hoàn thành đề tài cuối kỳ")
    add_body(doc, "Kế hoạch triển khai từ nay đến cuối học kỳ được phân chia thành 4 giai đoạn cụ thể:")

    t6 = doc.add_table(rows=5, cols=5)
    t6_headers = ["Giai đoạn", "Mốc thời gian", "Nội dung công việc kỹ thuật cụ thể", "Người phụ trách", "Sản phẩm dự kiến"]
    t6_data = [
        ["Giai đoạn 1", "08/11/2026", "Hoàn thiện tệp Báo cáo tiến độ giữa kỳ .docx, slide thuyết trình .pptx và đóng gói tệp nén Nhom10_StudentDropout_GiuaKy.zip nộp bài giữa kỳ.", "Cả nhóm, Phát chủ trì ghép và nộp", "Tệp Word .docx, slide .pptx và tệp .zip nộp đúng thời hạn."],
        ["Giai đoạn 2", "09/11 đến 15/11/2026", "Đã hoàn thành sớm việc xây dựng script run_all.py, khai báo xgboost và cập nhật README.md gốc; tiếp tục xây dựng các test case mở rộng cho kịch bản tự động.", "Lê Văn Hiếu và Văn Nguyễn Thành Đạt", "Tệp README.md gốc hoàn chỉnh; script run_all.py và test_all.py chạy thông suốt không lỗi."],
        ["Giai đoạn 3", "16/11 đến 25/11/2026", "Tinh chỉnh sâu Random Forest và XGBoost; thử nghiệm kỹ thuật tối ưu ngưỡng quyết định xác suất và kết hợp mô hình Ensemble/Stacking nhằm cải thiện Recall lớp Enrolled.", "Cái Trần Minh Tiến và Văn Nguyễn Thành Đạt", "Nhật ký thực nghiệm bổ sung, bảng so sánh siêu tham số và biểu đồ đường cong PR."],
        ["Giai đoạn 4", "26/11 đến 10/12/2026", "Họp nhóm chốt mô hình vô địch tối ưu; mở tập kiểm tra 885 mẫu để đánh giá độc lập một lần duy nhất; xây dựng giao diện ứng dụng web minh họa bằng Streamlit; soạn thảo báo cáo tổng kết cuối khóa và slide bảo vệ.", "Cả nhóm, Phát và Hiếu phụ trách demo", "Báo cáo cuối kỳ 5 chương, mã nguồn ứng dụng web demo, kết quả đánh giá tập kiểm tra."]
    ]
    format_table(t6, t6_headers, t6_data, [1.8, 2.5, 5.8, 3.2, 3.2], [True, False, False, False, False])

    # =========================================================
    # MỤC 8. PHÂN CÔNG VÀ ĐÓNG GÓP CÁ NHÂN
    # =========================================================
    add_heading_1(doc, "8. Phân công và đóng góp cá nhân")
    add_body(doc, "Dưới đây là bảng kê chi tiết các công việc kỹ thuật cụ thể mà từng thành viên đã trực tiếp thực hiện trong giai đoạn giữa kỳ của đề tài:")

    t7 = doc.add_table(rows=5, cols=6)
    t7_headers = ["STT", "Thành viên", "Mã số sinh viên", "Tác vụ kỹ thuật cụ thể đã thực hiện", "Sản phẩm mã nguồn và minh chứng", "Đóng góp"]
    t7_data = [
        ["1", "Dương Gia Phát", "3124411212", 
         "Trưởng nhóm, định hướng kiến trúc mã nguồn và kiểm soát rò rỉ dữ liệu.\nThiết lập bộ chia dữ liệu cố định student_dropout_seed42_v1 gồm 3.539 Train và 885 Test.\nXây dựng 3 đặc trưng mới tỷ lệ qua môn HK1, HK2 và chênh lệch điểm có xử lý an toàn mẫu số bằng 0.\nThiết kế và thực hiện nghiên cứu đối chứng loại bỏ thành phần Ablation Study A, B, C trên mô hình Logistic Regression.\nQuản lý kho lưu trữ GitHub và giải quyết các xung đột mã nguồn.", 
         "final/src/features.py\nfinal/experiments/ablation.csv\nThư mục chạy m05_logistic_regression_ablation_b và ablation_c\n13 commits trên kho lưu trữ", 
         "25%"],
        ["2", "Lê Văn Hiếu", "3124411091", 
         "Thu thập dữ liệu nguồn UCI 697, tạo tệp mã băm SHA256 xác thực.\nXây dựng đường ống tiền xử lý dữ liệu ColumnTransformer kết hợp StandardScaler và OneHotEncoder.\nTriển khai mô hình tham chiếu cơ sở DummyClassifier v1.\nHuấn luyện mô hình Logistic Regression phiên bản 1 trên 5 fold kiểm định chung.\nThiết lập cấu hình và đồng bộ nhật ký thực nghiệm Weights and Biases.", 
         "final/data/source_manifest.json\nfinal/configs/lr_preprocessing_v1.json\nfinal/notebooks/m01_baseline/v1.ipynb\nfinal/notebooks/m05_logistic_regression/v1.ipynb\n15 commits trên kho lưu trữ", 
         "25%"],
        ["3", "Văn Nguyễn Thành Đạt", "3124411067", 
         "Thực hiện phân tích khám phá dữ liệu trên 3.539 mẫu tập huấn luyện, trực quan hóa phân phối nhãn, tương quan điểm số và nợ học phí.\nXây dựng mô hình Decision Tree phiên bản 1 và khảo sát tham số độ sâu.\nTriển khai mô hình Logistic Regression phiên bản 2 với trọng số cân bằng lớp.\nTriển khai mô hình DummyClassifier phiên bản 2 và mô hình XGBoost phiên bản 1.\nPhụ trách hợp nhất các Pull Request kỹ thuật trên Git.", 
         "Notebook ThanhDat_EDA_DecisionTree.ipynb\nfinal/notebooks/m02_decision_tree/v1.ipynb\nfinal/notebooks/m04_xgboost/v1.ipynb\nfinal/notebooks/m05_logistic_regression/v2.ipynb\nPull Request số 6, 8, 9, 12; 27 commits", 
         "25%"],
        ["4", "Cái Trần Minh Tiến", "3124411309", 
         "Huấn luyện mô hình Random Forest phiên bản 1 gồm 100 cây trên 5 fold kiểm định.\nKiểm toán khoảng cách học quá khớp Train-Validation Gap của Random Forest v1.\nTriển khai mô hình Decision Tree phiên bản 2 kết hợp mã hóa One-Hot và thẩm định chéo lồng nhau Nested Cross-Validation với 24 ứng viên.\nTổng hợp số liệu các lần chạy vào nhật ký thực nghiệm và chuẩn hóa ảnh kết quả.\nSoạn thảo nội dung lý thuyết và kết quả của các mô hình cây.", 
         "Thư mục m03_random_forest_v1_train_gap_20261105T045926Z\nThư mục m02_decision_tree_v2_kaggle\nfinal/notebooks/m03_random_forest/v1.ipynb\nPull Request số 13, 14; 16 commits", 
         "25%"]
    ]
    format_table(t7, t7_headers, t7_data, [0.8, 2.5, 2.0, 5.8, 4.2, 1.2], [True, False, True, False, False, True])

    add_body(doc, "Toàn bộ 4 thành viên trong nhóm đều tham gia tích cực, có cam kết mã nguồn thực tế trên kho lưu trữ Git và hoàn thành 100% khối lượng công việc kỹ thuật được phân công cho giai đoạn giữa kỳ.", space_after=12)

    # Output file
    output_path = r"c:\Users\giuag\.gemini\antigravity\scratch\DCT124C1-MH-Nhom\BaoCao_TienDo_GiuaKy_Nhom10.docx"
    doc.save(output_path)
    print(f"Report successfully generated at: {output_path}")

if __name__ == '__main__':
    build_document()
