import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai

# إعداد واجهة الشاشة الواحدة والتصميم المالي
st.set_page_config(page_title="مستشارك المالي", page_icon="📊", layout="centered")

# عنوان التطبيق الشامل الذي سيظهر باللغة العربية
st.title("📊 مستشارك المالي الذكي")
st.caption("تحليل مالي، دراسات جدوى، وقراءة ملفات الإكسل والصور مجاناً بالكامل")

# إعداد مفتاح الذكاء الاصطناعي المجاني من جوجل (الخطة المجانية للأبد)
# يمكنك الحصول على مفتاحك الخاص مجاناً من Google AI Studio ووضعه هنا
API_KEY = "AIzaSy..." 
genai.configure(api_key=API_KEY)

# 1. قسم رفع الملفات المشترك (إكسل، صور قوائم مالية، أو PDF)
uploaded_file = st.file_uploader(
    "📎 ارفع ملف الإكسل للبيانات أو صورة القائمة المالية/الجدول هنا:", 
    type=["xlsx", "csv", "png", "jpg", "jpeg"]
)

excel_data_str = ""
uploaded_image = None

if uploaded_file is not None:
    # التحقق إذا كان الملف إكسل أو جدول بيانات
    if uploaded_file.name.endswith(('.xlsx', '.csv')):
        try:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
            st.success("📈 تم تحميل ملف البيانات بنجاح!")
            with st.expander("👀 عرض عينة من بيانات الملف"):
                st.dataframe(df.head(10))
            # تحويل البيانات لنص ليقرأها الذكاء الاصطناعي ويحللها
            excel_data_str = df.to_string()
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة ملف الإكسل: {e}")
            
    # التحقق إذا كان الملف صورة (لقائمة مالية أو دراسة ورقية)
    else:
        try:
            uploaded_image = Image.open(uploaded_file)
            st.success("📸 تم تحميل صورة القائمة المالية بنجاح!")
            with st.expander("👀 عرض الصورة المرفوعة"):
                st.image(uploaded_image, caption="القائمة المالية المرفوعة", use_container_width=True)
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الصورة: {e}")

# 2. مربع النص الموحد لكتابة الأوامر والأسئلة الحرّة
user_query = st.text_area(
    "✍️ اكتب سؤالك أو فكرة مشروعك للمستشار المالي:", 
    placeholder="مثال: هل هذا المشروع مجدٍ؟ أو استخرج لي نسب السيولة والربحية من الملف المرفق وحللها..."
)

# 3. زر تشغيل المستشار الذكي والتحليل المالي في نفس الشاشة
if st.button("🚀 ابدأ التحليل المالي الذكي الآن"):
    if not user_query and uploaded_file is None:
        st.warning("الرجاء رفع ملف أو كتابة سؤال أولاً ليتمكن المستشار من مساعدتك.")
    else:
        with st.spinner("🔄 جاري معالجة البيانات وتحضير التقارير المالية من المستشار الذكي..."):
            try:
                # تجهيز سياق الأمر للذكاء الاصطناعي ليعمل كمستشار مالي خبير
                system_prompt = "أنت مستشار مالي خبير ومحترف في دراسات الجدوى والتحليل المالي للقوائم والميزانيات العمومية. قم بالإجابة على طلب المستخدم بدقة وااحترافية وبناء الرسوم والتوصيات بناء على البيانات المتاحة.\n\n"
                
                # استخدام نموذج Gemini الشامل لقراءة النصوص والصور
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                content_inputs = [system_prompt]
                
                # إذا كان هناك بيانات إكسل ممررة
                if excel_data_str:
                    content_inputs.append(f"بيانات الجدول المالي المرفق:\n{excel_data_str}\n\n")
                
                # إذا كانت هناك صورة مرفوعة لقائمة مالية
                if uploaded_image:
                    content_inputs.append(uploaded_image)
                    content_inputs.append("قم بتحليل الأرقام والقوائم المالية الموجودة في هذه الصورة بدقة.\n")
                
                # إضافة سؤال المستخدم
                content_inputs.append(f"سؤال المستخدم أو فكرة المشروع: {user_query}")
                
                # إرسال البيانات للنموذج واستقبال التحليل المالي مجاناً
                response = model.generate_content(content_inputs)
                
                # عرض النتيجة النهائية في نفس الواجهة الشاملة
                st.markdown("---")
                st.subheader("📝 التقرير والتحليل المالي الصادر:")
                st.write(response.text)
                st.balloons()
                
            except Exception as e:
                st.error(f"عذراً، واجه المستشار المالي مشكلة أثناء التحليل: {e}")
