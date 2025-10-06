# Reset Branch Template

**Configuration Parameters:**
- `[DEFAULT_BRANCH]` - The default branch to reset to (e.g., "main", "master", "develop")

This command resets the current branch by deleting all commits and reverting back to the head of [DEFAULT_BRANCH].

## Usage
```
/reset-branch
```

## What it does
1. Fetches the latest [DEFAULT_BRANCH] branch from origin
2. Resets the current branch to match [DEFAULT_BRANCH] exactly
3. Discards all local changes and commits
4. Force pushes to update the remote branch (if it exists)

## Warning
⚠️ This is a destructive operation that will:
- Delete ALL commits on the current branch
- Remove ALL uncommitted changes
- Overwrite the remote branch if you force push

Make sure you really want to discard all work on this branch before proceeding.

## Implementation

```bash
#!/bin/bash

# Get current branch name
current_branch=$(git branch --show-current)

# Safety check - don't reset [DEFAULT_BRANCH] branch
if [ "$current_branch" = "[DEFAULT_BRANCH]" ]; then
    echo "❌ Cannot reset the [DEFAULT_BRANCH] branch!"
    exit 1
fi

echo "⚠️  WARNING: This will delete ALL commits and changes on branch '$current_branch'"
echo "Are you sure you want to reset to [DEFAULT_BRANCH]? (yes/no)"
read -r confirmation

if [ "$confirmation" != "yes" ]; then
    echo "❌ Reset cancelled"
    exit 0
fi

echo "🔄 Fetching latest [DEFAULT_BRANCH]..."
git fetch origin [DEFAULT_BRANCH]

echo "🔀 Resetting branch to origin/[DEFAULT_BRANCH]..."
git reset --hard origin/[DEFAULT_BRANCH]

echo "✅ Local branch reset to [DEFAULT_BRANCH]"

echo "Do you want to force push to update the remote branch? (yes/no)"
read -r push_confirmation

if [ "$push_confirmation" = "yes" ]; then
    echo "🚀 Force pushing to origin..."
    git push --force-with-lease origin "$current_branch"
    echo "✅ Remote branch updated"
else
    echo "ℹ️  Remote branch not updated. Use 'git push --force-with-lease' when ready."
fi

echo "✨ Branch '$current_branch' has been reset to [DEFAULT_BRANCH]"
```