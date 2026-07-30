#!/bin/bash

# سكريبت رفع التصاميم تلقائياً إلى جيت هاب (GitHub Upload Script)
# لبراند ملابس ستريت وير الخاص بك

echo -e "\e[1;35m====================================================\e[0m"
echo -e "\e[1;36m    🚀 سكريبت الرفع التلقائي إلى مستودع GitHub 🚀     \e[0m"
echo -e "\e[1;35m====================================================\e[0m"
echo ""

# التأكد من إعدادات Git المحلية الافتراضية
git config --global user.name "Streetwear Store" 2>/dev/null
git config --global user.email "store@streetwear.com" 2>/dev/null

# طلب البيانات من المستخدم
read -p "📌 أدخل اسم حسابك على GitHub (Username): " GH_USER
if [ -z "$GH_USER" ]; then
    echo -e "\e[1;31m❌ خطأ: اسم المستخدم مطلوب.\e[0m"
    exit 1
fi

read -p "📌 أدخل اسم المستودع (Repository Name): " GH_REPO
if [ -z "$GH_REPO" ]; then
    echo -e "\e[1;31m❌ خطأ: اسم المستودع مطلوب.\e[0m"
    exit 1
fi

read -sp "📌 أدخل رمز الوصول الخاص بك (GitHub Personal Access Token - PAT): " GH_TOKEN
echo ""
if [ -z "$GH_TOKEN" ]; then
    echo -e "\e[1;31m❌ خطأ: رمز الوصول مطلوب للرفع الآمن.\e[0m"
    exit 1
fi

echo ""
echo -e "\e[1;33m🔄 جاري تهيئة مستودع Git المحلي...\e[0m"

# تهيئة Git إذا لم يكن مهيئاً من قبل
if [ ! -d ".git" ]; then
    git init
    git checkout -b main
else
    echo "✅ مستودع Git مهيأ بالفعل."
fi

# إضافة جميع الملفات (التصاميم والرموز)
git add README.md bg_remover.py TSH-* 2>/dev/null

# تسجيل التغييرات
git commit -m "Add/Update products & streetwear designs folders" 2>/dev/null || echo "لا توجد تغييرات جديدة للتسجيل."

# إعداد الرابط البعيد بأمان باستخدام التوكن
REMOTE_URL="https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git"

# إزالة الرابط القديم إن وجد وإضافة الرابط الجديد
git remote remove origin 2>/dev/null
git remote add origin "$REMOTE_URL"

echo -e "\e[1;33m📦 جاري دفع الملفات إلى GitHub...\e[0m"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "\e[1;32m====================================================\e[0m"
    echo -e "\e[1;32m🎉 تم رفع جميع التصاميم بنجاح إلى حسابك على GitHub! 🎉\e[0m"
    echo -e "\e[1;34m🔗 رابط المستودع: https://github.com/${GH_USER}/${GH_REPO}\e[0m"
    echo -e "\e[1;32m====================================================\e[0m"
else
    echo ""
    echo -e "\e[1;31m❌ حدث خطأ أثناء الرفع. تأكد من:\e[0m"
    echo "1. أنك قمت بإنشاء المستودع ($GH_REPO) على حسابك في GitHub أولاً."
    echo "2. أن الـ Personal Access Token (PAT) لديه صلاحيات 'repo' أو 'write'."
    echo "3. صحة اسم المستخدم واسم المستودع."
fi
