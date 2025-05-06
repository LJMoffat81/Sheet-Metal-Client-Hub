#!/bin/bash
# Verification script for Sheet Metal Client Hub repository
echo "=== Repository Verification Report ==="
echo "Date: $(date)"
echo ""

# Check current directory
echo "1. Current Directory:"
pwd
echo ""

# Check Git status
echo "2. Git Status:"
git status
echo ""

# Check remote configuration
echo "3. Remote Configuration:"
git remote -v
echo ""

# Check sync with GitHub (commit history)
echo "4. Sync with GitHub (Recent Commits):"
git fetch origin
git log --oneline -n 5
echo "Run 'git log --oneline' to see full history if needed."
echo ""

# Check file structure
echo "5. File Structure:"
echo "Root:"
ls -la
echo "docs/:"
ls -la docs/
echo "docs/diagrams/:"
ls -la docs/diagrams/
echo "src/:"
ls -la src/
echo "src/tests/:"
ls -la src/tests/
echo "data/:"
ls -la data/
echo ""

# Check backups
echo "6. Backups:"
ls -la "/c/Users/Laurie/Proton Drive/tartant/My files/Backups"
echo ""

# Summary
echo "=== Summary ==="
echo "If the following are true, the repository is OK:"
echo "- Git Status shows 'Your branch is up to date with origin/main' and 'nothing to commit'."
echo "- Remote is set to 'https://github.com/LJMoffat81/Sheet-Metal-Client-Hub.git' or token-authenticated URL."
echo "- File structure matches expected list (see Step 1 in guide)."
echo "- Recent commits align with GitHub's history."
echo "- Backups exist (e.g., Sheet-Metal-Client-Hub-20250506)."
echo ""
echo "Review the output above. If any issues are found (e.g., uncommitted changes, missing files, authentication errors), reply with the output for assistance."
echo "If all looks good, reply with 'All is OK' to proceed with Git Bash uninstall/reinstall."

