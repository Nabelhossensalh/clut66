import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from math import sqrt, atan, degrees, radians
import plotly.graph_objects as go
import plotly.express as px

class SlopeAnalysis3D:
    def __init__(self):
        # ألوان محددة للعناصر
        self.ground_color = '#2E8B57'
        self.hypotenuse_color = '#FF6B35'
        self.angle_color = '#FFD166'
        self.base_color = '#4ECDC4'
        self.height_color = '#6A0572'
        self.structure_color = '#1A535C'
        
        # تهيئة البيانات
        self.geometry_data = None
        
    def calculate_geometry(self, base, height, depth):
        """حساب الأبعاد الهندسية الأساسية"""
        hypotenuse = sqrt(base ** 2 + height ** 2)
        space_diagonal = sqrt(base ** 2 + height ** 2 + depth ** 2)
        angle_base = degrees(atan(height / base))
        angle_top = 90 - angle_base
        volume = 0.5 * base * height * depth
        
        self.geometry_data = {
            'base': base, 'height': height, 'depth': depth,
            'hypotenuse': hypotenuse, 'space_diagonal': space_diagonal,
            'angle_base': angle_base, 'angle_top': angle_top,
            'volume': volume
        }
        return self.geometry_data
    
    def plot_matplotlib_3d(self, line_thickness=2):
        """رسم ثلاثي الأبعاد باستخدام matplotlib"""
        if not self.geometry_data:
            return None
            
        base = self.geometry_data['base']
        height = self.geometry_data['height']
        depth = self.geometry_data['depth']
        hypotenuse = self.geometry_data['hypotenuse']
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 🎨 رسم الأرضية الملونة
        x_ground = np.linspace(-base * 0.2, base * 1.2, 10)
        z_ground = np.linspace(-depth * 0.2, depth * 1.2, 10)
        X, Z = np.meshgrid(x_ground, z_ground)
        Y = np.zeros_like(X) - height * 0.1
        
        ax.plot_surface(X, Y, Z, color=self.ground_color, alpha=0.6, shade=True)
        
        # نقاط الهيكل الرئيسية
        points = [
            [0, 0, 0],           # P1 - الزاوية الأمامية اليسرى
            [base, 0, 0],        # P2 - الزاوية الأمامية اليمنى  
            [base / 2, height, 0], # P3 - القمة الأمامية
            [0, 0, depth],       # P4 - الزاوية الخلفية اليسرى
            [base, 0, depth],    # P5 - الزاوية الخلفية اليمنى
            [base / 2, height, depth] # P6 - القمة الخلفية
        ]
        
        # 🔺 تعريف أوجه المنشور الثلاثي
        faces = [
            [points[0], points[1], points[2]],  # الوجه الأمامي (مثلث)
            [points[3], points[4], points[5]],  # الوجه الخلفي (مثلث)
            [points[0], points[1], points[4], points[3]],  # القاعدة (مستطيل)
            [points[1], points[2], points[5], points[4]],  # الوجه الأيمن
            [points[2], points[0], points[3], points[5]]   # الوجه الأيسر
        ]
        
        # 🎨 رسم الأسطح الرئيسية
        poly3d = Poly3DCollection(
            faces,
            facecolors=[
                self.structure_color,  # أمامي
                self.structure_color,  # خلفي  
                self.base_color,       # قاعدة
                self.structure_color,  # يمين
                self.structure_color   # يسار
            ],
            linewidths=line_thickness,
            edgecolors='black',
            alpha=0.9
        )
        ax.add_collection3d(poly3d)
        
        # 📏 رسم الوتر (الخط المائل)
        hypotenuse_lines = [
            [points[0], points[2]],  # وتر أمامي
            [points[3], points[5]],  # وتر خلفي
        ]
        
        hyp_collection = Line3DCollection(
            hypotenuse_lines,
            colors=[self.hypotenuse_color, self.hypotenuse_color],
            linewidths=line_thickness + 1,
            linestyles='-',
            alpha=1.0
        )
        ax.add_collection3d(hyp_collection)
        
        # 📐 رسم الزوايا والقياسات
        self._draw_angle_annotations(ax, base, height)
        self._add_dimension_labels(ax, points, base, height, depth, hypotenuse)
        
        # ⚙️ إعداد المحاور والمظهر
        margin = max(base, height, depth) * 0.3
        ax.set_xlim([-margin, base + margin])
        ax.set_ylim([-margin, height + margin])
        ax.set_zlim([-margin, depth + margin])
        
        ax.set_xlabel('المحور X (الطول)', fontsize=12, labelpad=15, fontweight='bold')
        ax.set_ylabel('المحور Y (الارتفاع)', fontsize=12, labelpad=15, fontweight='bold')
        ax.set_zlabel('المحور Z (العمق)', fontsize=12, labelpad=15, fontweight='bold')
        
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#ffffff')
        
        title = f"""الهيكل الثلاثي الأبعاد
القاعدة: {base}م, الارتفاع: {height}م, العمق: {depth}م
الوتر: {hypotenuse:.3f}م, الزاوية: {self.geometry_data['angle_base']:.2f}°"""
        
        ax.set_title(title, fontsize=14, pad=25, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_plotly_3d(self):
        """رسم ثلاثي الأبعاد تفاعلي باستخدام Plotly"""
        if not self.geometry_data:
            return None
            
        base = self.geometry_data['base']
        height = self.geometry_data['height']
        depth = self.geometry_data['depth']
        
        # تعريف نقاط المنشور الثلاثي
        vertices = np.array([
            [0, 0, 0],      # 0
            [base, 0, 0],   # 1  
            [base/2, height, 0], # 2
            [0, 0, depth],  # 3
            [base, 0, depth], # 4
            [base/2, height, depth] # 5
        ])
        
        # تعريف الأوجه
        faces = [
            [0, 1, 2],  # وجه أمامي
            [3, 4, 5],  # وجه خلفي
            [0, 1, 4, 3],  # قاعدة
            [1, 2, 5, 4],  # وجه أيمن
            [2, 0, 3, 5]   # وجه أيسر
        ]
        
        fig = go.Figure()
        
        # إضافة الأسطح
        for i, face in enumerate(faces):
            x = vertices[face, 0]
            y = vertices[face, 1] 
            z = vertices[face, 2]
            
            fig.add_trace(go.Mesh3d(
                x=x, y=y, z=z,
                color=self.structure_color,
                opacity=0.8,
                name=f'وجه {i+1}'
            ))
        
        # إضافة الحواف
        edges = [
            [0, 1], [1, 2], [2, 0],  # أمامي
            [3, 4], [4, 5], [5, 3],  # خلفي  
            [0, 3], [1, 4], [2, 5]   # وصلات
        ]
        
        for edge in edges:
            x = vertices[edge, 0]
            y = vertices[edge, 1]
            z = vertices[edge, 2]
            
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line=dict(color='black', width=4),
                showlegend=False
            ))
        
        # إضافة الوتر الملون
        fig.add_trace(go.Scatter3d(
            x=[vertices[0, 0], vertices[2, 0]],
            y=[vertices[0, 1], vertices[2, 1]], 
            z=[vertices[0, 2], vertices[2, 2]],
            mode='lines',
            line=dict(color=self.hypotenuse_color, width=6),
            name='الوتر'
        ))
        
        fig.update_layout(
            title=f'الهيكل الثلاثي الأبعاد التفاعلي<br>القاعدة: {base}م, الارتفاع: {height}م, العمق: {depth}م',
            scene=dict(
                xaxis_title='المحور X (الطول)',
                yaxis_title='المحور Y (الارتفاع)',
                zaxis_title='المحور Z (العمق)',
                aspectmode='data'
            ),
            width=800,
            height=600
        )
        
        return fig
    
    def _draw_angle_annotations(self, ax, base, height):
        """رسم الزوايا والقياسات التوضيحية"""
        angle_base = self.geometry_data['angle_base']
        
        # رسم قوس الزاوية
        theta = np.linspace(0, radians(angle_base), 30)
        arc_radius = min(base, height) * 0.3
        
        x_arc = arc_radius * np.cos(theta)
        y_arc = arc_radius * np.sin(theta) 
        z_arc = np.zeros_like(x_arc)
        
        ax.plot(x_arc, y_arc, z_arc, color=self.angle_color, 
                linewidth=3, alpha=0.8)
        
        # نص الزاوية
        ax.text(arc_radius * 0.7, arc_radius * 0.3, 0,
                f'θ = {angle_base:.1f}°', fontsize=11, 
                color=self.angle_color, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    def _add_dimension_labels(self, ax, points, base, height, depth, hypotenuse):
        """إضافة تسميات الأبعاد على الرسم"""
        
        # تسمية النقاط
        labels = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
        for i, point in enumerate(points):
            ax.text(point[0], point[1], point[2], labels[i],
                   fontsize=10, color='darkred', fontweight='bold')
        
        # تسمية الأبعاد الرئيسية
        dimension_texts = [
            [base/2, -height*0.15, -depth*0.1, f'القاعدة: {base:.1f}م', self.base_color],
            [-base*0.2, height/2, -depth*0.1, f'الارتفاع: {height:.1f}م', self.height_color],
            [base*1.1, height/2, depth/2, f'العمق: {depth:.1f}م', 'blue'],
            [base/4, height/3, 0, f'الوتر: {hypotenuse:.2f}م', self.hypotenuse_color]
        ]
        
        for x, y, z, text, color in dimension_texts:
            ax.text(x, y, z, text, fontsize=11, color=color, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

def main():
    st.set_page_config(
        page_title="النظام المتقدم للرسم ثلاثي الأبعاد",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # تخصيص التصميم
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1A535C;
        border-bottom: 2px solid #4ECDC4;
        padding-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🏗️ النظام المتقدم للرسم ثلاثي الأبعاد</h1>', unsafe_allow_html=True)
    
    # إنشاء كائن التحليل
    analyzer = SlopeAnalysis3D()
    
    # 📐 الشريط الجانبي للإدخالات
    with st.sidebar:
        st.markdown('<h2 class="section-header">📐 إعدادات الأبعاد</h2>', unsafe_allow_html=True)
        
        base = st.slider("طول القاعدة (م)", 1.0, 50.0, 10.0, 0.1)
        height = st.slider("الارتفاع (م)", 1.0, 30.0, 7.0, 0.1)  
        depth = st.slider("العمق (م)", 1.0, 30.0, 12.0, 0.1)
        angle = st.slider("زاوية الميل (°)", 1.0, 89.0, 45.0, 0.1)
        
        # تحديث الارتفاع بناءً على الزاوية إذا رغب المستخدم
        if st.checkbox("تحديث الارتفاع تلقائياً بناءً على الزاوية"):
            height = base * np.tan(np.radians(angle))
            st.info(f"الارتفاع المعدل: {height:.2f} م")
        
        line_thickness = st.slider("سمك الخطوط", 1, 10, 3)
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">🎨 تخصيص الألوان</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            analyzer.base_color = st.color_picker("لون القاعدة", analyzer.base_color)
            analyzer.height_color = st.color_picker("لون الارتفاع", analyzer.height_color)
            analyzer.structure_color = st.color_picker("لون الهيكل", analyzer.structure_color)
        with col2:
            analyzer.hypotenuse_color = st.color_picker("لون الوتر", analyzer.hypotenuse_color)
            analyzer.angle_color = st.color_picker("لون الزوايا", analyzer.angle_color)
            analyzer.ground_color = st.color_picker("لون الأرض", analyzer.ground_color)
    
    # 🎯 المنطقة الرئيسية
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">🎯 الرسم ثلاثي الأبعاد</h2>', unsafe_allow_html=True)
        
        # حساب الهندسة
        geometry_data = analyzer.calculate_geometry(base, height, depth)
        
        # اختيار نوع الرسم
        plot_type = st.radio("اختر نوع الرسم:", ["Matplotlib (ثابت)", "Plotly (تفاعلي)"])
        
        if plot_type == "Matplotlib (ثابت)":
            fig = analyzer.plot_matplotlib_3d(line_thickness)
            if fig:
                st.pyplot(fig)
        else:
            fig = analyzer.plot_plotly_3d() 
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h2 class="section-header">📊 النتائج المحسوبة</h2>', unsafe_allow_html=True)
        
        if geometry_data:
            # عرض النتائج في بطاقات
            st.metric("📐 طول الوتر", f"{geometry_data['hypotenuse']:.3f} م")
            st.metric("📏 القطر الفضائي", f"{geometry_data['space_diagonal']:.3f} م") 
            st.metric("📊 الزاوية عند القاعدة", f"{geometry_data['angle_base']:.2f}°")
            st.metric("📈 الزاوية عند القمة", f"{geometry_data['angle_top']:.2f}°")
            st.metric("🧮 الحجم", f"{geometry_data['volume']:.3f} م³")
            
            st.markdown("---")
            st.markdown("### 📝 تفسير النتائج:")
            
            explanations = [
                f"**الوتر ({geometry_data['hypotenuse']:.3f} م)**: هو الضلع المائل في المثلث، يحسب باستخدام نظرية فيثاغورس: √(القاعدة² + الارتفاع²)",
                f"**القطر الفضائي ({geometry_data['space_diagonal']:.3f} م)**: هو أطول مسافة داخل المنشور، يحسب: √(القاعدة² + الارتفاع² + العمق²)", 
                f"**الزاوية ({geometry_data['angle_base']:.2f}°)**: تحسب باستخدام الدالة المثلثية: tan⁻¹(الارتفاع/القاعدة)",
                f"**الحجم ({geometry_data['volume']:.3f} م³)**: يحسب بضرب مساحة المثلث في العمق: (½ × القاعدة × الارتفاع) × العمق"
            ]
            
            for exp in explanations:
                st.info(exp)
    
    # 📚 قسم الشرح التفصيلي
    st.markdown("---")
    st.markdown('<h2 class="section-header">📚 الشرح التفصيلي للحسابات</h2>', unsafe_allow_html=True)
    
    with st.expander("🔍 كيف تم حساب الأبعاد والزوايا؟", expanded=True):
        st.markdown("""
        ### 📐 الحسابات الهندسية المستخدمة:
        
        **1. حساب الوتر (الضلع المائل):**
        ```
        الوتر = √(القاعدة² + الارتفاع²)
        المثال: √(10² + 7²) = √(100 + 49) = √149 ≈ 12.206 م
        ```
        
        **2. حساب الزاوية عند القاعدة:**
        ```
        الزاوية = tan⁻¹(الارتفاع / القاعدة)  
        المثال: tan⁻¹(7 / 10) = tan⁻¹(0.7) ≈ 35.0°
        ```
        
        **3. حساب القطر الفضائي:**
        ```
        القطر_الفضائي = √(القاعدة² + الارتفاع² + العمق²)
        المثال: √(10² + 7² + 12²) = √(100 + 49 + 144) = √293 ≈ 17.117 م
        ```
        
        **4. حساب الحجم:**
        ```
        الحجم = (½ × القاعدة × الارتفاع) × العمق
        المثال: (0.5 × 10 × 7) × 12 = 35 × 12 = 420 م³
        ```
        
        ### 🎨 تفسير الألوان في الرسم:
        - **🟢 لون الأرض**: يظهر السطح الذي يرتكز عليه الهيكل
        - **🔵 لون القاعدة**: يمثل الضلع الأفقي السفلي  
        - **🟣 لون الارتفاع**: يمثل الضلع الرأسي
        - **🟠 لون الوتر**: يمثل الضلع المائل (الوتر)
        - **🟡 لون الزوايا**: يظهر قياسات الزوايا
        - **🔶 لون الهيكل**: لون الأسطح الجانبية للمنشور
        """)

if __name__ == "__main__":
    main()
def demasinal_main():
    """الدالة الرئيسية لتطبيق حساب المساحات"""
    main()

if __name__ == "__main__":
    main()