# 🛠️ DISTRICT-99 (D99) - PROPOSED THEME MODIFICATIONS

يا باشا، الله ينور عليك! السكرينات دي وضحت كل حاجة بالملّي وملاحظاتك في قمة الذكاء والدقة. 

إليك التحليل التقني لكل نقطة، والتعديلات المقترحة لبرمجة وتصميم الثيم بالملّي قبل ما نرفع أي كود على الموقع الحي (تمهيداً لموافقتك):

---

## 📸 1. موضوع الصور و "No Image" (هل هي غلطة؟)

**الإجابة السريعة:** لا يا غالي، دي مش غلطة خالص، وده هو التصميم القياسي والاحترافي لثيمات شوبيفاي الحديثة (Online Store 2.0)!

### 💡 التفسير التقني:
إحنا برمجنا قسم **D99 Split Hero** وقسم **D99 Bento Lookbook** كأقسام ديناميكية بالكامل باستخدام الـ `image_picker` في لغة Liquid. 
* لما بيترفع القسم لأول مرة، بيظهر بشكل افتراضي بعبارة **"No Image"** كحيز فارغ (Placeholder).
* **طريقة وضع الصور (سهلة جداً في ثانيتين):**
  1. ادخل على الـ **Shopify Customizer** (الصفحة المفتوحة عندك في السكرين).
  2. اضغط من القائمة الجانبية اليسرى على قسم `D99 Split Hero` أو `D99 Bento Lookbook`.
  3. هتتفتح لك لوحة تحكم في اليمين تحتوي على خيار **"Select Image"** لكل لوحة!
  4. اضغط عليها واختار أي صورة تيشيرت أو موديل من مكتبة موقعك، وهتظهر فوراً بمقاس مثالي!

هذا الأسلوب بيعطيك **تحكم كامل 100%** لتغيير صور اللوك بوك والبانر في المستقبل بضغطة زر مع كل دروب جديد، بدون ما تحتاج تعدل سطر كود واحد!

---

## 🛑 2. تعديلbreakpoints الـ Bento Lookbook (حل مشكلة التكديس الرأسي)

في السكرين شوت الثاني، ظهرت مشكلة إن لوحات الـ Bento Lookbook متكدسة فوق بعضها رأسياً كعمود واحد في الـ Customizer.

### 🐛 سبب المشكلة:
الـ Breakpoint الافتراضي للموبايل كان مضبوط على `768px`. وبما إن نافذة محرّر شوبيفاي (Shopify Editor) بتشغل مساحة كبيرة من الشاشة وبتصغر حجم المعاينة (Iframe Viewport) لأقل من `768px`؛ محرّر شوبيفاي افتكر إننا فاتحين من موبايل، فقام بتفعيل تصميم الموبايل وعرض الصور رأسياً!

### 🛠️ التعديل المقترح لـ `sections/d99-lookbook-grid.liquid`:
هنقوم بتقليل الـ Breakpoint الخاص بالموبايل ليكون `600px` بدلاً من `768px`؛ وهنخلي الشاشات المتوسطة (بين 600px و 1024px - مثل شاشة المحرر عندك) تظهر كـ **شبكة ثنائية الأعمدة (2 Columns Grid)** بدلاً من التكديس الرأسي.

**كود الـ CSS المقترح للتعديل:**
```css
  /* شبكة الـ Bento الأساسية للديسكتوب (4 أعمدة) */
  .d99-bento-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(280px, auto);
    gap: 30px;
    width: 100%;
  }

  /* للشاشات المتوسطة ومُحرر شوبيفاي (عمودين بدلاً من التكديس) */
  @media screen and (max-width: 1024px) {
    .d99-bento-grid {
      grid-template-columns: repeat(2, 1fr) !important;
      grid-auto-rows: minmax(220px, auto) !important;
      gap: 20px !important;
    }
  }

  /* للموبايل الحقيقي فقط (تكديس رأسي مريح) */
  @media screen and (max-width: 600px) {
    .d99-bento-grid {
      display: flex !important;
      flex-direction: column !important;
      gap: 20px !important;
    }
  }
```

---

## 🗑️ 3. حذف قسم الـ Featured Collection من الصفحة الرئيسية

بناءً على طلبك، سنقوم بمسح قسم الـ Featured Collection (الذي يعرض المنتجات بشكل تقليدي) نهائياً من الصفحة الرئيسية ليكون الموقع نظيفاً وإيديتوريال بالكامل.

### 🛠️ التعديل المقترح لملف `templates/index.json`:
سنقوم بإزالة الـ `featured_products` من قائمة الأقسام والترتيب، ليصبح الهيكل كالتالي:

```json
{
  "sections": {
    "d99_marquee_ticker": {
      "type": "d99-marquee-ticker",
      "settings": {
        "marquee_text": "DISTRICT-99 // ACTION IS THE BRIDGE // FREE SHIPPING NATIONWIDE //"
      }
    },
    "d99_split_hero": {
      "type": "d99-split-hero",
      "settings": {
        "title_left": "New Arrivals",
        "btn_label_left": "COP NOW",
        "title_right": "The Lookbook",
        "btn_label_right": "Explore"
      }
    },
    "d99_lookbook_grid": {
      "type": "d99-lookbook-grid",
      "settings": {
        "heading": "Define Your District"
      }
    }
  },
  "order": [
    "d99_marquee_ticker",
    "d99_split_hero",
    "d99_lookbook_grid"
  ]
}
```

---

### 💬 مستني قرارك يا باشا!
راجع التعديلات دي، وبمجرد ما تقولي **"دوس"** أو تعدل أي حاجة ببالك، هقوم برفع الكود فوراً ومزامنته بمتجرك لتشاهد التحديث الخرافي بنفسك! 🚀🔥
