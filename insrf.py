import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, simpson
import io
import base64

class LandAreaCalculator:
    def __init__(self, lengths, widths):
        self.lengths = lengths
        self.widths = widths
        self.areas = {}
    
    def calculate_all_methods(self):
        """حساب المساحة بجميع الطرق"""
        # طريقة شبه المنحرف
        self.areas['طريقة شبه المنحرف'] = np.trapz(self.widths, self.lengths)
        
        # طريقة سمبسون
        self.areas['طريقة سمبسون'] = simpson(self.widths, self.lengths)
        
        # طريقة التكامل العددي
        def width_function(l):
            return np.interp(l, self.lengths, self.widths)
        
        integral_area, error = quad(width_function, min(self.lengths), max(self.lengths))
        self.areas['طريقة التكامل'] = integral_area
        
        # طريقة التقسيم إلى أجزاء
        total_area = 0
        for i in range(len(self.lengths) - 1):
            avg_width = (self.widths[i] + self.widths[i + 1]) / 2
            segment_length = self.lengths[i + 1] - self.lengths[i]
            total_area += avg_width * segment_length
        self.areas['طريقة التقسيم'] = total_area
        
        return self.areas
    
    def plot_land(self):
        """رسم شكل الأرض"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # رسم الشكل
        ax.plot(self.lengths, self.widths, 'b-', linewidth=3, label='حدود الأرض', marker='o', markersize=8)
        ax.fill_between(self.lengths, self.widths, alpha=0.3, color='green', label='المساحة')
        
        # إضافة النقاط والتسميات
        for i, (x, y) in enumerate(zip(self.lengths, self.widths)):
            ax.annotate(f'({x}m, {y}m)', (x, y), xytext=(5, 5),
                       textcoords='offset points', fontsize=10, fontweight='bold')
        
        ax.set_title('حساب مساحة الأرض ذات الانحراف', fontsize=16, fontweight='bold')
        ax.set_xlabel('الطول (متر)', fontsize=12)
        ax.set_ylabel('العرض (متر)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # إضافة معلومات المساحة
        info_text = "نتائج حساب المساحة:\n\n"
        for method, area in self.areas.items():
            info_text += f"{method}: {area:.2f} م²\n"
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                verticalalignment='top', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        return fig

def get_explanation_image():
    """إنشاء صورة توضيحية للشرح"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # الرسم الأول: طريقة شبه المنحرف
    x = [0, 5, 10]
    y = [4, 6, 4]
    ax1.fill_between(x, y, alpha=0.3, color='blue')
    ax1.plot(x, y, 'bo-', linewidth=2)
    ax1.set_title('طريقة شبه المنحرف', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # الرسم الثاني: طريقة سمبسون
    x2 = np.linspace(0, 10, 50)
    y2 = 5 + np.sin(x2)
    ax2.fill_between(x2, y2, alpha=0.3, color='green')
    ax2.plot(x2, y2, 'g-', linewidth=2)
    ax2.set_title('طريقة سمبسون', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # الرسم الثالث: طريقة التقسيم
    x3 = [0, 3, 7, 10]
    y3 = [4, 7, 5, 6]
    ax3.fill_between(x3, y3, alpha=0.3, color='red')
    ax3.plot(x3, y3, 'ro-', linewidth=2)
    ax3.set_title('طريقة التقسيم', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # تحويل الرسم إلى صورة base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    
    return img_str

def main():
    st.set_page_config(
        page_title="الحاسبة المتقدمة لمساحات الأراضي",
        page_icon="🏞️",
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
        margin-top: 2rem;
    }
    .result-box {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .method-explanation {
        background-color: #e8f5e8;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🏞️ الحاسبة المتقدمة لمساحات الأراضي</h1>', unsafe_allow_html=True)
    
    # الشريط الجانبي للإدخال
    with st.sidebar:
        st.markdown('<h2 class="section-header">📐 إدخال بيانات الأرض</h2>', unsafe_allow_html=True)
        
        st.info("""
        **تعليمات الإدخال:**
        - أدخل النقاط الطولية والعروض المقابلة
        - استخدم الفاصلة لفصل القيم
        - مثال: 0, 13, 15, 20
        """)
        
        # إدخال النقاط الطولية
        lengths_input = st.text_input("النقاط على محور الطول (متر):", "0, 13, 15, 20")
        
        # إدخال العروض
        widths_input = st.text_input("العروض المقابلة (متر):", "10, 10, 9, 9")
        
        # زر الحساب
        calculate_btn = st.button("🧮 حساب المساحة", type="primary", use_container_width=True)
        
        # زر الرسم
        plot_btn = st.button("📊 رسم الشكل", use_container_width=True)
        
        # زر شرح الطرق
        explain_btn = st.button("📚 شرح طرق الحساب", use_container_width=True)
    
    # المنطقة الرئيسية
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if calculate_btn or plot_btn:
            try:
                # تحويل البيانات المدخلة
                lengths = [float(x.strip()) for x in lengths_input.split(",")]
                widths = [float(x.strip()) for x in widths_input.split(",")]
                
                if len(lengths) != len(widths):
                    st.error("❌ يجب أن يتساوى عدد النقاط الطولية مع عدد العروض")
                elif len(lengths) < 2:
                    st.error("❌ يجب إدخال نقطتين على الأقل")
                else:
                    # إنشاء الكائن والحساب
                    calculator = LandAreaCalculator(lengths, widths)
                    areas = calculator.calculate_all_methods()
                    
                    if calculate_btn:
                        st.markdown('<h2 class="section-header">📊 نتائج حساب المساحة</h2>', unsafe_allow_html=True)
                        
                        # عرض النتائج في بطاقات
                        cols = st.columns(2)
                        methods = list(areas.keys())
                        
                        for i, (col, method) in enumerate(zip(cols * 2, methods)):
                            with col:
                                area = areas[method]
                                st.metric(
                                    label=f"**{method}**",
                                    value=f"{area:.4f} م²",
                                    delta=f"{(area - np.mean(list(areas.values()))):.4f}" if i > 0 else None
                                )
                        
                        # المتوسط
                        avg_area = np.mean(list(areas.values()))
                        st.success(f"**المساحة المتوسطة: {avg_area:.4f} متر مربع**")
                    
                    if plot_btn:
                        st.markdown('<h2 class="section-header">🎨 رسم شكل الأرض</h2>', unsafe_allow_html=True)
                        fig = calculator.plot_land()
                        st.pyplot(fig)
                        
            except Exception as e:
                st.error(f"❌ حدث خطأ في البيانات: {str(e)}")
    
    with col2:
        if calculate_btn:
            st.markdown('<h2 class="section-header">📈 تحليل النتائج</h2>', unsafe_allow_html=True)
            
            # مخطط شريطي للمقارنة
            if 'areas' in locals():
                fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
                methods = list(areas.keys())
                values = list(areas.values())
                
                bars = ax_bar.bar(methods, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
                ax_bar.set_title('مقارنة طرق حساب المساحة', fontweight='bold')
                ax_bar.set_ylabel('المساحة (م²)')
                ax_bar.tick_params(axis='x', rotation=45)
                
                # إضافة القيم على الأعمدة
                for bar, value in zip(bars, values):
                    ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                               f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig_bar)
    
    # قسم شرح طرق الحساب
    if explain_btn:
        st.markdown('<h2 class="section-header">📚 شرح مفصل لطرق حساب المساحة</h2>', unsafe_allow_html=True)
        
        # الصور التوضيحية
        st.markdown("### 🎨 رسم توضيحي للطرق المختلفة")
        img_str = get_explanation_image()
        st.markdown(f'<img src="data:image/png;base64,{img_str}" width="100%">', unsafe_allow_html=True)
        
        # شرح طريقة شبه المنحرف
        with st.expander("📐 طريقة شبه المنحرف (Trapezoidal Rule)", expanded=True):
            st.markdown("""
            <div class="method-explanation">
            <h4>🧮 الصيغة الرياضية:</h4>
            <p>المساحة = ∑ [ (العرض₁ + العرض₂) / 2 × الطول ]</p>
            
            <h4>📖 الشرح:</h4>
            <p>تقسم الأرض إلى عدة أقسام على شكل شبه منحرف، وتحسب مساحة كل قسم ثم تجمع.</p>
            
            <h4>⚡ المميزات:</h4>
            <ul>
            <li>بسيطة وسهلة التطبيق</li>
            <li>دقيقة للأشكال شبه المنحرفة</li>
            <li>مناسبة لمعظم الأشكال العادية</li>
            </ul>
            
            <h4>🔍 مثال تطبيقي:</h4>
            <p>إذا كانت لدينا نقاط: (0,10), (13,10), (15,9), (20,9)</p>
            <p>المساحة = [(10+10)/2 × 13] + [(10+9)/2 × 2] + [(9+9)/2 × 5] = 130 + 19 + 22.5 = 171.5 م²</p>
            </div>
            """, unsafe_allow_html=True)
        
        # شرح طريقة سمبسون
        with st.expander("📊 طريقة سمبسون (Simpson's Rule)"):
            st.markdown("""
            <div class="method-explanation">
            <h4>🧮 الصيغة الرياضية:</h4>
            <p>المساحة = (h/3) × [y₀ + yₙ + 4∑y_فردي + 2∑y_زوجي]</p>
            
            <h4>📖 الشرح:</h4>
            <p>تستخدم منحنيات تربيعية (قطع مكافئ) لتقريب الشكل، مما يعطي دقة أعلى للأشكال المنحنية.</p>
            
            <h4>⚡ المميزات:</h4>
            <ul>
            <li>دقة عالية للأشكال المنحنية</li>
            <li>مناسبة للأراضي ذات التضاريس المعقدة</li>
            <li>تستخدم في الحسابات الهندسية الدقيقة</li>
            </ul>
            
            <h4>⚠️ الشروط:</h4>
            <ul>
            <li>يجب أن يكون عدد الفترات زوجياً</li>
            <li>تتطلب توزيعاً منتظماً للنقاط</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # شرح طريقة التكامل
        with st.expander("📈 طريقة التكامل العددي (Numerical Integration)"):
            st.markdown("""
            <div class="method-explanation">
            <h4>🧮 الصيغة الرياضية:</h4>
            <p>المساحة = ∫ من أ إلى ب للعرض(الطول) دالطول</p>
            
            <h4>📖 الشرح:</h4>
            <p>تستخدم خوارزميات متقدمة لحساب التكامل العددي للمنحني، مما يعطي دقة عالية جداً.</p>
            
            <h4>⚡ المميزات:</h4>
            <ul>
            <li>أعلى درجة من الدقة</li>
            <li>مناسبة للأشكال المعقدة جداً</li>
            <li>تستخدم في البرامج الهندسية المتخصصة</li>
            </ul>
            
            <h4>🔧 التقنية:</h4>
            <p>تستخدم مكتبة SciPy المتقدمة وخوارزميات التكامل التكيفي</p>
            </div>
            """, unsafe_allow_html=True)
        
        # شرح طريقة التقسيم
        with st.expander("📏 طريقة التقسيم (Division Method)"):
            st.markdown("""
            <div class="method-explanation">
            <h4>🧮 الصيغة الرياضية:</h4>
            <p>المساحة = ∑ [ متوسط العرض × طول القسم ]</p>
            
            <h4>📖 الشرح:</h4>
            <p>تقسم الأرض إلى أقسام صغيرة، وتحسب مساحة كل قسم بمتوسط العرضين ثم تجمع المساحات.</p>
            
            <h4>⚡ المميزات:</h4>
            <ul>
            <li>سهلة الفهم والتطبيق</li>
            <li>لا تتطلب رياضيات متقدمة</li>
            <li>مناسبة للحسابات اليدوية</li>
            </ul>
            
            <h4>🔍 مثال تطبيقي:</h4>
            <p>لقسم بين نقطتين (13,10) و (15,9):</p>
            <p>متوسط العرض = (10 + 9) / 2 = 9.5</p>
            <p>طول القسم = 15 - 13 = 2</p>
            <p>مساحة القسم = 9.5 × 2 = 19 م²</p>
            </div>
            """, unsafe_allow_html=True)
    
    # قسم التقرير
    if calculate_btn and 'areas' in locals():
        st.markdown("---")
        st.markdown('<h2 class="section-header">📋 تقرير مفصل</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("البيانات المدخلة")
            st.write(f"**النقاط الطولية:** {lengths}")
            st.write(f"**العروض المقابلة:** {widths}")
            st.write(f"**عدد النقاط:** {len(lengths)}")
            st.write(f"**أقصى طول:** {max(lengths)} متر")
            st.write(f"**أدنى طول:** {min(lengths)} متر")
        
        with col2:
            st.subheader("التحليل الإحصائي")
            areas_list = list(areas.values())
            st.write(f"**أعلى مساحة:** {max(areas_list):.4f} م²")
            st.write(f"**أدنى مساحة:** {min(areas_list):.4f} م²")
            st.write(f"**المتوسط:** {np.mean(areas_list):.4f} م²")
            st.write(f"**الانحراف المعياري:** {np.std(areas_list):.4f} م²")
            st.write(f"**نسبة الاختلاف:** {(max(areas_list)-min(areas_list))/np.mean(areas_list)*100:.2f}%")
        
        # زر تصدير التقرير
        if st.button("💾 تصدير التقرير"):
            report_text = f"""
            تقرير حساب مساحة الأرض
            {'='*50}
            التاريخ: {st.session_state.get('current_time', 'غير محدد')}
            
            البيانات المدخلة:
            - النقاط الطولية: {lengths}
            - العروض: {widths}
            
            نتائج الحساب:
            """
            
            for method, area in areas.items():
                report_text += f"- {method}: {area:.4f} م²\n"
            
            report_text += f"\nالمساحة المتوسطة: {np.mean(list(areas.values())):.4f} م²"
            
            st.download_button(
                label="📥 تحميل التقرير",
                data=report_text,
                file_name="تقرير_مساحة_الأرض.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
def insrf_main():
    """الدالة الرئيسية لتطبيق حساب المساحات"""
    main()

if __name__ == "__main__":
    main()