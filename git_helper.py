#!/usr/bin/env python3
"""
Git automation script for ML projects
Simplifies common Git operations with ML-specific features
"""

import subprocess
import sys
import os
from datetime import datetime
import argparse


def run_git_command(command, description=""):
    """Run a git command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        if description:
            print(f"✅ {description}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return None


def check_git_status():
    """Check if we're in a git repository and show status."""
    if not os.path.exists('.git'):
        print("❌ Not in a Git repository. Run 'git init' first.")
        return False
    
    status = run_git_command("git status --porcelain")
    if status:
        print("📋 Current changes:")
        lines = status.split('\n')
        for line in lines[:10]:  # Show first 10 changes
            print(f"   {line}")
        if len(lines) > 10:
            print(f"   ... and {len(lines) - 10} more files")
        return True
    else:
        print("✅ Working directory clean")
        return False


def ml_commit(message, commit_type="feat"):
    """Create a commit with ML-specific formatting."""
    # Type emojis for ML projects
    type_emojis = {
        "data": "📊",
        "model": "🤖", 
        "feat": "🔧",
        "fix": "🐛",
        "docs": "📝",
        "test": "✅",
        "refactor": "♻️",
        "perf": "⚡",
        "style": "🎨",
        "experiment": "🧪",
        "analysis": "📈"
    }
    
    emoji = type_emojis.get(commit_type, "🔧")
    formatted_message = f"{emoji} {commit_type}: {message}"
    
    # Stage all changes
    run_git_command("git add .", "Staging all changes")
    
    # Create commit
    if run_git_command(f'git commit -m "{formatted_message}"', "Creating commit"):
        print(f"📝 Committed: {formatted_message}")
        return True
    return False


def quick_push(branch=None):
    """Quick push to remote repository."""
    if not branch:
        # Get current branch
        branch = run_git_command("git branch --show-current")
    
    if branch:
        result = run_git_command(f"git push -u origin {branch}", 
                               f"Pushing {branch} to remote")
        return result is not None
    return False


def create_ml_branch(branch_name, branch_type="feature"):
    """Create a new branch with ML naming convention."""
    full_branch_name = f"{branch_type}/{branch_name}"
    
    if run_git_command(f"git checkout -b {full_branch_name}", 
                      f"Creating branch {full_branch_name}"):
        print(f"🌿 Switched to new branch: {full_branch_name}")
        return full_branch_name
    return None


def daily_commit():
    """Interactive daily commit workflow."""
    print("🌅 Daily ML Progress Commit")
    print("=" * 40)
    
    # Check status
    has_changes = check_git_status()
    if not has_changes:
        print("No changes to commit today.")
        return
    
    # Get commit details
    print("\n📝 Describe today's work:")
    message = input("Commit message: ")
    
    print("\n🏷️  What type of work did you do?")
    print("1. data - Data exploration/preprocessing")
    print("2. model - Model development/training") 
    print("3. experiment - Experimental work")
    print("4. analysis - Data analysis/visualization")
    print("5. feat - New features/functionality")
    print("6. docs - Documentation")
    print("7. fix - Bug fixes")
    
    choice = input("Choose (1-7): ").strip()
    type_map = {
        "1": "data", "2": "model", "3": "experiment", 
        "4": "analysis", "5": "feat", "6": "docs", "7": "fix"
    }
    commit_type = type_map.get(choice, "feat")
    
    # Create commit
    if ml_commit(message, commit_type):
        # Ask about pushing
        push = input("\n🚀 Push to GitHub? (y/n): ").lower().startswith('y')
        if push:
            quick_push()
    
    print("\n🎉 Daily commit complete! Keep up the great work!")


