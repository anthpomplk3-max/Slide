import streamlit as st
import base64
from io import BytesIO
import json
import random

# Cấu hình trang
st.set_page_config(
    page_title="Trình Tạo Slide 3D Chuyên Nghiệp",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    /* Nền gradient chuyên nghiệp */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tiêu đề chính */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3.5rem;
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
    }
    
    .template-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Nút tùy chỉnh */
    .stButton > button {
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
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
    
    /* Thanh sidebar */
    .css-1d391kg {
        background: rgba(30, 30, 46, 0.8);
    }
    
    /* Tiêu đề section */
    .section-header {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #6a11cb;
        padding-left: 15px;
    }
    
    /* Hiệu ứng 3D cho preview */
    .slide-preview-3d {
        transform: perspective(1000px) rotateY(-10deg) rotateX(5deg);
        transition: transform 0.5s ease;
        box-shadow: -20px 20px 40px rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .slide-preview-3d:hover {
        transform: perspective(1000px) rotateY(0deg) rotateX(0deg);
    }
    
    /* Hiệu ứng cho tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: white;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(106, 17, 203, 0.9) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Tiêu đề ứng dụng
st.markdown('<h1 class="main-title">🎬 Trình Tạo Slide 3D Chuyên Nghiệp</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tạo bài thuyết trình ấn tượng với hiệu ứng 3D và mẫu chuyên nghiệp</p>', unsafe_allow_html=True)

# Các mẫu slide chuyên nghiệp
TEMPLATES = {
    "Corporate Blue": {
        "primary_color": "#1a237e",
        "secondary_color": "#0d47a1",
        "accent_color": "#2196f3",
        "font": "Arial, sans-serif",
        "style": "corporate",
        "description": "Mẫu chuyên nghiệp phù hợp cho doanh nghiệp và báo cáo công ty"
    },
    "Creative Orange": {
        "primary_color": "#bf360c",
        "secondary_color": "#ff5722",
        "accent_color": "#ff9800",
        "font": "Segoe UI, sans-serif",
        "style": "creative",
        "description": "Mẫu sáng tạo với màu sắc nổi bật cho các bài thuyết trình marketing"
    },
    "Elegant Purple": {
        "primary_color": "#4a148c",
        "secondary_color": "#7b1fa2",
        "accent_color": "#e1bee7",
        "font": "Georgia, serif",
        "style": "elegant",
        "description": "Mẫu thanh lịch phù hợp cho sự kiện và hội nghị quan trọng"
    },
    "Tech Green": {
        "primary_color": "#1b5e20",
        "secondary_color": "#388e3c",
        "accent_color": "#4caf50",
        "font": "Consolas, monospace",
        "style": "tech",
        "description": "Mẫu công nghệ với phong cách hiện đại cho các bài thuyết trình kỹ thuật"
    },
    "Minimal White": {
        "primary_color": "#263238",
        "secondary_color": "#546e7a",
        "accent_color": "#ffffff",
        "font": "Helvetica, sans-serif",
        "style": "minimal",
        "description": "Mẫu tối giản với thiết kế sạch sẽ và tập trung vào nội dung"
    }
}

# Hàm tạo HTML cho slide
def generate_slide_html(title, content, template_name, slide_type="title"):
    template = TEMPLATES[template_name]
    
    if slide_type == "title":
        html = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
                
                body {{
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(135deg, {template['primary_color']}, {template['secondary_color']});
                    font-family: {template['font']};
                    color: white;
                    perspective: 1000px;
                    overflow: hidden;
                }}
                
                .slide-container {{
                    width: 90vw;
                    height: 85vh;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    padding: 40px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transform-style: preserve-3d;
                    animation: float 6s ease-in-out infinite;
                }}
                
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px) rotateX(5deg) rotateY(-5deg); }}
                    50% {{ transform: translateY(-20px) rotateX(3deg) rotateY(-7deg); }}
                }}
                
                .title {{
                    font-size: 4.5rem;
                    font-weight: 900;
                    margin-bottom: 20px;
                    text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
                    color: {template['accent_color']};
                    transform: translateZ(50px);
                }}
                
                .subtitle {{
                    font-size: 1.8rem;
                    font-weight: 400;
                    max-width: 80%;
                    line-height: 1.5;
                    opacity: 0.9;
                    transform: translateZ(30px);
                }}
                
                .presenter {{
                    position: absolute;
                    bottom: 40px;
                    right: 40px;
                    font-size: 1.2rem;
                    opacity: 0.7;
                }}
                
                .logo {{
                    position: absolute;
                    top: 40px;
                    left: 40px;
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: {template['accent_color']};
                }}
                
                .corner-decoration {{
                    position: absolute;
                    width: 200px;
                    height: 200px;
                    background: {template['accent_color']};
                    opacity: 0.1;
                    border-radius: 50%;
                    top: -100px;
                    right: -100px;
                }}
                
                .corner-decoration-2 {{
                    position: absolute;
                    width: 150px;
                    height: 150px;
                    background: {template['accent_color']};
                    opacity: 0.1;
                    border-radius: 50%;
                    bottom: -75px;
                    left: -75px;
                }}
            </style>
        </head>
        <body>
            <div class="slide-container">
                <div class="corner-decoration"></div>
                <div class="corner-decoration-2"></div>
                <div class="logo">TRÌNH CHIẾU 3D</div>
                <h1 class="title">{title}</h1>
                <p class="subtitle">{content}</p>
                <div class="presenter">Thuyết trình bởi: {template_name}</div>
            </div>
        </body>
        </html>
        """
    elif slide_type == "content":
        html = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
                
                body {{
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(135deg, {template['primary_color']}, {template['secondary_color']});
                    font-family: {template['font']};
                    color: white;
                    perspective: 1000px;
                    overflow: hidden;
                }}
                
                .slide-container {{
                    width: 90vw;
                    height: 85vh;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
                    display: flex;
                    padding: 40px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transform-style: preserve-3d;
                    animation: float 6s ease-in-out infinite;
                    position: relative;
                }}
                
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px) rotateX(5deg) rotateY(5deg); }}
                    50% {{ transform: translateY(-20px) rotateX(3deg) rotateY(7deg); }}
                }}
                
                .content-left {{
                    flex: 1;
                    padding-right: 40px;
                    transform: translateZ(40px);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }}
                
                .content-right {{
                    flex: 1;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    transform: translateZ(60px);
                }}
                
                .slide-title {{
                    font-size: 3.5rem;
                    font-weight: 700;
                    margin-bottom: 30px;
                    color: {template['accent_color']};
                    line-height: 1.2;
                }}
                
                .slide-content {{
                    font-size: 1.5rem;
                    line-height: 1.8;
                    opacity: 0.9;
                }}
                
                .content-box {{
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 15px;
                    padding: 30px;
                    width: 100%;
                    max-height: 60vh;
                    overflow-y: auto;
                }}
                
                .content-box::-webkit-scrollbar {{
                    width: 8px;
                }}
                
                .content-box::-webkit-scrollbar-track {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                }}
                
                .content-box::-webkit-scrollbar-thumb {{
                    background: {template['accent_color']};
                    border-radius: 10px;
                }}
                
                .slide-number {{
                    position: absolute;
                    bottom: 30px;
                    right: 40px;
                    font-size: 1.2rem;
                    opacity: 0.7;
                }}
                
                .graphic-element {{
                    width: 300px;
                    height: 300px;
                    background: {template['accent_color']};
                    opacity: 0.2;
                    border-radius: 50%;
                    position: absolute;
                    top: -150px;
                    right: -150px;
                }}
                
                ul, ol {{
                    margin-left: 20px;
                }}
                
                li {{
                    margin-bottom: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="slide-container">
                <div class="graphic-element"></div>
                <div class="content-left">
                    <h1 class="slide-title">{title}</h1>
                    <div class="content-box">
                        <div class="slide-content">{content.replace('\n', '<br>')}</div>
                    </div>
                </div>
                <div class="content-right">
                    <div style="font-size: 5rem; color: {template['accent_color']}; opacity: 0.5;">📊</div>
                </div>
                <div class="slide-number">Slide Nội Dung</div>
            </div>
        </body>
        </html>
        """
    
    return html

# Hàm tạo HTML đầy đủ cho trình chiếu
def generate_presentation_html(slides_data, template_name):
    template = TEMPLATES[template_name]
    
    slides_html = ""
    for i, slide in enumerate(slides_data):
        if i == 0:
            slides_html += f"""
            <section class="slide-3d" data-background="linear-gradient(135deg, {template['primary_color']}, {template['secondary_color']})">
                <div class="slide-title-container">
                    <h1 style="color: {template['accent_color']}; font-size: 4rem;">{slide['title']}</h1>
                    <p style="font-size: 2rem; opacity: 0.9;">{slide['content']}</p>
                </div>
                <div class="presenter-info">
                    <p>Mẫu: {template_name}</p>
                </div>
            </section>
            """
        else:
            slides_html += f"""
            <section class="slide-3d" data-background="linear-gradient(135deg, {template['secondary_color']}, {template['primary_color']})">
                <h2 style="color: {template['accent_color']};">{slide['title']}</h2>
                <div class="content-box-3d">
                    {slide['content'].replace('\n', '<br>')}
                </div>
                <div class="slide-number">Slide {i+1}</div>
            </section>
            """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trình chiếu 3D - {template_name}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/theme/black.css">
        <style>
            .reveal {{
                perspective: 1000px;
            }}
            
            .slide-3d {{
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px !important;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transform-style: preserve-3d;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            }}
            
            .slide-title-container {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100%;
                transform: translateZ(50px);
            }}
            
            .content-box-3d {{
                background: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 30px;
                margin-top: 30px;
                font-size: 1.8rem;
                transform: translateZ(30px);
                text-align: left;
            }}
            
            .presenter-info {{
                position: absolute;
                bottom: 20px;
                right: 20px;
                font-size: 1.2rem;
                opacity: 0.7;
            }}
            
            .slide-number {{
                position: absolute;
                bottom: 20px;
                left: 20px;
                font-size: 1.2rem;
                opacity: 0.7;
            }}
            
            body {{
                font-family: {template['font']};
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
                parallaxBackgroundImage: '',
                parallaxBackgroundSize: '',
                mouseWheel: true,
                slideNumber: true,
                width: "90%",
                height: "90%",
                margin: 0.04,
                minScale: 0.2,
                maxScale: 2.0
            }});
            
            // Hiệu ứng 3D cho slide
            document.querySelectorAll('.slide-3d').forEach(slide => {{
                slide.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateZ(100px)';
                }});
                
                slide.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateZ(0px)';
                }});
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
        <p style="margin: 5px 0;"><strong>Màu chính:</strong> {template_info['primary_color']}</p>
        <p style="margin: 5px 0;"><strong>Phong cách:</strong> {template_info['style']}</p>
        <p style="margin: 5px 0;"><strong>Font chữ:</strong> {template_info['font'].split(',')[0]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<p style='color: white;'>{template_info['description']}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tùy chọn hiệu ứng
    st.markdown('<div class="section-header">🎭 Hiệu Ứng 3D</div>', unsafe_allow_html=True)
    
    animation_intensity = st.slider("Cường độ hiệu ứng 3D", 1, 10, 5)
    shadow_intensity = st.slider("Cường độ bóng đổ", 1, 10, 7)
    
    # Tùy chọn nội dung
    st.markdown('<div class="section-header">📝 Loại Slide</div>', unsafe_allow_html=True)
    slide_type = st.radio("Chọn loại slide", ["Slide Tiêu Đề", "Slide Nội Dung"], index=0)
    
    st.markdown("---")
    
    # Thông tin ứng dụng
    st.markdown("""
    <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 20px;">
        <p><strong>Trình Tạo Slide 3D Chuyên Nghiệp</strong></p>
        <p>Tạo bài thuyết trình ấn tượng với hiệu ứng 3D và mẫu chuyên nghiệp.</p>
        <p>Hỗ trợ xuất file HTML để trình chiếu trên mọi thiết bị.</p>
    </div>
    """, unsafe_allow_html=True)

# Tab chính
tab1, tab2, tab3 = st.tabs(["📝 Nhập Nội Dung", "👁️ Xem Trước", "💾 Xuất Slide"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">📋 Nhập Nội Dung Slide</div>', unsafe_allow_html=True)
        
        slide_title = st.text_input("Tiêu đề slide", "Xu Hướng Công Nghệ 2024")
        
        if slide_type == "Slide Tiêu Đề":
            slide_content = st.text_area(
                "Nội dung slide (phụ đề)",
                "Khám phá những công nghệ đột phá sẽ định hình tương lai kỹ thuật số",
                height=150
            )
        else:
            slide_content = st.text_area(
                "Nội dung slide",
                """• Trí tuệ nhân tạo Generative AI phát triển mạnh mẽ
• Công nghệ Metaverse và Web3 tiếp tục mở rộng
• Tính toán lượng tử đạt được những bước tiến quan trọng
• IoT kết nối vạn vật thông minh hơn
• An ninh mạng trở thành ưu tiên hàng đầu
• Phát triển bền vững với công nghệ xanh
• Tự động hóa và robot thay đổi ngành sản xuất""",
                height=250
            )
        
        # Nút tạo slide
        if st.button("🎬 Tạo Slide Trình Chiếu", use_container_width=True):
            st.session_state.slide_created = True
            st.session_state.slide_title = slide_title
            st.session_state.slide_content = slide_content
            st.session_state.slide_type = slide_type
            st.success("Slide đã được tạo thành công! Chuyển sang tab 'Xem Trước' để xem kết quả.")
    
    with col2:
        st.markdown('<div class="section-header">📊 Mẫu Slide Nhanh</div>', unsafe_allow_html=True)
        
        # Các mẫu nội dung nhanh
        quick_templates = {
            "Báo Cáo Doanh Thu": {
                "title": "Báo Cáo Doanh Thu Q4 2023",
                "content": "Tăng trưởng ấn tượng 25% so với cùng kỳ năm trước"
            },
            "Chiến Lược Marketing": {
                "title": "Chiến Lược Marketing 2024",
                "content": "Tập trung vào digital transformation và personalization"
            },
            "Giới Thiệu Sản Phẩm Mới": {
                "title": "Sản Phẩm AlphaX Pro",
                "content": "Công nghệ đột phá với hiệu suất vượt trội 40%"
            }
        }
        
        for template_name, template_data in quick_templates.items():
            with st.container():
                st.markdown(f"""
                <div class="template-card">
                    <h4 style="color: white; margin-top: 0;">{template_name}</h4>
                    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{template_data['title']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Sử dụng mẫu {template_name}", key=template_name):
                    st.session_state.slide_title = template_data['title']
                    st.session_state.slide_content = template_data['content']
                    st.experimental_rerun()

with tab2:
    if 'slide_created' not in st.session_state:
        st.info("Vui lòng nhập nội dung slide và nhấn 'Tạo Slide Trình Chiếu' ở tab 'Nhập Nội Dung'.")
    else:
        st.markdown('<div class="section-header">👁️ Xem Trước Slide 3D</div>', unsafe_allow_html=True)
        
        # Xác định loại slide
        slide_type_code = "title" if st.session_state.slide_type == "Slide Tiêu Đề" else "content"
        
        # Tạo HTML cho slide
        slide_html = generate_slide_html(
            st.session_state.slide_title,
            st.session_state.slide_content,
            selected_template,
            slide_type_code
        )
        
        # Hiển thị slide trong iframe
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.markdown(f"""
            <div class="slide-preview-3d">
                <iframe srcdoc='{slide_html}' width="100%" height="600" style="border: none; border-radius: 10px;"></iframe>
            </div>
            """, unsafe_allow_html=True)
            
            # Thông tin slide
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h4 style="color: white; margin-top: 0;">Thông tin Slide</h4>
                <p style="color: rgba(255,255,255,0.9);"><strong>Tiêu đề:</strong> {st.session_state.slide_title}</p>
                <p style="color: rgba(255,255,255,0.9);"><strong>Mẫu:</strong> {selected_template}</p>
                <p style="color: rgba(255,255,255,0.9);"><strong>Loại slide:</strong> {st.session_state.slide_type}</p>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">💾 Xuất Slide Trình Chiếu</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: white; margin-top: 0;">Xuất Slide Đơn</h4>
            <p style="color: rgba(255,255,255,0.9);">Tải về slide hiện tại dưới dạng file HTML có thể chạy độc lập.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tạo slide đơn để xuất
        if 'slide_created' in st.session_state:
            slide_type_code = "title" if st.session_state.slide_type == "Slide Tiêu Đề" else "content"
            slide_html = generate_slide_html(
                st.session_state.slide_title,
                st.session_state.slide_content,
                selected_template,
                slide_type_code
            )
            
            # Chuyển HTML thành base64 để tải về
            b64 = base64.b64encode(slide_html.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="slide_3d.html" style="text-decoration: none;">'
            
            st.markdown(f"""
            <div style="text-align: center;">
                {href}
                    <button style="background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%); color: white; border: none; padding: 15px 30px; border-radius: 30px; font-weight: 600; font-size: 1rem; cursor: pointer; width: 100%;">
                        📥 Tải Slide Đơn (HTML)
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: white; margin-top: 0;">Tạo Trình Chiếu Đầy Đủ</h4>
            <p style="color: rgba(255,255,255,0.9);">Tạo bài thuyết trình đầy đủ với nhiều slide và hiệu ứng chuyển tiếp.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Thêm các slide khác
        st.markdown("##### Thêm slide vào trình chiếu")
        
        if 'slides' not in st.session_state:
            st.session_state.slides = []
        
        new_slide_title = st.text_input("Tiêu đề slide mới", key="new_slide_title")
        new_slide_content = st.text_area("Nội dung slide mới", key="new_slide_content", height=100)
        
        col_add1, col_add2 = st.columns(2)
        with col_add1:
            if st.button("➕ Thêm Slide", use_container_width=True):
                if new_slide_title and new_slide_content:
                    st.session_state.slides.append({
                        'title': new_slide_title,
                        'content': new_slide_content
                    })
                    st.success(f"Đã thêm slide: {new_slide_title}")
                else:
                    st.warning("Vui lòng nhập tiêu đề và nội dung cho slide")
        
        with col_add2:
            if st.button("🗑️ Xóa Tất cả Slide", use_container_width=True):
                st.session_state.slides = []
                st.success("Đã xóa tất cả slide")
        
        # Hiển thị danh sách slide
        if st.session_state.slides:
            st.markdown("##### Danh sách slide trong trình chiếu")
            for i, slide in enumerate(st.session_state.slides):
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; margin-bottom: 5px;">
                    <strong>Slide {i+1}:</strong> {slide['title']}
                </div>
                """, unsafe_allow_html=True)
            
            # Tạo trình chiếu đầy đủ
            all_slides = [{'title': st.session_state.slide_title, 'content': st.session_state.slide_content}] + st.session_state.slides
            presentation_html = generate_presentation_html(all_slides, selected_template)
            
            # Chuyển HTML thành base64 để tải về
            b64_presentation = base64.b64encode(presentation_html.encode()).decode()
            href_presentation = f'<a href="data:text/html;base64,{b64_presentation}" download="trinh_chieu_3d.html" style="text-decoration: none;">'
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 20px;">
                {href_presentation}
                    <button style="background: linear-gradient(45deg, #FF416C 0%, #FF4B2B 100%); color: white; border: none; padding: 15px 30px; border-radius: 30px; font-weight: 600; font-size: 1rem; cursor: pointer; width: 100%;">
                        🎬 Tải Trình Chiếu Đầy Đủ (HTML)
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        # Hướng dẫn sử dụng
        st.markdown("---")
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 20px;">
            <h4 style="color: white; margin-top: 0;">📖 Hướng dẫn sử dụng</h4>
            <ol style="color: rgba(255,255,255,0.9);">
                <li>Chọn mẫu slide ở sidebar</li>
                <li>Nhập nội dung slide ở tab "Nhập Nội Dung"</li>
                <li>Xem trước slide ở tab "Xem Trước"</li>
                <li>Thêm nhiều slide để tạo trình chiếu đầy đủ</li>
                <li>Tải về file HTML để trình chiếu trên mọi thiết bị</li>
            </ol>
            <p style="color: rgba(255,255,255,0.9);"><strong>Mẹo:</strong> File HTML tải về có thể chạy trực tiếp trên trình duyệt, không cần kết nối Internet.</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px;">
    <p>Trình Tạo Slide 3D Chuyên Nghiệp • Sử dụng Reveal.js và Streamlit • © 2024</p>
    <p>Ứng dụng hỗ trợ tạo bài thuyết trình 3D chuyên nghiệp với hiệu ứng hình ảnh sống động</p>
</div>
""", unsafe_allow_html=True)
