import streamlit as st
import matplotlib.pyplot as plt
import math
import numpy as np

def tan_main():
    """الدالة الرئيسية لتطبيق حاسبة الجملون"""
    
    # إعداد صفحة Streamlit
    st.set_page_config(page_title="حاسبة الجملون", page_icon="🏗️", layout="wide")

    # تحسين إعدادات matplotlib للأفضل وضوحاً
    plt.rcParams['figure.figsize'] = [12, 9]
    plt.rcParams['font.size'] = 12
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 14

    # العنوان الرئيسي
    st.title("🏗️ حاسبة الجملون - أنظمة متعددة")

    # إنشاء التبويبات
    tab1, tab2, tab3, tab4 = st.tabs(["📐 حساب الوتر", "🏗️ حساب الشتلة", "📏 حساب الزوايا", "📊 حساب الكمر"])

    # متغيرات لتخزين النتائج
    if 'hypotenuse' not in st.session_state:
        st.session_state.hypotenuse = 0
    if 'rafter' not in st.session_state:
        st.session_state.rafter = 0
    if 'angle' not in st.session_state:
        st.session_state.angle = 0
    if 'top_angle' not in st.session_state:
        st.session_state.top_angle = 0

    def create_clear_triangle_figure(base, height, helf, beem, angle, title, show_angles=True):
        """إنشاء رسم مثلث واضح ومفصل"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # ألوان واضحة ومتناسقة
        colors = {
            'base': '#2E8B57',      # أخضر للقاعدة
            'left': '#FF6B6B',      # أحمر للجانب الأيسر
            'right': '#4ECDC4',     # أزرق للجانب الأيمن
            'height': '#FFD166',    # أصفر للارتفاع
            'angle': '#6A0572',     # بنفسجي للزوايا
            'text': '#1A535C'       # أزرق داكن للنصوص
        }
        
        # رسم المثلث الرئيسي
        ax.plot([-helf, helf], [0, 0], color=colors['base'], linewidth=6, label=f'القاعدة: {base}m')
        ax.plot([-helf, 0], [0, height], color=colors['left'], linewidth=6, label=f'الوتر الأيسر: {beem:.3f}m')
        ax.plot([0, helf], [height, 0], color=colors['right'], linewidth=6, label=f'الوتر الأيمن: {beem:.3f}m')
        
        # خط الارتفاع العمودي
        ax.plot([0, 0], [0, height], '--', color=colors['height'], linewidth=3, alpha=0.7, label=f'الارتفاع: {height}m')
        
        # النقاط الرئيسية
        points = [(-helf, 0), (0, height), (helf, 0)]
        for i, (x, y) in enumerate(points):
            ax.plot(x, y, 'ko', markersize=12, markeredgecolor='white', markeredgewidth=2)
            ax.text(x, y - height*0.1, f'P{i+1}', fontsize=14, ha='center', 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
        
        # إضافة القياسات مع خلفيات واضحة
        # قياس القاعدة
        ax.annotate(f'{base}m', xy=(0, -height*0.15), xytext=(0, -height*0.25), 
                    textcoords='data', ha='center', fontsize=16, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['base'], alpha=0.8),
                    arrowprops=dict(arrowstyle="<->", color=colors['base'], lw=2))
        
        # قياس الارتفاع
        ax.annotate(f'{height}m', xy=(helf*0.1, height/2), xytext=(helf*0.3, height/2), 
                    textcoords='data', ha='center', fontsize=16, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['height'], alpha=0.8),
                    arrowprops=dict(arrowstyle="<->", color=colors['height'], lw=2))
        
        # قياس الأوتار
        ax.annotate(f'{beem:.3f}m', xy=(-helf/2, height/3), xytext=(-helf, height/2), 
                    textcoords='data', ha='center', fontsize=14, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['left'], alpha=0.8),
                    arrowprops=dict(arrowstyle="->", color=colors['left'], lw=2))
        
        ax.annotate(f'{beem:.3f}m', xy=(helf/2, height/3), xytext=(helf, height/2), 
                    textcoords='data', ha='center', fontsize=14, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['right'], alpha=0.8),
                    arrowprops=dict(arrowstyle="->", color=colors['right'], lw=2))
        
        if show_angles:
            # إضافة الزوايا مع أقواس
            angle_radius = min(helf, height) * 0.2
            
            # الزاوية اليسرى
            theta_left = np.linspace(0, np.radians(angle), 30)
            x_arc_left = -helf + angle_radius * np.cos(theta_left)
            y_arc_left = angle_radius * np.sin(theta_left)
            ax.plot(x_arc_left, y_arc_left, color=colors['angle'], linewidth=3)
            
            ax.text(-helf + angle_radius*1.5, angle_radius*0.8, f'{angle:.1f}°', 
                    fontsize=16, color=colors['angle'], fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9))
            
            # الزاوية اليمنى
            theta_right = np.linspace(np.radians(180-angle), np.radians(180), 30)
            x_arc_right = helf + angle_radius * np.cos(theta_right)
            y_arc_right = angle_radius * np.sin(theta_right)
            ax.plot(x_arc_right, y_arc_right, color=colors['angle'], linewidth=3)
            
            ax.text(helf - angle_radius*1.5, angle_radius*0.8, f'{angle:.1f}°', 
                    fontsize=16, color=colors['angle'], fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9))
            
            # زاوية القمة إذا كانت موجودة
            if 'top_angle' in st.session_state and st.session_state.top_angle > 0:
                top_angle = st.session_state.top_angle
                theta_top = np.linspace(np.radians(180-angle), np.radians(180+angle), 30)
                x_arc_top = angle_radius * np.cos(theta_top)
                y_arc_top = height + angle_radius * np.sin(theta_top)
                ax.plot(x_arc_top, y_arc_top, color='purple', linewidth=3)
                
                ax.text(0, height + angle_radius*1.5, f'{top_angle:.1f}°', 
                        fontsize=16, color='purple', fontweight='bold', ha='center',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lavender", alpha=0.9))
        
        # إعداد المحاور والمظهر
        margin = max(helf, height) * 0.3
        ax.set_xlim([-helf - margin, helf + margin])
        ax.set_ylim([-height * 0.4, height + margin])
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # العنوان والتسميات
        ax.set_title(f'🎯 {title}\n(القاعدة: {base}m, الارتفاع: {height}m)', 
                     fontsize=18, fontweight='bold', pad=20)
        ax.set_xlabel('المسافة الأفقية (متر)', fontsize=14, fontweight='bold')
        ax.set_ylabel('المسافة الرأسية (متر)', fontsize=14, fontweight='bold')
        
        # وسيلة الإيضاح
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), 
                  ncol=3, fontsize=12, framealpha=0.9)
        
        plt.tight_layout()
        return fig

    with tab1:
        st.header("📐 حساب الوتر بنظرية فيثاغورس")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("🎯 إدخال البيانات")
            
            # استخدام أعمدة للإدخال لمزيد من التنظيم
            col1a, col1b = st.columns(2)
            with col1a:
                base_hyp_text = st.text_input("القاعدة (متر):", value="40", key="base_hyp_text")
            with col1b:
                height_hyp_text = st.text_input("الارتفاع (متر):", value="2", key="height_hyp_text")
            
            if st.button("🧮 حساب الوتر", key="calc_hyp", use_container_width=True):
                try:
                    base_hyp = float(base_hyp_text)
                    height_hyp = float(height_hyp_text)
                    
                    if base_hyp > 0 and height_hyp > 0:
                        # الحسابات
                        helf = base_hyp / 2
                        beem = math.sqrt(helf**2 + height_hyp**2)
                        angle = math.degrees(math.atan(height_hyp / helf))
                        
                        st.session_state.hypotenuse = beem
                        st.session_state.angle_calc = angle
                        st.session_state.helf_calc = helf
                        
                        st.subheader("📊 النتائج")
                        st.success(f"""
                        **🧮 نتائج حساب الوتر:**
                        
                        **📐 البيانات المدخلة:**
                        - القاعدة: {base_hyp} متر
                        - الارتفاع: {height_hyp} متر  
                        
                        **📏 النتائج المحسوبة:**
                        - نصف القاعدة: {helf} متر
                        - طول الوتر: {beem:.3f} متر
                        - الزاوية: {angle:.2f}°

                        **🔢 المعادلات المستخدمة:**
                        - نصف القاعدة = القاعدة ÷ 2 = {base_hyp} ÷ 2 = {helf} متر
                        - الوتر = √(نصف_القاعدة² + الارتفاع²) = √({helf}² + {height_hyp}²) = {beem:.3f} متر
                        - الزاوية = tan⁻¹(الارتفاع ÷ نصف_القاعدة) = tan⁻¹({height_hyp} ÷ {helf}) = {angle:.2f}°
                        """)
                        
                        st.session_state.base_hyp_value = base_hyp
                        st.session_state.height_hyp_value = height_hyp
                    else:
                        st.error("❌ يجب أن تكون القيم أكبر من الصفر")
                        
                except ValueError:
                    st.error("❌ يرجى إدخال قيم رقمية صحيحة")
        
        with col2:
            st.subheader("🎨 الرسم التوضيحي")
            if st.session_state.hypotenuse > 0:
                base_hyp = st.session_state.base_hyp_value
                height_hyp = st.session_state.height_hyp_value
                helf = st.session_state.helf_calc
                beem = st.session_state.hypotenuse
                angle = st.session_state.angle_calc
                
                fig = create_clear_triangle_figure(
                    base_hyp, height_hyp, helf, beem, angle,
                    "رسم توضيحي لحساب الوتر"
                )
                st.pyplot(fig)
                
                # معلومات إضافية تحت الرسم
                st.info(f"""
                **💡 ملاحظات تقنية:**
                - هذا الرسم يوضح تطبيق نظرية فيثاغورس على المثلث القائم
                - الزوايا محسوبة باستخدام الدوال المثلثية العكسية
                - الدقة في الحسابات: ±0.001 متر للأطوال، ±0.01° للزوايا
                """)
            else:
                st.info("""
                **📝 تعليمات:**
                - أدخل قيمة القاعدة والارتفاع في الحقول على اليسار
                - اضغط على زر 'حساب الوتر' لرؤية النتائج والرسم التوضيحي
                - الرسم سيوضح جميع القياسات والزوايا بشكل واضح
                """)

    with tab2:
        st.header("🏗️ حساب الشتلة")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("🎯 إدخال البيانات")
            
            col2a, col2b = st.columns(2)
            with col2a:
                width_raft_text = st.text_input("عرض الجملون (متر):", value="40", key="width_raft_text")
            with col2b:
                height_raft_cm_text = st.text_input("ارتفاع الجملون (سم):", value="200", key="height_raft_cm_text")
            
            if st.button("🧮 حساب الشتلة", key="calc_raft", use_container_width=True):
                try:
                    width_raft = float(width_raft_text)
                    height_raft_cm = float(height_raft_cm_text)
                    
                    if width_raft > 0 and height_raft_cm > 0:
                        height_raft_m = height_raft_cm / 100
                        helf = width_raft / 2
                        beem = math.sqrt(helf**2 + height_raft_m**2)
                        angle = math.degrees(math.atan(height_raft_m / helf))
                        
                        st.session_state.rafter = beem
                        st.session_state.rafter_angle = angle
                        
                        st.subheader("📊 النتائج")
                        st.success(f"""
                        **🏗️ نتائج حساب الشتلة:**
                        
                        **📐 البيانات المدخلة:**
                        - عرض الجملون: {width_raft} متر
                        - ارتفاع الجملون: {height_raft_cm} سم ({height_raft_m} متر)
                        
                        **📏 النتائج المحسوبة:**
                        - نصف العرض: {helf} متر
                        - طول الشتلة الواحدة: {beem:.3f} متر
                        - الطول الكلي للشتلتين: {beem * 2:.3f} متر
                        - زاوية الشتلة: {angle:.2f}°

                        **🔢 المعادلات المستخدمة:**
                        - نصف العرض = العرض ÷ 2 = {width_raft} ÷ 2 = {helf} متر
                        - طول الشتلة = √(نصف_العرض² + الارتفاع²) = √({helf}² + {height_raft_m}²) = {beem:.3f} متر
                        - الزاوية = tan⁻¹(الارتفاع ÷ نصف_العرض) = tan⁻¹({height_raft_m} ÷ {helf}) = {angle:.2f}°
                        """)
                        
                        st.session_state.width_raft_value = width_raft
                        st.session_state.height_raft_m_value = height_raft_m
                        st.session_state.helf_raft_value = helf
                        
                    else:
                        st.error("❌ يجب أن تكون القيم أكبر من الصفر")
                        
                except ValueError:
                    st.error("❌ يرجى إدخال قيم رقمية صحيحة")
        
        with col2:
            st.subheader("🎨 الرسم التوضيحي")
            if st.session_state.rafter > 0:
                width_raft = st.session_state.width_raft_value
                height_raft_m = st.session_state.height_raft_m_value
                helf = st.session_state.helf_raft_value
                beem = st.session_state.rafter
                angle = st.session_state.rafter_angle
                
                fig = create_clear_triangle_figure(
                    width_raft, height_raft_m, helf, beem, angle,
                    "رسم توضيحي للجملون والشتلات"
                )
                st.pyplot(fig)
                
                st.info(f"""
                **💡 معلومات تقنية عن الشتلات:**
                - طول الشتلة الواحدة: {beem:.3f} متر
                - الطول الإجمالي المطلوب: {beem * 2:.3f} متر
                - زاوية القص المطلوبة: {angle:.2f}°
                - نسبة الانحدار: {height_raft_m/helf*100:.1f}%
                """)

    with tab3:
        st.header("📏 حساب الزوايا")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("🎯 إدخال البيانات")
            
            col3a, col3b = st.columns(2)
            with col3a:
                base_ang_text = st.text_input("القاعدة (متر):", value="40", key="base_ang_text")
            with col3b:
                height_ang_text = st.text_input("الارتفاع (متر):", value="2", key="height_ang_text")
            
            if st.button("🧮 حساب الزوايا", key="calc_ang", use_container_width=True):
                try:
                    base_ang = float(base_ang_text)
                    height_ang = float(height_ang_text)
                    
                    if base_ang > 0 and height_ang > 0:
                        helf = base_ang / 2
                        angle = math.degrees(math.atan(height_ang / helf))
                        top_angle = 180 - (2 * angle)
                        
                        st.session_state.angle = angle
                        st.session_state.top_angle = top_angle
                        st.session_state.helf_ang = helf
                        
                        st.subheader("📊 النتائج")
                        st.success(f"""
                        **📏 نتائج حساب الزوايا:**
                        
                        **📐 البيانات المدخلة:**
                        - القاعدة: {base_ang} متر
                        - الارتفاع: {height_ang} متر
                        
                        **📐 النتائج المحسوبة:**
                        - نصف القاعدة: {helf} متر
                        - زاوية القاعدة: {angle:.2f}°
                        - زاوية القمة: {top_angle:.2f}°
                        - زاوية قص الرأس: {top_angle / 2:.2f}°

                        **🔢 المعادلات المستخدمة:**
                        - نصف القاعدة = القاعدة ÷ 2 = {base_ang} ÷ 2 = {helf} متر
                        - زاوية القاعدة = tan⁻¹(الارتفاع ÷ نصف_القاعدة) = tan⁻¹({height_ang} ÷ {helf}) = {angle:.2f}°
                        - زاوية القمة = 180 - (2 × زاوية_القاعدة) = 180 - (2 × {angle:.2f}) = {top_angle:.2f}°
                        - زاوية قص الرأس = زاوية_القمة ÷ 2 = {top_angle:.2f} ÷ 2 = {top_angle / 2:.2f}°
                        """)
                        
                        st.session_state.base_ang_value = base_ang
                        st.session_state.height_ang_value = height_ang
                        
                    else:
                        st.error("❌ يجب أن تكون القيم أكبر من الصفر")
                        
                except ValueError:
                    st.error("❌ يرجى إدخال قيم رقمية صحيحة")
        
        with col2:
            st.subheader("🎨 الرسم التوضيحي")
            if st.session_state.angle > 0:
                base_ang = st.session_state.base_ang_value
                height_ang = st.session_state.height_ang_value
                helf = st.session_state.helf_ang
                angle = st.session_state.angle
                top_angle = st.session_state.top_angle
                
                fig = create_clear_triangle_figure(
                    base_ang, height_ang, helf, st.session_state.hypotenuse, angle,
                    "رسم توضيحي للزوايا"
                )
                st.pyplot(fig)
                
                st.info(f"""
                **💡 معلومات عن الزوايا:**
                - زاوية القاعدة: {angle:.2f}° (تستخدم في قص الأطراف)
                - زاوية القمة: {top_angle:.2f}° (الزاوية بين الشتلتين)
                - زاوية قص الرأس: {top_angle / 2:.2f}° (لكل شتلة)
                - مجموع زوايا المثلث: 180° (للتحقق: {angle:.2f} + {angle:.2f} + {top_angle:.2f} = 180°)
                """)

    with tab4:
        st.header("📊 حساب الكمر")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("🎯 إدخال بيانات الكمر")
            
            col4a, col4b = st.columns(2)
            with col4a:
                kamer_width_text = st.text_input("عرض الكمر (متر):", value="40", key="kamer_width_text")
            with col4b:
                kamer_height_text = st.text_input("ارتفاع الكمر (متر):", value="2", key="kamer_height_text")
            
            if st.button("🧮 حساب الكمر", key="calc_kamer", use_container_width=True):
                try:
                    kamer_width = float(kamer_width_text)
                    kamer_height = float(kamer_height_text)
                    
                    if kamer_width > 0 and kamer_height > 0:
                        helf = kamer_width / 2
                        beem = math.sqrt(helf**2 + kamer_height**2)
                        angle = math.degrees(math.atan(kamer_height / helf))
                        
                        st.subheader("📊 نتائج حساب الكمر")
                        st.success(f"""
                        **📊 نتائج حساب الكمر:**
                        
                        **📐 البيانات المدخلة:**
                        - عرض الكمر: {kamer_width} متر
                        - ارتفاع الكمر: {kamer_height} متر
                        
                        **📏 النتائج المحسوبة:**
                        - نصف العرض: {helf} متر
                        - طول الكمر: {beem:.3f} متر
                        - الطول الإجمالي: {beem * 2:.3f} متر
                        - زاوية الكمر: {angle:.2f}°

                        **🔢 المعادلات المستخدمة:**
                        - نصف العرض = العرض ÷ 2 = {kamer_width} ÷ 2 = {helf} متر
                        - طول الكمر = √(نصف_العرض² + الارتفاع²) = √({helf}² + {kamer_height}²) = {beem:.3f} متر
                        - الزاوية = tan⁻¹(الارتفاع ÷ نصف_العرض) = tan⁻¹({kamer_height} ÷ {helf}) = {angle:.2f}°
                        """)
                        
                        st.session_state.kamer_width = kamer_width
                        st.session_state.kamer_height = kamer_height
                        st.session_state.kamer_beem = beem
                        st.session_state.kamer_angle = angle
                        st.session_state.kamer_helf = helf
                        
                    else:
                        st.error("❌ يجب أن تكون القيم أكبر من الصفر")
                        
                except ValueError:
                    st.error("❌ يرجى إدخال قيم رقمية صحيحة")
        
        with col2:
            st.subheader("🎨 الرسم التوضيحي للكمر")
            if 'kamer_width' in st.session_state:
                kamer_width = st.session_state.kamer_width
                kamer_height = st.session_state.kamer_height
                helf = st.session_state.kamer_helf
                beem = st.session_state.kamer_beem
                angle = st.session_state.kamer_angle
                
                fig = create_clear_triangle_figure(
                    kamer_width, kamer_height, helf, beem, angle,
                    "رسم توضيحي للكمر"
                )
                st.pyplot(fig)
                
                st.info(f"""
                **💡 معلومات تقنية عن الكمر:**
                - طول كل جزء مائل: {beem:.3f} متر
                - الطول الإجمالي للمواد: {beem * 2:.3f} متر
                - زاوية التثبيت: {angle:.2f}°
                - مساحة السطح: {kamer_width * beem:.2f} متر مربع
                """)

    # الشريط الجانبي
    with st.sidebar:
        st.header("ℹ️ معلومات سريعة")
        
        st.markdown("""
        **📐 المعادلات الأساسية:**
        ```
        نصف القاعدة = القاعدة ÷ 2
        الوتر = √(نصف_القاعدة² + الارتفاع²)
        الزاوية = tan⁻¹(الارتفاع ÷ نصف_القاعدة)
        ```
        
        **🔍 مثال تطبيقي:**
        ```
        القاعدة = 40 متر
        الارتفاع = 2 متر
        نصف القاعدة = 40 ÷ 2 = 20 متر
        الوتر = √(20² + 2²) = √404 = 20.099 متر
        الزاوية = tan⁻¹(2 ÷ 20) = 5.71°
        ```
        """)
        
        st.header("⚙️ الإعدادات")
        
        # إعدادات الرسم
        st.subheader("🎨 إعدادات الرسم")
        show_grid = st.checkbox("إظهار الشبكة", value=True)
        show_angles = st.checkbox("إظهار الزوايا", value=True)
        
        st.header("🧹 تنظيف")
        if st.button("مسح جميع الحقول", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # تذييل الصفحة
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>تم تطوير هذه الآلة الحاسبة باستخدام Streamlit و Python</p>
        <p>جميع الحسابات تعتمد على المعادلات الرياضية الأساسية والدوال المثلثية</p>
    </div>
    """, unsafe_allow_html=True)

    # تشغيل التطبيق
    st.success("✅ تم تحميل الآلة الحاسبة بنجاح! اختر تبويباً للبدء.")

if __name__ == "__main__":
    tan_main()