def project_setup():
    """Set up Git for a new ML project."""
    print("🚀 Setting up Git for ML project")
    print("=" * 40)
    
    # Initialize git if needed
    if not os.path.exists('.git'):
        run_git_command("git init", "Initializing Git repository")
        run_git_command("git branch -M main", "Setting default branch to main")
    
    # Check for .gitignore
    if not os.path.exists('.gitignore'):
        print("⚠️  No .gitignore found. Please create one for ML projects.")
    
    # Create initial commit if no commits exist
    try:
        run_git_command("git rev-parse HEAD", "")
    except:
        print("📝 Creating initial commit...")
        if ml_commit("Initial project setup", "feat"):
            print("✅ Initial commit created")
    
    # Get remote repository URL
    remote_url = input("\n🔗 GitHub repository URL (optional): ").strip()
    if remote_url:
        run_git_command(f"git remote add origin {remote_url}", 
                       "Adding remote repository")
        
        push = input("🚀 Push to GitHub now? (y/n): ").lower().startswith('y')
        if push:
            quick_push("main")
    
    print("\n✅ Git setup complete!")


def weekly_summary():
    """Create a weekly summary commit and tag."""
    print("📅 Weekly Summary")
    print("=" * 40)
    
    # Get this week's commits
    week_ago = datetime.now().strftime("%Y-%m-%d")
    commits = run_git_command(f"git log --since='1 week ago' --oneline")
    
    if commits:
        print(f"📊 This week's commits:")
        for line in commits.split('\n')[:10]:
            print(f"   {line}")
    
    # Create weekly tag
    week_num = input("\nWeek number (e.g., 1, 2, 3): ").strip()
    if week_num:
        tag_name = f"week-{week_num}"
        summary = input("Weekly summary: ")
        
        tag_message = f"📅 Week {week_num} Complete: {summary}"
        run_git_command(f'git tag -a {tag_name} -m "{tag_message}"', 
                       f"Creating tag {tag_name}")
        
        # Push tag
        run_git_command("git push --tags", "Pushing tags to remote")
        print(f"🏷️  Week {week_num} tagged and pushed!")


def clean_notebooks():
    """Clear notebook outputs before committing."""
    print("🧹 Cleaning notebook outputs...")
    
    # Find all notebook files
    notebooks = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.ipynb'):
                notebooks.append(os.path.join(root, file))
    
    if not notebooks:
        print("No notebooks found.")
        return
    
    # Try to use nbstripout if available
    try:
        for notebook in notebooks:
            result = subprocess.run(['nbstripout', notebook], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Cleaned {notebook}")
            else:
                print(f"⚠️  Could not clean {notebook}")
    except FileNotFoundError:
        print("📦 nbstripout not found. Install with: pip install nbstripout")
        print("Alternatively, manually clear outputs in Jupyter before committing.")


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(description="Git automation for ML projects")
    parser.add_argument('action', choices=[
        'status', 'daily', 'setup', 'weekly', 'clean', 'commit', 'push'
    ], help='Action to perform')
    
    parser.add_argument('--message', '-m', help='Commit message')
    parser.add_argument('--type', '-t', default='feat', 
                       choices=['data', 'model', 'feat', 'fix', 'docs', 'test', 
                               'refactor', 'perf', 'style', 'experiment', 'analysis'],
                       help='Type of commit')
    parser.add_argument('--branch', '-b', help='Branch name')
    
    args = parser.parse_args()
    
    if args.action == 'status':
        check_git_status()
    
    elif args.action == 'daily':
        daily_commit()
    
    elif args.action == 'setup':
        project_setup()
    
    elif args.action == 'weekly':
        weekly_summary()
    
    elif args.action == 'clean':
        clean_notebooks()
    
    elif args.action == 'commit':
        if not args.message:
            args.message = input("Commit message: ")
        ml_commit(args.message, args.type)
    
    elif args.action == 'push':
        quick_push(args.branch)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Interactive mode
        print("🤖 ML Git Assistant")
        print("=" * 30)
        print("1. Check status")
        print("2. Daily commit")
        print("3. Setup project")
        print("4. Weekly summary")
        print("5. Clean notebooks")
        
        choice = input("\nChoose an action (1-5): ").strip()
        actions = {
            '1': lambda: check_git_status(),
            '2': lambda: daily_commit(),
            '3': lambda: project_setup(),
            '4': lambda: weekly_summary(),
            '5': lambda: clean_notebooks()
        }
        
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice")
    else:
        main()
