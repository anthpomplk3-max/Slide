import streamlit as st
import base64
from PIL import Image
import io
import json

# Cấu hình trang
st.set_page_config(
    page_title="Trình Tạo Slide 3D Nâng Cao - Điện & ATLĐ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    /* Nền gradient chuyên nghiệp */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    /* Tiêu đề chính */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        background: linear-gradient(90deg, #00c9ff 0%, #92fe9d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Phụ đề */
    .sub-title {
        text-align: center;
        color: #b0bec5;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Card mẫu slide */
    .template-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
    }
    
    .template-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(100, 255, 218, 0.5);
        background: rgba(255, 255, 255, 0.12);
    }
    
    /* Nút tùy chỉnh */
    .stButton > button {
        background: linear-gradient(45deg, #00c9ff 0%, #92fe9d 100%);
        color: #0f2027;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 201, 255, 0.4);
    }
    
    /* Tiêu đề section */
    .section-header {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #00c9ff;
        padding-left: 15px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Hiệu ứng 3D cho preview */
    .slide-preview-3d {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Badge cho template */
    .template-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        background: rgba(0, 201, 255, 0.2);
        color: #64ffda;
        border: 1px solid rgba(100, 255, 218, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #b0bec5;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-right: 5px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, rgba(0, 201, 255, 0.2), rgba(146, 254, 157, 0.2)) !important;
        color: white !important;
        border-color: rgba(0, 201, 255, 0.5) !important;
    }
    
    /* Preview container */
    .preview-container {
        background: rgba(15, 32, 39, 0.6);
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px dashed rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00c9ff 0%, #92fe9d 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Tiêu đề ứng dụng
st.markdown('<h1 class="main-title">⚡ Trình Tạo Slide 3D Nâng Cao - Điện & ATLĐ</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tạo bài thuyết trình chuyên nghiệp với logo tùy chỉnh, hình ảnh và hiệu ứng 3D đa dạng</p>', unsafe_allow_html=True)

# Khởi tạo session state
if 'slide_data' not in st.session_state:
    st.session_state.slide_data = {
        'title': 'An Toàn Điện Trong Trạm Biến Áp',
        'content': 'Nguyên tắc và quy trình an toàn khi làm việc với thiết bị điện cao áp',
        'template': 'Điện Lực 3D',
        'effect_type': 'floating',
        'logo_position': 'top-left',
        'logo_base64': None,
        'images': []
    }

# Các kiểu hiệu ứng 3D
EFFECTS_3D = {
    "floating": {
        "name": "Nổi 3D",
        "description": "Hiệu ứng nổi với chuyển động nhẹ",
        "css_class": "effect-floating"
    },
    "perspective": {
        "name": "Phối cảnh sâu",
        "description": "Hiệu ứng phối cảnh 3D mạnh",
        "css_class": "effect-perspective"
    },
    "rotate": {
        "name": "Xoay 3D",
        "description": "Hiệu ứng xoay không gian 3D",
        "css_class": "effect-rotate"
    },
    "cuboid": {
        "name": "Khối lập phương",
        "description": "Slide như một khối 3D",
        "css_class": "effect-cuboid"
    },
    "parallax": {
        "name": "Parallax 3D",
        "description": "Hiệu ứng parallax đa lớp",
        "css_class": "effect-parallax"
    },
    "neon": {
        "name": "Neon 3D",
        "description": "Hiệu ứng neon với ánh sáng 3D",
        "css_class": "effect-neon"
    }
}

# Các mẫu slide chuyên ngành
TEMPLATES = {
    "Điện Lực 3D": {
        "primary_color": "#0f2027",
        "secondary_color": "#203a43",
        "accent_color": "#00c9ff",
        "highlight_color": "#92fe9d",
        "font": "'Segoe UI', 'Roboto', sans-serif",
        "description": "Mẫu 3D chuyên nghiệp cho ngành điện lực",
        "tags": ["Điện", "3D", "Chuyên nghiệp"],
        "icon": "⚡"
    },
    "Trạm Biến Áp 3D": {
        "primary_color": "#1a1a2e",
        "secondary_color": "#16213e",
        "accent_color": "#0fcecb",
        "highlight_color": "#ffd166",
        "font": "'Roboto Mono', monospace",
        "description": "Mẫu kỹ thuật 3D cho trạm biến áp",
        "tags": ["Trạm Biến Áp", "Kỹ Thuật", "3D"],
        "icon": "🏭"
    },
    "HSE An Toàn": {
        "primary_color": "#1b4332",
        "secondary_color": "#2d6a4f",
        "accent_color": "#52b788",
        "highlight_color": "#ff9e00",
        "font": "'Montserrat', sans-serif",
        "description": "Mẫu 3D cho an toàn và sức khỏe",
        "tags": ["HSE", "An Toàn", "3D"],
        "icon": "🛡️"
    },
    "ATVSLĐ Cảnh Báo 3D": {
        "primary_color": "#660708",
        "secondary_color": "#a4161a",
        "accent_color": "#e5383b",
        "highlight_color": "#ffd60a",
        "font": "'Impact', 'Arial Black', sans-serif",
        "description": "Mẫu cảnh báo 3D nổi bật",
        "tags": ["ATVSLĐ", "Cảnh Báo", "3D"],
        "icon": "⚠️"
    }
}

# Hàm chuyển ảnh thành base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Hàm tạo CSS cho hiệu ứng 3D
def get_3d_effect_css(effect_type):
    effects = {
        "floating": """
            transform-style: preserve-3d;
            transform: translateZ(0);
            animation: float3d 6s ease-in-out infinite;
            
            @keyframes float3d {
                0%, 100% { transform: translateZ(0) rotateX(5deg) rotateY(-5deg); }
                50% { transform: translateZ(20px) rotateX(3deg) rotateY(-7deg); }
            }
        """,
        "perspective": """
            transform-style: preserve-3d;
            perspective: 1500px;
            transform: rotateX(15deg) rotateY(-10deg) translateZ(50px);
            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            
            &:hover {
                transform: rotateX(10deg) rotateY(-5deg) translateZ(100px);
            }
        """,
        "rotate": """
            transform-style: preserve-3d;
            animation: rotate3d 20s infinite linear;
            
            @keyframes rotate3d {
                0% { transform: rotateY(0deg) rotateX(5deg); }
                100% { transform: rotateY(360deg) rotateX(5deg); }
            }
        """,
        "cuboid": """
            transform-style: preserve-3d;
            transform: rotateX(20deg) rotateY(-20deg);
            box-shadow: 
                20px 20px 40px rgba(0,0,0,0.3),
                inset 0 0 50px rgba(255,255,255,0.1);
            
            &:before, &:after {
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                background: inherit;
                transform-origin: center;
            }
            
            &:before {
                transform: translateZ(-50px);
                opacity: 0.7;
            }
            
            &:after {
                transform: translateZ(-100px);
                opacity: 0.4;
            }
        """,
        "parallax": """
            transform-style: preserve-3d;
            
            & > * {
                transform-style: preserve-3d;
            }
            
            .layer1 { transform: translateZ(0); }
            .layer2 { transform: translateZ(50px); }
            .layer3 { transform: translateZ(100px); }
            .layer4 { transform: translateZ(150px); }
        """,
        "neon": """
            transform-style: preserve-3d;
            transform: translateZ(0);
            box-shadow: 
                0 0 20px var(--accent),
                0 0 40px var(--accent),
                inset 0 0 20px rgba(255,255,255,0.1);
            animation: neon-pulse 2s infinite alternate;
            
            @keyframes neon-pulse {
                from { box-shadow: 0 0 20px var(--accent), 0 0 40px var(--accent); }
                to { box-shadow: 0 0 30px var(--accent), 0 0 60px var(--accent); }
            }
        """
    }
    return effects.get(effect_type, effects["floating"])

# Hàm tạo CSS cho vị trí logo
def get_logo_position_css(position):
    positions = {
        "top-left": "top: 30px; left: 30px;",
        "top-right": "top: 30px; right: 30px;",
        "bottom-left": "bottom: 30px; left: 30px;",
        "bottom-right": "bottom: 30px; right: 30px;",
        "center-top": "top: 30px; left: 50%; transform: translateX(-50%);",
        "center-bottom": "bottom: 30px; left: 50%; transform: translateX(-50%);"
    }
    return positions.get(position, "top: 30px; left: 30px;")

# Hàm tạo HTML cho slide với đầy đủ tính năng
def generate_slide_html(title, content, template_name, effect_type, logo_base64, logo_position, images):
    template = TEMPLATES[template_name]
    effect_css = get_3d_effect_css(effect_type)
    logo_css = get_logo_position_css(logo_position)
    
    # Tạo HTML cho logo nếu có
    logo_html = ""
    if logo_base64:
        logo_html = f"""
        <div class="slide-logo" style="{logo_css}">
            <img src="data:image/png;base64,{logo_base64}" 
                 style="max-height: 80px; max-width: 200px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));">
        </div>
        """
    
    # Tạo HTML cho hình ảnh
    images_html = ""
    if images:
        images_html = '<div class="image-gallery">'
        for i, img_base64 in enumerate(images[:3]):  # Giới hạn 3 ảnh
            images_html += f"""
            <div class="image-item" style="transform: translateZ({30 * (i+1)}px);">
                <img src="data:image/png;base64,{img_base64}" 
                     style="max-width: 100%; border-radius: 10px; box-shadow: 0 10px 20px rgba(0,0,0,0.3);">
            </div>
            """
        images_html += '</div>'
    
    html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&family=Montserrat:wght@400;700;900&family=Roboto+Mono:wght@400;700&display=swap');
            
            :root {{
                --primary: {template['primary_color']};
                --secondary: {template['secondary_color']};
                --accent: {template['accent_color']};
                --highlight: {template['highlight_color']};
            }}
            
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
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                overflow: hidden;
                perspective: 1000px;
            }}
            
            .slide-3d-container {{
                width: 90%;
                max-width: 1200px;
                height: 80vh;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                position: relative;
                overflow: hidden;
                {effect_css}
            }}
            
            .slide-header {{
                background: linear-gradient(90deg, var(--accent), var(--highlight));
                color: white;
                padding: 40px;
                border-radius: 20px 20px 0 0;
                position: relative;
                transform-style: preserve-3d;
            }}
            
            .slide-title {{
                font-size: 3.5rem;
                font-weight: 900;
                margin-bottom: 15px;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                transform: translateZ(50px);
                background: linear-gradient(90deg, white, #f0f0f0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .slide-subtitle {{
                font-size: 1.6rem;
                opacity: 0.9;
                font-weight: 300;
                transform: translateZ(30px);
                color: rgba(255,255,255,0.9);
            }}
            
            .slide-content {{
                padding: 40px;
                color: #333;
                transform-style: preserve-3d;
                position: relative;
                z-index: 2;
            }}
            
            .content-main {{
                font-size: 2rem;
                line-height: 1.6;
                margin-bottom: 30px;
                transform: translateZ(40px);
                color: var(--primary);
                font-weight: 700;
            }}
            
            .content-bullets {{
                font-size: 1.6rem;
                line-height: 1.8;
                margin-left: 25px;
                transform: translateZ(30px);
            }}
            
            .content-bullets li {{
                margin-bottom: 20px;
                position: relative;
                padding-left: 15px;
                color: #444;
            }}
            
            .content-bullets li:before {{
                content: "{template['icon']}";
                position: absolute;
                left: -30px;
                color: var(--accent);
                font-size: 1.2rem;
            }}
            
            .slide-logo {{
                position: absolute;
                z-index: 100;
                filter: drop-shadow(0 5px 15px rgba(0,0,0,0.3));
            }}
            
            .image-gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 40px 0;
                transform-style: preserve-3d;
            }}
            
            .image-item {{
                transition: transform 0.3s ease;
                border-radius: 10px;
                overflow: hidden;
            }}
            
            .image-item:hover {{
                transform: translateZ(50px) scale(1.05);
            }}
            
            .slide-footer {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(0, 0, 0, 0.8);
                padding: 20px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 3px solid var(--accent);
                transform: translateZ(20px);
            }}
            
            .template-name {{
                font-weight: 700;
                color: var(--accent);
                font-size: 1.3rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .slide-number {{
                font-size: 1.2rem;
                color: #aaa;
            }}
            
            .effect-badge {{
                background: var(--accent);
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 600;
            }}
            
            .decoration-1 {{
                position: absolute;
                width: 300px;
                height: 300px;
                background: var(--accent);
                opacity: 0.1;
                border-radius: 50%;
                top: -150px;
                right: -150px;
                transform: translateZ(-100px);
            }}
            
            .decoration-2 {{
                position: absolute;
                width: 200px;
                height: 200px;
                background: var(--highlight);
                opacity: 0.1;
                border-radius: 50%;
                bottom: -100px;
                left: -100px;
                transform: translateZ(-50px);
            }}
            
            .warning-box {{
                background: linear-gradient(135deg, rgba(255, 235, 59, 0.2), rgba(255, 193, 7, 0.2));
                border-left: 5px solid #ffc107;
                padding: 25px;
                margin: 30px 0;
                border-radius: 0 15px 15px 0;
                transform: translateZ(25px);
                box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
            }}
            
            @media (max-width: 768px) {{
                .slide-title {{
                    font-size: 2.5rem;
                }}
                
                .content-main {{
                    font-size: 1.6rem;
                }}
                
                .content-bullets {{
                    font-size: 1.3rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="slide-3d-container">
            <div class="decoration-1"></div>
            <div class="decoration-2"></div>
            
            {logo_html}
            
            <div class="slide-header">
                <h1 class="slide-title">{title}</h1>
                <div class="slide-subtitle">Trình bày chuyên đề - Hiệu ứng: {EFFECTS_3D[effect_type]['name']}</div>
            </div>
            
            <div class="slide-content">
                <div class="content-main">
                    {content if '\\n' not in content else content.split('\\n')[0]}
                </div>
                
                {"<ul class='content-bullets'>" + ''.join([f'<li>{line.strip()}</li>' for line in content.split('\\n')[1:] if line.strip()]) + "</ul>" if '\\n' in content else ""}
                
                {images_html}
                
                <div class="warning-box">
                    <strong>⚠️ Lưu ý an toàn:</strong> Tuân thủ nghiêm ngặt quy trình 5S và các quy định ATVSLĐ khi làm việc với thiết bị điện cao áp.
                </div>
            </div>
            
            <div class="slide-footer">
                <div class="template-name">
                    {template['icon']} {template_name} | <span class="effect-badge">{EFFECTS_3D[effect_type]['name']}</span>
                </div>
                <div class="slide-number">Slide 3D Chuyên Ngành Điện & ATLĐ</div>
            </div>
        </div>
        
        <script>
            // Hiệu ứng 3D tương tác
            const slide = document.querySelector('.slide-3d-container');
            const body = document.body;
            
            body.addEventListener('mousemove', (e) => {{
                const {{ clientX: x, clientY: y }} = e;
                const centerX = window.innerWidth / 2;
                const centerY = window.innerHeight / 2;
                
                const rotateY = (x - centerX) / 50;
                const rotateX = (centerY - y) / 50;
                
                slide.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
            }});
            
            body.addEventListener('mouseleave', () => {{
                slide.style.transform = 'rotateX(0) rotateY(0)';
            }});
        </script>
    </body>
    </html>
    """
    
    return html

# Sidebar với các tùy chọn
with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Cài Đặt Chính</div>', unsafe_allow_html=True)
    
    # Chọn mẫu
    selected_template = st.selectbox(
        "Chọn mẫu trình chiếu",
        list(TEMPLATES.keys()),
        index=0
    )
    
    # Chọn hiệu ứng 3D
    selected_effect = st.selectbox(
        "Chọn hiệu ứng 3D",
        list(EFFECTS_3D.keys()),
        format_func=lambda x: EFFECTS_3D[x]['name'],
        index=0
    )
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin: 10px 0;">
        <p style="color: #b0bec5; font-size: 0.9rem; margin: 0;">{EFFECTS_3D[selected_effect]['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload logo
    st.markdown('<div class="section-header">🏷️ Logo & Nhận Diện</div>', unsafe_allow_html=True)
    
    logo_file = st.file_uploader("Upload logo của bạn", type=['png', 'jpg', 'jpeg'], key="logo_upload")
    
    if logo_file:
        image = Image.open(logo_file)
        st.image(image, caption="Logo đã upload", width=150)
        st.session_state.logo_base64 = image_to_base64(image)
    elif 'logo_base64' not in st.session_state:
        st.session_state.logo_base64 = None
    
    # Vị trí logo
    if st.session_state.logo_base64:
        logo_position = st.selectbox(
            "Vị trí logo trên slide",
            ["top-left", "top-right", "bottom-left", "bottom-right", "center-top", "center-bottom"],
            format_func=lambda x: {
                "top-left": "Trên - Trái",
                "top-right": "Trên - Phải",
                "bottom-left": "Dưới - Trái",
                "bottom-right": "Dưới - Phải",
                "center-top": "Giữa - Trên",
                "center-bottom": "Giữa - Dưới"
            }[x],
            index=0
        )
    else:
        logo_position = "top-left"
    
    st.markdown("---")
    
    # Upload hình ảnh
    st.markdown('<div class="section-header">🖼️ Hình Ảnh Bổ Sung</div>', unsafe_allow_html=True)
    
    uploaded_images = st.file_uploader(
        "Upload hình ảnh cho slide (tối đa 3 ảnh)",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="image_upload"
    )
    
    if uploaded_images:
        st.session_state.images = []
        for i, img_file in enumerate(uploaded_images[:3]):  # Giới hạn 3 ảnh
            image = Image.open(img_file)
            st.image(image, caption=f"Hình {i+1}", width=100)
            st.session_state.images.append(image_to_base64(image))
    elif 'images' not in st.session_state:
        st.session_state.images = []
    
    st.markdown("---")
    
    # Tùy chỉnh nâng cao
    with st.expander("🎛️ Tùy Chỉnh Nâng Cao"):
        animation_speed = st.slider("Tốc độ hiệu ứng", 0.5, 3.0, 1.0, 0.1)
        shadow_intensity = st.slider("Cường độ bóng đổ", 0, 100, 50)
        glow_intensity = st.slider("Cường độ ánh sáng", 0, 100, 30)
        
        if st.button("🔄 Đặt lại cài đặt mặc định"):
            st.session_state.animation_speed = 1.0
            st.session_state.shadow_intensity = 50
            st.session_state.glow_intensity = 30
    
    st.markdown("---")
    
    # Thông tin ứng dụng
    st.markdown("""
    <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 20px;">
        <p><strong>🔄 Cập nhật tính năng:</strong></p>
        <ul style="padding-left: 20px;">
            <li>6 hiệu ứng 3D khác nhau</li>
            <li>Logo tùy chỉnh vị trí</li>
            <li>Chèn nhiều hình ảnh</li>
            <li>Hiệu ứng tương tác với chuột</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Tab chính
tab1, tab2, tab3 = st.tabs(["📝 Nhập Nội Dung", "👁️ Xem Trước 3D", "💾 Xuất File"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">📋 Nhập Nội Dung Slide</div>', unsafe_allow_html=True)
        
        # Nhập tiêu đề
        slide_title = st.text_input(
            "Tiêu đề slide",
            value=st.session_state.slide_data.get('title', 'An Toàn Điện Trong Trạm Biến Áp'),
            key="input_title",
            placeholder="Nhập tiêu đề slide..."
        )
        
        # Nhập nội dung
        slide_content = st.text_area(
            "Nội dung slide (mỗi dòng là một gạch đầu dòng)",
            value=st.session_state.slide_data.get('content', 'Nguyên tắc và quy trình an toàn khi làm việc với thiết bị điện cao áp'),
            height=250,
            key="input_content",
            help="Dòng đầu tiên là nội dung chính, các dòng sau là các gạch đầu dòng.",
            placeholder="""Nội dung chính...
• Gạch đầu dòng 1
• Gạch đầu dòng 2
• Gạch đầu dòng 3"""
        )
        
        # Nút cập nhật
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎬 Cập nhật & Xem trước", type="primary", use_container_width=True):
                st.session_state.slide_data.update({
                    'title': slide_title,
                    'content': slide_content,
                    'template': selected_template,
                    'effect_type': selected_effect,
                    'logo_position': logo_position if 'logo_base64' in st.session_state and st.session_state.logo_base64 else "top-left",
                    'logo_base64': st.session_state.get('logo_base64'),
                    'images': st.session_state.get('images', [])
                })
                st.success("✅ Đã cập nhật slide với hiệu ứng 3D!")
        
        with col_btn2:
            if st.button("🗑️ Xóa tất cả nội dung", use_container_width=True):
                st.session_state.slide_data['title'] = ""
                st.session_state.slide_data['content'] = ""
                st.rerun()
    
    with col2:
        st.markdown('<div class="section-header">📊 Mẫu Nội Dung Nhanh</div>', unsafe_allow_html=True)
        
        quick_templates = {
            "Quy Trình An Toàn Điện": {
                "title": "Quy Trình 5 Bước An Toàn Điện",
                "content": """Thực hiện quy trình cô lập nguồn điện
• Bước 1: Ngắt toàn bộ nguồn điện chính
• Bước 2: Khóa và treo biển cảnh báo
• Bước 3: Kiểm tra không còn điện
• Bước 4: Nối đất và ngắn mạch
• Bước 5: Bố trí rào chắn cảnh báo"""
            },
            "Bảo Trì Trạm Biến Áp": {
                "title": "Quy Trình Bảo Trì Định Kỳ",
                "content": """Bảo trì hệ thống trạm biến áp 110kV
• Kiểm tra máy biến áp và hệ thống làm mát
• Vệ sinh sứ cách điện và thanh cái
• Đo đạc thông số nhiệt độ, độ rung
• Kiểm tra hệ thống bảo vệ và relay
• Bảo dưỡng hệ thống chống sét
• Ghi chép nhật ký vận hành"""
            },
            "Huấn Luyện ATVSLĐ": {
                "title": "Đào Tạo An Toàn Lao Động",
                "content": """Chương trình đào tạo ATVSLĐ toàn diện
• Nhận diện các mối nguy hiểm
• Sử dụng thiết bị bảo hộ cá nhân
• Kỹ thuật sơ cứu điện giật
• Quy trình ứng phó sự cố
• Thực hành tại hiện trường
• Đánh giá và cấp chứng chỉ"""
            }
        }
        
        for template_name, template_data in quick_templates.items():
            with st.container():
                st.markdown(f"""
                <div class="template-card" onclick="this.style.transform='scale(0.98)'; setTimeout(()=>this.style.transform='', 200)">
                    <h4 style="color: #64ffda; margin-top: 0;">{template_name}</h4>
                    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{template_data['title']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Sử dụng mẫu này", key=f"btn_{template_name}", use_container_width=True):
                    st.session_state.slide_data['title'] = template_data['title']
                    st.session_state.slide_data['content'] = template_data['content']
                    st.rerun()

with tab2:
    st.markdown('<div class="section-header">👁️ Xem Trước Slide 3D</div>', unsafe_allow_html=True)
    
    # Thông tin slide
    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
    with col_info1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Tiêu đề", st.session_state.slide_data.get('title', '')[:20] + "..." if len(st.session_state.slide_data.get('title', '')) > 20 else st.session_state.slide_data.get('title', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_info2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Hiệu ứng 3D", EFFECTS_3D[st.session_state.slide_data.get('effect_type', 'floating')]['name'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_info3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Mẫu thiết kế", st.session_state.slide_data.get('template', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_info4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        has_logo = "Có" if st.session_state.slide_data.get('logo_base64') else "Không"
        st.metric("Logo", has_logo)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Xem trước slide
    st.markdown('<div class="preview-container">', unsafe_allow_html=True)
    
    if st.session_state.slide_data.get('title'):
        slide_html = generate_slide_html(
            st.session_state.slide_data['title'],
            st.session_state.slide_data['content'],
            st.session_state.slide_data['template'],
            st.session_state.slide_data['effect_type'],
            st.session_state.slide_data.get('logo_base64'),
            st.session_state.slide_data.get('logo_position', 'top-left'),
            st.session_state.slide_data.get('images', [])
        )
        
        # Hiển thị slide với hiệu ứng 3D
        st.components.v1.html(slide_html, height=700, scrolling=False)
        
        # Hướng dẫn tương tác
        st.markdown("""
        <div style="background: rgba(0,201,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px solid rgba(0,201,255,0.3);">
            <h4 style="color: #64ffda; margin-top: 0;">🎮 Hướng dẫn tương tác 3D:</h4>
            <ul style="color: rgba(255,255,255,0.9);">
                <li><strong>Di chuột</strong> trên slide để xem hiệu ứng 3D tương tác</li>
                <li><strong>Di chuột ra ngoài</strong> để trở về trạng thái ban đầu</li>
                <li>Các hình ảnh có hiệu ứng <strong>nổi 3D</strong> khi hover</li>
                <li>Logo và các phần tử có hiệu ứng <strong>đổ bóng 3D</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Vui lòng nhập nội dung slide ở tab 'Nhập Nội Dung'")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">💾 Xuất Slide Trình Chiếu</div>', unsafe_allow_html=True)
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.08); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(0,201,255,0.2);">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 2rem; margin-right: 15px;">📥</div>
                <div>
                    <h4 style="color: white; margin: 0;">Xuất Slide Đơn 3D</h4>
                    <p style="color: #b0bec5; font-size: 0.95rem; margin: 5px 0 0 0;">Tải về slide hiện tại với đầy đủ hiệu ứng 3D</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.slide_data.get('title'):
            # Tạo slide đơn
            slide_html = generate_slide_html(
                st.session_state.slide_data['title'],
                st.session_state.slide_data['content'],
                st.session_state.slide_data['template'],
                st.session_state.slide_data['effect_type'],
                st.session_state.slide_data.get('logo_base64'),
                st.session_state.slide_data.get('logo_position', 'top-left'),
                st.session_state.slide_data.get('images', [])
            )
            
            # Tạo file download
            b64 = base64.b64encode(slide_html.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="slide_3d_nang_cao.html" style="text-decoration: none;">'
            
            st.markdown(f"""
            <div style="text-align: center;">
                {href}
                    <button style="background: linear-gradient(45deg, #00c9ff 0%, #92fe9d 100%); color: #0f2027; border: none; padding: 15px 30px; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; width: 100%; transition: all 0.3s ease;">
                        ⚡ Tải Slide 3D (HTML)
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            # Thông tin file
            file_size = len(slide_html) / 1024  # KB
            st.info(f"📦 Kích thước file: {file_size:.1f} KB | 📄 Định dạng: HTML 3D | 🎨 Hiệu ứng: {EFFECTS_3D[st.session_state.slide_data['effect_type']]['name']}")
    
    with col_export2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.08); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(146,254,157,0.2);">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 2rem; margin-right: 15px;">🎬</div>
                <div>
                    <h4 style="color: white; margin: 0;">Trình Chiếu Nhiều Slide</h4>
                    <p style="color: #b0bec5; font-size: 0.95rem; margin: 5px 0 0 0;">Tạo bài thuyết trình với nhiều slide 3D</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quản lý nhiều slide
        if 'all_slides' not in st.session_state:
            st.session_state.all_slides = []
        
        # Form thêm slide mới
        with st.form("add_slide_form"):
            col_form1, col_form2 = st.columns([2, 1])
            with col_form1:
                new_title = st.text_input("Tiêu đề slide mới", "Slide mới")
            with col_form2:
                new_effect = st.selectbox(
                    "Hiệu ứng",
                    list(EFFECTS_3D.keys()),
                    format_func=lambda x: EFFECTS_3D[x]['name'],
                    index=0,
                    key="new_effect"
                )
            
            new_content = st.text_area("Nội dung slide mới", "Nội dung chi tiết...", height=100)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                add_submitted = st.form_submit_button("➕ Thêm vào trình chiếu", use_container_width=True)
            with col_btn2:
                clear_submitted = st.form_submit_button("🗑️ Xóa tất cả", use_container_width=True)
        
        if add_submitted and new_title:
            new_slide = {
                'title': new_title,
                'content': new_content,
                'template': selected_template,
                'effect_type': new_effect,
                'logo_base64': st.session_state.get('logo_base64'),
                'logo_position': logo_position if st.session_state.get('logo_base64') else "top-left"
            }
            st.session_state.all_slides.append(new_slide)
            st.success(f"✅ Đã thêm slide: {new_title}")
        
        if clear_submitted:
            st.session_state.all_slides = []
            st.success("🗑️ Đã xóa tất cả slide")
        
        # Hiển thị danh sách slide
        if st.session_state.all_slides:
            st.markdown("##### 📋 Danh sách slide trong trình chiếu")
            for i, slide in enumerate(st.session_state.all_slides):
                with st.expander(f"Slide {i+1}: {slide['title'][:30]}..." if len(slide['title']) > 30 else f"Slide {i+1}: {slide['title']}"):
                    col_slide1, col_slide2 = st.columns([3, 1])
                    with col_slide1:
                        st.write(f"**Nội dung:** {slide['content'][:100]}..." if len(slide['content']) > 100 else slide['content'])
                    with col_slide2:
                        st.write(f"**Hiệu ứng:** {EFFECTS_3D[slide['effect_type']]['name']}")
            
            # Tạo trình chiếu đầy đủ
            all_slides_for_presentation = [st.session_state.slide_data] + st.session_state.all_slides
            
            # Tạo file download
            if st.button("🎬 Tạo trình chiếu đầy đủ", type="primary", use_container_width=True):
                # Trong thực tế, cần tạo hàm generate_full_presentation_html
                # Ở đây sẽ tạo file zip chứa nhiều slide HTML
                st.success(f"✅ Đã tạo trình chiếu với {len(all_slides_for_presentation)} slide")
                
                # Tạo file HTML cho mỗi slide
                for i, slide in enumerate(all_slides_for_presentation):
                    slide_html = generate_slide_html(
                        slide['title'],
                        slide['content'],
                        slide['template'],
                        slide['effect_type'],
                        slide.get('logo_base64'),
                        slide.get('logo_position', 'top-left'),
                        []
                    )
                    
                    b64_slide = base64.b64encode(slide_html.encode()).decode()
                    href_slide = f'<a href="data:text/html;base64,{b64_slide}" download="slide_{i+1}_3d.html" style="text-decoration: none;">'
                    
                    st.markdown(f"""
                    <div style="margin: 10px 0;">
                        {href_slide}
                            <button style="background: rgba(146,254,157,0.2); color: #92fe9d; border: 1px solid rgba(146,254,157,0.5); padding: 8px 15px; border-radius: 5px; font-size: 0.9rem; cursor: pointer; width: 100%;">
                                📥 Tải Slide {i+1}: {slide['title'][:20]}...
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Hướng dẫn sử dụng
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin-top: 20px;">
        <h4 style="color: #64ffda; margin-top: 0;">📖 Hướng dẫn sử dụng file xuất:</h4>
        <ol style="color: rgba(255,255,255,0.9);">
            <li><strong>Tải file HTML</strong> về máy tính</li>
            <li><strong>Mở file</strong> bằng trình duyệt (Chrome, Firefox, Edge)</li>
            <li><strong>Di chuột</strong> để tương tác với hiệu ứng 3D</li>
            <li>Có thể <strong>trình chiếu trực tiếp</strong> từ file HTML</li>
            <li><strong>Không cần internet</strong> để hiển thị hiệu ứng 3D</li>
            <li>File hỗ trợ đầy đủ <strong>hiệu ứng CSS3 3D</strong></li>
        </ol>
        <div style="background: rgba(255, 100, 100, 0.1); padding: 10px; border-radius: 5px; margin-top: 10px; border-left: 3px solid #ff6464;">
            <strong>⚠️ Lưu ý:</strong> Một số hiệu ứng 3D nâng cao có thể không hoạt động trên trình duyệt cũ.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 20px;">
    <p><strong>Trình Tạo Slide 3D Nâng Cao - Chuyên Ngành Điện & An Toàn Lao Động</strong></p>
    <p style="font-size: 0.9rem;">© 2024 - Hỗ trợ: Kỹ thuật Điện | Trạm Biến Áp | ATVSLĐ | HSE | Hiệu ứng 3D nâng cao</p>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 10px; font-size: 0.8rem;">
        <span>⚡ 6 Hiệu ứng 3D</span>
        <span>🏷️ Logo tùy chỉnh</span>
        <span>🖼️ Chèn ảnh đa dạng</span>
        <span>🎮 Tương tác chuột</span>
    </div>
</div>
""", unsafe_allow_html=True)
