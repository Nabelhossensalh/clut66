import streamlit as st
import sys
import os

# إضافة المسار الحالي للوحدات
sys.path.append(os.path.dirname(__file__))

# استيراد التطبيقات
try:
    from insrf import insrf_main
    from tan import tan_main
    from dimshnal import demasinal_main
except ImportError as e:
    st.error(f"خطأ في استيراد الملفات: {e}")
    st.info("تأكد من وجود الملفات insrf.py و tan.py و dimshnal.py في نفس المجلد")

def show_homepage():
    """عرض الصفحة الرئيسية"""
    st.markdown('<h1 class="main-header">🏗️ النظام المتكامل للتحليل الهندسي</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <p style='font-size: 1.3rem; color: #666;'>
        نظام متكامل يجمع بين أدوات التحليل الهندسي المتقدمة في واجهة واحدة موحدة
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # بطاقات التطبيقات
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; padding: 25px; margin: 15px 0; color: white;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>🏞️</div>
            <h2 style='color: white; margin-bottom: 15px;'>حساب المساحات</h2>
            <p style='color: rgba(255,255,255,0.9);'>
            حساب مساحات الأراضي غير المنتظمة باستخدام طرق متعددة
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%); 
                    border-radius: 15px; padding: 25px; margin: 15px 0; color: white;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>📐</div>
            <h2 style='color: white; margin-bottom: 15px;'>تحليل الزوايا</h2>
            <p style='color: rgba(255,255,255,0.9);'>
            تحليل الزوايا والمنحدرات للأرض والهياكل الهندسية
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); 
                    border-radius: 15px; padding: 25px; margin: 15px 0; color: white;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>📊</div>
            <h2 style='color: white; margin-bottom: 15px;'>التحليل البُعدي</h2>
            <p style='color: rgba(255,255,255,0.9);'>
            تحليل الأبعاد والقياسات الهندسية للأراضي والهياكل
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("**🚀 ابدأ الآن:** اختر أي تطبيق من القائمة الجانبية لاستخدامه")

def main():
    st.set_page_config(
        page_title="النظام المتكامل للتحليل الهندسي",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # تصميم الصفحة
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #1A535C;
        border-bottom: 3px solid #4ECDC4;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # الشريط الجانبي للتنقل
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='color: #2E8B57; font-size: 1.8rem;'>🏗️ النظام المتكامل</h1>
            <p style='color: #666;'>للتحليل الهندسي المتقدم</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧭 التنقل بين التطبيقات")
        
        app_choice = st.radio(
            "اختر التطبيق:",
            [
                "🏠 الصفحة الرئيسية", 
                "🏞️ حساب مساحات الأراضي", 
                "📐 تحليل الزوايا والمنحدرات (tan)", 
                "📊 التحليل البُعدي (dimshnal)"
            ],
            index=0
        )

    # الصفحة الرئيسية
    if app_choice == "🏠 الصفحة الرئيسية":
        show_homepage()

    # تطبيقات أخرى
    elif app_choice == "🏞️ حساب مساحات الأراضي":
        st.markdown('<h1 class="main-header">🏞️ الحاسبة المتقدمة لمساحات الأراضي</h1>', unsafe_allow_html=True)
        try:
            insrf_main()
        except Exception as e:
            st.error(f"حدث خطأ في تحميل تطبيق حساب المساحات: {e}")

    elif app_choice == "📐 تحليل الزوايا والمنحدرات (tan)":
        st.markdown('<h1 class="main-header">📐 تطبيق تحليل الزوايا والمنحدرات</h1>', unsafe_allow_html=True)
        try:
            tan_main()
        except Exception as e:
            st.error(f"حدث خطأ في تحميل تطبيق tan: {e}")

    elif app_choice == "📊 التحليل البُعدي (dimshnal)":
        st.markdown('<h1 class="main-header">📊 تطبيق التحليل البُعدي</h1>', unsafe_allow_html=True)
        try:
            demasinal_main()
        except Exception as e:
            st.error(f"حدث خطأ في تحميل تطبيق dimshnal: {e}")

if __name__ == "__main__":
    main()