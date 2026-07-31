#!/bin/bash

# سكريبت الرفع الآمن وتوفير المساحة للأبد (Safe Push & Clean Script)
# DISTRICT-99 (D99)

COMMIT_MSG=$1
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update district-99 premium brand files"
fi

# Read token safely from the ignored local file
if [ -f "/home/user/.git_token" ]; then
    GH_TOKEN=$(cat /home/user/.git_token | xargs)
else
    echo "❌ Error: .git_token file not found."
    exit 1
fi

echo "🔄 Initializing temporary shallow Git..."
git init 2>/dev/null
git config user.name "mohaamedabdelhady007-del" 2>/dev/null
git config user.email "mohaamedabdelhady007-del@users.noreply.github.com" 2>/dev/null

# Clean up remote and add with token
git remote add origin "https://mohaamedabdelhady007-del:${GH_TOKEN}@github.com/mohaamedabdelhady007-del/workspace-019fb551-ba6f-7b33-8e5d-c6cb5af69f5f.git" 2>/dev/null

echo "📥 Fetching shallow history from GitHub..."
git fetch origin main --depth=1 2>/dev/null

echo "🔄 Resetting index..."
git reset --mixed origin/main 2>/dev/null

echo "➕ Staging all workspace changes..."
git add -A 2>/dev/null

echo "📝 Committing changes..."
git commit -m "$COMMIT_MSG" 2>/dev/null

echo "📤 Pushing to GitHub..."
git branch -m main 2>/dev/null
git push origin main -f 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed all changes to GitHub!"
else
    echo "❌ Failed to push changes."
fi

# THE MAGIC TRICK: Delete .git folder from the container to free up 85 MB instantly!
echo "🧼 Cleaning up temporary Git cache to free up 100% space..."
rm -rf /home/user/.git

echo "📉 Space check:"
du -sh /home/user/*
