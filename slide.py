import streamlit as st
import base64
from io import BytesIO
import json

# Cấu hình trang
st.set_page_config(
    page_title="Trình Tạo Slide 3D - Điện & An Toàn Lao Động",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    /* Nền gradient chuyên nghiệp */
    .stApp {
        background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
    }
    
    /* Tiêu đề chính */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Phụ đề */
    .sub-title {
        text-align: center;
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Card mẫu slide */
    .template-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
    }
    
    .template-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Nút tùy chỉnh */
    .stButton > button {
        background: linear-gradient(45deg, #1a2980 0%, #26d0ce 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Vùng nhập liệu */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
    }
    
    /* Tiêu đề section */
    .section-header {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #26d0ce;
        padding-left: 15px;
    }
    
    /* Hiệu ứng 3D cho preview */
    .slide-preview-3d {
        transform: perspective(1000px) rotateY(-10deg) rotateX(5deg);
        transition: transform 0.5s ease;
        box-shadow: -20px 20px 40px rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        overflow: hidden;
        background: white;
    }
    
    .slide-preview-3d:hover {
        transform: perspective(1000px) rotateY(0deg) rotateX(0deg);
    }
    
    /* Badge cho template */
    .template-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: white;
        font-weight: 500;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(26, 41, 128, 0.9) !important;
        color: white !important;
    }
    
    /* Preview container */
    .preview-container {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Tiêu đề ứng dụng
st.markdown('<h1 class="main-title">⚡ Trình Tạo Slide 3D - Điện & An Toàn Lao Động</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tạo bài thuyết trình chuyên nghiệp về điện, trạm biến áp, ATVSLĐ và HSE</p>', unsafe_allow_html=True)

# Khởi tạo session state
if 'slide_data' not in st.session_state:
    st.session_state.slide_data = {
        'title': 'An Toàn Điện Trong Trạm Biến Áp',
        'content': 'Nguyên tắc và quy trình an toàn khi làm việc với thiết bị điện cao áp',
        'template': 'Điện Lực An Toàn'
    }

# Các mẫu slide chuyên ngành điện & ATLĐ
TEMPLATES = {
    "Điện Lực An Toàn": {
        "primary_color": "#1a2980",
        "secondary_color": "#26d0ce",
        "accent_color": "#ff6b6b",
        "font": "Arial, sans-serif",
        "style": "corporate",
        "description": "Mẫu chuyên nghiệp cho lĩnh vực điện lực và an toàn",
        "tags": ["Điện", "An Toàn", "Trạm Biến Áp"],
        "icon": "⚡"
    },
    "HSE Chuyên Nghiệp": {
        "primary_color": "#2E7D32",
        "secondary_color": "#4CAF50",
        "accent_color": "#FFC107",
        "font": "Segoe UI, sans-serif",
        "style": "hse",
        "description": "Mẫu dành cho An toàn - Sức khỏe - Môi trường (HSE)",
        "tags": ["HSE", "An Toàn", "Môi Trường"],
        "icon": "🛡️"
    },
    "Trạm Biến Áp": {
        "primary_color": "#37474F",
        "secondary_color": "#607D8B",
        "accent_color": "#FF9800",
        "font": "Roboto, sans-serif",
        "style": "technical",
        "description": "Mẫu kỹ thuật cho trình bày về trạm biến áp",
        "tags": ["Trạm Biến Áp", "Kỹ Thuật", "Điện"],
        "icon": "🏭"
    },
    "ATVSLĐ Cảnh Báo": {
        "primary_color": "#B71C1C",
        "secondary_color": "#F44336",
        "accent_color": "#FFEB3B",
        "font": "Impact, sans-serif",
        "style": "warning",
        "description": "Mẫu cảnh báo nguy hiểm cho ATVSLĐ",
        "tags": ["ATVSLĐ", "Cảnh Báo", "Nguy Hiểm"],
        "icon": "⚠️"
    },
    "Quy Trình Điện": {
        "primary_color": "#0D47A1",
        "secondary_color": "#2196F3",
        "accent_color": "#00BCD4",
        "font": "Consolas, monospace",
        "style": "process",
        "description": "Mẫu trình bày quy trình và sơ đồ điện",
        "tags": ["Quy Trình", "Sơ Đồ", "Điện"],
        "icon": "📋"
    }
}

# Hàm tạo HTML cho slide
def generate_slide_html(title, content, template_name):
    template = TEMPLATES[template_name]
    
    html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: {template['font']};
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, {template['primary_color']}, {template['secondary_color']});
                perspective: 1200px;
                overflow: hidden;
            }}
            
            .slide-3d-container {{
                width: 90%;
                max-width: 1200px;
                height: 80vh;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
                transform-style: preserve-3d;
                transform: rotateY(-15deg) rotateX(10deg);
                transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
            }}
            
            .slide-3d-container:hover {{
                transform: rotateY(-5deg) rotateX(5deg);
            }}
            
            .slide-header {{
                background: linear-gradient(to right, {template['primary_color']}, {template['secondary_color']});
                color: white;
                padding: 30px 40px;
                border-radius: 20px 20px 0 0;
            }}
            
            .slide-title {{
                font-size: 3.2rem;
                font-weight: 900;
                margin-bottom: 10px;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            
            .slide-subtitle {{
                font-size: 1.4rem;
                opacity: 0.9;
                font-weight: 300;
            }}
            
            .slide-content {{
                padding: 40px;
                color: #333;
            }}
            
            .content-main {{
                font-size: 1.8rem;
                line-height: 1.6;
                margin-bottom: 30px;
            }}
            
            .content-bullets {{
                font-size: 1.5rem;
                line-height: 1.8;
                margin-left: 20px;
            }}
            
            .content-bullets li {{
                margin-bottom: 15px;
                position: relative;
                padding-left: 10px;
            }}
            
            .content-bullets li:before {{
                content: "{template['icon']}";
                position: absolute;
                left: -25px;
                color: {template['accent_color']};
            }}
            
            .slide-footer {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(0, 0, 0, 0.05);
                padding: 20px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 2px solid {template['accent_color']};
            }}
            
            .template-name {{
                font-weight: 700;
                color: {template['primary_color']};
                font-size: 1.2rem;
            }}
            
            .slide-number {{
                font-size: 1.1rem;
                color: #666;
            }}
            
            .corner-decoration {{
                position: absolute;
                width: 300px;
                height: 300px;
                background: {template['accent_color']};
                opacity: 0.1;
                border-radius: 50%;
                top: -150px;
                right: -150px;
            }}
            
            .corner-decoration-2 {{
                position: absolute;
                width: 200px;
                height: 200px;
                background: {template['secondary_color']};
                opacity: 0.1;
                border-radius: 50%;
                bottom: -100px;
                left: -100px;
            }}
            
            .warning-note {{
                background: rgba(255, 235, 59, 0.2);
                border-left: 5px solid {template['accent_color']};
                padding: 20px;
                margin: 20px 0;
                border-radius: 0 10px 10px 0;
            }}
            
            @media (max-width: 768px) {{
                .slide-title {{
                    font-size: 2.2rem;
                }}
                
                .content-main {{
                    font-size: 1.4rem;
                }}
                
                .content-bullets {{
                    font-size: 1.2rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="slide-3d-container">
            <div class="corner-decoration"></div>
            <div class="corner-decoration-2"></div>
            
            <div class="slide-header">
                <h1 class="slide-title">{title}</h1>
                <div class="slide-subtitle">Trình bày chuyên đề điện & an toàn lao động</div>
            </div>
            
            <div class="slide-content">
                <div class="content-main">
                    {content if '\n' not in content else content.split('\n')[0]}
                </div>
                
                {"<ul class='content-bullets'>" + ''.join([f'<li>{line.strip()}</li>' for line in content.split('\n')[1:] if line.strip()]) + "</ul>" if '\n' in content else ""}
                
                <div class="warning-note">
                    <strong>Lưu ý an toàn:</strong> Tuân thủ quy trình 5S và các quy định về ATVSLĐ khi làm việc với thiết bị điện.
                </div>
            </div>
            
            <div class="slide-footer">
                <div class="template-name">{template_name} {template['icon']}</div>
                <div class="slide-number">Slide trình chiếu 3D | Ngành Điện & ATLĐ</div>
            </div>
        </div>
        
        <script>
            // Thêm hiệu ứng 3D khi di chuột
            const slide = document.querySelector('.slide-3d-container');
            document.addEventListener('mousemove', (e) => {{
                const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
                const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
                slide.style.transform = `rotateY(${{-15 + xAxis}}deg) rotateX(${{10 - yAxis}}deg)`;
            }});
        </script>
    </body>
    </html>
    """
    
    return html

# Hàm tạo trình chiếu đầy đủ
def generate_full_presentation(slides, template_name):
    template = TEMPLATES[template_name]
    
    slides_html = ""
    for i, slide in enumerate(slides):
        slides_html += f"""
        <section class="presentation-slide" data-background="linear-gradient(135deg, {template['primary_color']}, {template['secondary_color']})">
            <div class="slide-inner">
                <h2>{slide['title']}</h2>
                <div class="slide-content">
                    {slide['content'].replace('\n', '<br>')}
                </div>
                <div class="slide-footer">
                    <span class="slide-num">Slide {i+1}/{len(slides)}</span>
                    <span class="template-badge">{template_name}</span>
                </div>
            </div>
        </section>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trình Chiếu Điện & ATLĐ - {template_name}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/theme/black.css">
        <style>
            .reveal .slides {{
                perspective: 1000px;
            }}
            
            .presentation-slide {{
                background: rgba(255, 255, 255, 0.95) !important;
                border-radius: 20px;
                padding: 40px !important;
                transform-style: preserve-3d;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                border: 3px solid {template['accent_color']};
            }}
            
            .presentation-slide h2 {{
                color: {template['primary_color']};
                font-size: 3.5rem;
                margin-bottom: 30px;
                border-bottom: 3px solid {template['accent_color']};
                padding-bottom: 15px;
            }}
            
            .slide-content {{
                font-size: 2rem;
                line-height: 1.6;
                color: #333;
                text-align: left;
            }}
            
            .slide-footer {{
                position: absolute;
                bottom: 20px;
                width: calc(100% - 80px);
                display: flex;
                justify-content: space-between;
                font-size: 1.2rem;
                color: #666;
            }}
            
            .template-badge {{
                background: {template['accent_color']};
                color: #000;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
            }}
            
            .reveal .progress {{
                color: {template['accent_color']};
            }}
            
            .reveal .controls {{
                color: {template['accent_color']};
            }}
        </style>
    </head>
    <body>
        <div class="reveal">
            <div class="slides">
                {slides_html}
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.js"></script>
        <script>
            Reveal.initialize({{
                hash: true,
                transition: 'convex',
                backgroundTransition: 'slide',
                width: "90%",
                height: "90%",
                margin: 0.1,
                minScale: 0.2,
                maxScale: 2.0
            }});
        </script>
    </body>
    </html>
    """
    
    return html

# Sidebar với các tùy chọn
with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Cài Đặt Slide</div>', unsafe_allow_html=True)
    
    # Chọn mẫu
    selected_template = st.selectbox(
        "Chọn mẫu trình chiếu",
        list(TEMPLATES.keys()),
        index=0
    )
    
    # Hiển thị thông tin mẫu
    template_info = TEMPLATES[selected_template]
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 1.5rem; margin-right: 10px;">{template_info['icon']}</span>
            <h4 style="color: white; margin: 0;">{selected_template}</h4>
        </div>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0; font-size: 0.9rem;">{template_info['description']}</p>
        <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px;">
    """, unsafe_allow_html=True)
    
    for tag in template_info['tags']:
        st.markdown(f'<span class="template-badge" style="background: {template_info["accent_color"]}; color: #000;">{tag}</span>', unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tùy chọn nội dung
    st.markdown('<div class="section-header">📝 Cấu Hình</div>', unsafe_allow_html=True)
    
    # Tự động cập nhật session state khi chọn template
    if st.button("🔄 Áp dụng mẫu đã chọn", use_container_width=True):
        st.session_state.slide_data['template'] = selected_template
        st.success(f"Đã áp dụng mẫu {selected_template}")
    
    st.markdown("---")
    
    # Thông tin ứng dụng
    st.markdown("""
    <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 20px;">
        <p><strong>Chuyên ngành hỗ trợ:</strong></p>
        <ul style="padding-left: 20px;">
            <li>Kỹ thuật điện</li>
            <li>Trạm biến áp</li>
            <li>An toàn vệ sinh lao động</li>
            <li>HSE (Sức khỏe - An toàn - Môi trường)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Tab chính
tab1, tab2, tab3 = st.tabs(["📝 Nhập Nội Dung", "👁️ Xem Trước Slide", "💾 Xuất File"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">📋 Nhập Nội Dung Slide</div>', unsafe_allow_html=True)
        
        # Nhập tiêu đề
        slide_title = st.text_input(
            "Tiêu đề slide",
            value=st.session_state.slide_data['title'],
            key="input_title"
        )
        
        # Nhập nội dung
        slide_content = st.text_area(
            "Nội dung slide (mỗi dòng là một gạch đầu dòng)",
            value=st.session_state.slide_data['content'],
            height=200,
            key="input_content",
            help="Mỗi dòng sẽ được hiển thị như một gạch đầu dòng. Dòng đầu tiên là nội dung chính."
        )
        
        # Cập nhật session state
        if st.button("🎬 Cập nhật & Xem trước", type="primary", use_container_width=True):
            st.session_state.slide_data['title'] = slide_title
            st.session_state.slide_data['content'] = slide_content
            st.session_state.slide_data['template'] = selected_template
            st.success("Đã cập nhật nội dung slide!")
    
    with col2:
        st.markdown('<div class="section-header">📊 Mẫu Nội Dung Nhanh</div>', unsafe_allow_html=True)
        
        # Các mẫu nội dung cho ngành điện & ATLĐ
        quick_templates = {
            "An Toàn Điện Cao Áp": {
                "title": "Quy Trình An Toàn Điện Cao Áp",
                "content": """Nguyên tắc làm việc an toàn với điện cao áp
Kiểm tra thiết bị bảo hộ trước khi làm việc
Sử dụng đầy đủ trang thiết bị bảo hộ cá nhân
Thực hiện quy trình cô lập nguồn điện 5 bước
Kiểm tra không còn điện trước khi tiếp cận
Bố trí người giám sát an toàn"""
            },
            "Bảo Trì Trạm Biến Áp": {
                "title": "Quy Trình Bảo Trì Trạm Biến Áp",
                "content": """Kiểm tra định kỳ thiết bị trạm biến áp
Vệ sinh và bảo dưỡng máy biến áp
Kiểm tra hệ thống làm mát
Đo đạc thông số kỹ thuật
Phát hiện và xử lý sự cố
Lập báo cáo bảo trì"""
            },
            "Huấn Luyện ATVSLĐ": {
                "title": "Chương Trình Huấn Luyện ATVSLĐ",
                "content": """Đào tạo nhận diện mối nguy hiểm
Huấn luyện sơ cứu tai nạn điện
Sử dụng thiết bị bảo hộ cá nhân
Quy trình ứng phó sự cố
Thực hành an toàn tại hiện trường
Đánh giá và cấp chứng chỉ"""
            },
            "Kiểm Tra HSE": {
                "title": "Checklist Kiểm Tra HSE Định Kỳ",
                "content": """Kiểm tra hệ thống chống sét
Đánh giá rủi ro môi trường làm việc
Kiểm tra thiết bị PCCC
Đánh giá yếu tố vi khí hậu
Kiểm tra hệ thống thông gió
Giám sát chất lượng không khí"""
            }
        }
        
        for template_name, template_data in quick_templates.items():
            with st.container():
                st.markdown(f"""
                <div class="template-card" onclick="this.style.transform='scale(0.98)'; setTimeout(()=>this.style.transform='', 200)">
                    <h4 style="color: white; margin-top: 0;">{template_name}</h4>
                    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{template_data['title']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Sử dụng mẫu này", key=f"btn_{template_name}", use_container_width=True):
                    st.session_state.slide_data['title'] = template_data['title']
                    st.session_state.slide_data['content'] = template_data['content']
                    st.rerun()

with tab2:
    st.markdown('<div class="section-header">👁️ Xem Trước Slide 3D</div>', unsafe_allow_html=True)
    
    # Hiển thị thông tin slide hiện tại
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Tiêu đề", st.session_state.slide_data['title'])
    with col_info2:
        st.metric("Mẫu đang dùng", st.session_state.slide_data['template'])
    with col_info3:
        st.metric("Số dòng nội dung", len(st.session_state.slide_data['content'].split('\n')))
    
    # Tạo và hiển thị slide
    slide_html = generate_slide_html(
        st.session_state.slide_data['title'],
        st.session_state.slide_data['content'],
        st.session_state.slide_data['template']
    )
    
    # Hiển thị slide trong iframe
    st.markdown('<div class="preview-container">', unsafe_allow_html=True)
    st.components.v1.html(slide_html, height=700, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hướng dẫn
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">💡 Hướng dẫn xem slide 3D:</h4>
        <ul style="color: rgba(255,255,255,0.9);">
            <li>Di chuyển chuột trên slide để xem hiệu ứng 3D</li>
            <li>Slide tự động định dạng nội dung theo gạch đầu dòng</li>
            <li>Màu sắc và biểu tượng phù hợp với chuyên ngành điện & ATLĐ</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">💾 Xuất Slide Trình Chiếu</div>', unsafe_allow_html=True)
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: white; margin-top: 0;">📥 Xuất Slide Đơn</h4>
            <p style="color: rgba(255,255,255,0.9); font-size: 0.95rem;">Tải về slide hiện tại dưới dạng file HTML có thể chạy độc lập trên mọi trình duyệt.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tạo slide đơn
        slide_html = generate_slide_html(
            st.session_state.slide_data['title'],
            st.session_state.slide_data['content'],
            st.session_state.slide_data['template']
        )
        
        # Tạo file download
        b64 = base64.b64encode(slide_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="slide_dien_atld.html" style="text-decoration: none;">'
        
        st.markdown(f"""
        <div style="text-align: center;">
            {href}
                <button style="background: linear-gradient(45deg, #1a2980 0%, #26d0ce 100%); color: white; border: none; padding: 15px 30px; border-radius: 30px; font-weight: 600; font-size: 1rem; cursor: pointer; width: 100%;">
                    ⚡ Tải Slide Đơn (HTML)
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col_export2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: white; margin-top: 0;">🎬 Tạo Trình Chiếu Nhiều Slide</h4>
            <p style="color: rgba(255,255,255,0.9); font-size: 0.95rem;">Thêm nhiều slide để tạo bài thuyết trình đầy đủ với hiệu ứng chuyển slide.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quản lý nhiều slide
        if 'all_slides' not in st.session_state:
            st.session_state.all_slides = []
        
        # Form thêm slide mới
        with st.form("add_slide_form"):
            new_title = st.text_input("Tiêu đề slide mới", "Slide mới")
            new_content = st.text_area("Nội dung slide mới", "Nội dung chi tiết...", height=100)
            
            col_add1, col_add2 = st.columns(2)
            with col_add1:
                add_submitted = st.form_submit_button("➕ Thêm vào trình chiếu", use_container_width=True)
            with col_add2:
                clear_submitted = st.form_submit_button("🗑️ Xóa tất cả", use_container_width=True)
        
        if add_submitted and new_title:
            st.session_state.all_slides.append({
                'title': new_title,
                'content': new_content
            })
            st.success(f"Đã thêm slide: {new_title}")
        
        if clear_submitted:
            st.session_state.all_slides = []
            st.success("Đã xóa tất cả slide")
        
        # Hiển thị danh sách slide
        if st.session_state.all_slides:
            st.markdown("##### Danh sách slide trong trình chiếu")
            for i, slide in enumerate(st.session_state.all_slides):
                with st.expander(f"Slide {i+1}: {slide['title']}"):
                    st.write(slide['content'])
            
            # Tạo trình chiếu đầy đủ
            all_slides_for_presentation = [st.session_state.slide_data] + st.session_state.all_slides
            presentation_html = generate_full_presentation(all_slides_for_presentation, st.session_state.slide_data['template'])
            
            # Tạo file download
            b64_presentation = base64.b64encode(presentation_html.encode()).decode()
            href_presentation = f'<a href="data:text/html;base64,{b64_presentation}" download="trinh_chieu_dien_atld.html" style="text-decoration: none;">'
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 20px;">
                {href_presentation}
                    <button style="background: linear-gradient(45deg, #FF416C 0%, #FF4B2B 100%); color: white; border: none; padding: 15px 30px; border-radius: 30px; font-weight: 600; font-size: 1rem; cursor: pointer; width: 100%;">
                        🎬 Tải Trình Chiếu Đầy Đủ ({len(all_slides_for_presentation)} slide)
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    # Hướng dẫn sử dụng
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📖 Hướng dẫn sử dụng file xuất:</h4>
        <ol style="color: rgba(255,255,255,0.9);">
            <li>Tải file HTML về máy tính</li>
            <li>Mở file bằng trình duyệt web (Chrome, Firefox, Edge)</li>
            <li>Slide sẽ hiển thị với hiệu ứng 3D đầy đủ</li>
            <li>Đối với trình chiếu nhiều slide: sử dụng phím mũi tên để chuyển slide</li>
            <li>Có thể trình chiếu trực tiếp từ file HTML mà không cần internet</li>
        </ol>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem;"><strong>Lưu ý:</strong> File HTML có chứa hiệu ứng 3D và hoạt ảnh, đảm bảo trình duyệt hỗ trợ CSS3.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px;">
    <p><strong>Trình Tạo Slide 3D - Chuyên Ngành Điện & An Toàn Lao Động</strong></p>
    <p>Ứng dụng tạo bài thuyết trình chuyên nghiệp cho kỹ sư điện, kỹ thuật viên trạm biến áp, và chuyên gia HSE</p>
    <p style="font-size: 0.9rem;">© 2024 - Hỗ trợ: Kỹ thuật Điện | Trạm Biến Áp | ATVSLĐ | HSE</p>
</div>
""", unsafe_allow_html=True)
