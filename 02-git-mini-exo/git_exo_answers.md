# Git mini exo: commands and answers

## Part 1: Setup & config

```bash
git --version
git config --global user.name "Virgile"
git config --global user.email "virgile.durand@essec.edu"
```

## Part 2: Create your first repository

```bash
mkdir my-first-repo
cd my-first-repo
git init
touch readme.txt
```

## Part 3: Your first commit

1. Current state: `git status`
2. Stage file: `git add readme.txt`
3. Commit: `git commit -m "Add readme file"`
4. History: `git log`

## Part 4: Make changes

```bash
echo "Hello Mr Dallard" >> readme.txt
git status
git add readme.txt
git commit -m "Update readme"
```

- **What `git status` shows:** It displays `readme.txt` in red as modified, meaning Git detects the change in the folder, but it is not staged for commit yet.
- **Number of commits now:** 2 commits.

## Part 5: Exploration

- `git diff`: Shows the exact lines added or removed in files that haven't been staged yet.
- `git log --oneline`: Shows the commit history in a compact format (one commit per line with its short ID and message).

## Part 6: Working with branches

1. List branches: `git branch`
2. Create `feature-script`: `git branch feature-script`
3. Switch to `feature-script`: `git checkout feature-script`
4. Create and switch to `dev` in one command: `git checkout -b dev`
5. Switch back to `feature-script`: `git checkout feature-script`
6. Verify current branch: `git branch` (the active branch has a `*` next to it)

## Part 7: Create a bash script on a branch

```bash
git checkout feature-script
nano install.sh
```

Content of `install.sh`:

```bash
#!/usr/bin/env bash
echo "Starting installation..."
sudo apt update
sudo apt install -y curl
echo "Installation complete!"
```

Make executable, commit and check log:

```
chmod +x install.sh
git add install.sh
git commit -m "Add install script"
git log
```

## Part 8: Merge branches

1. Switch back to `main`: `git checkout main`
2. **Is `install.sh` present?** No, because branches are separate. Changes made on `feature-script` stay on that branch until they are merged into `main`.
3. Merge `feature-script` into `main`: `git merge feature-script`
4. **List files again (`ls`):** `install.sh` is now in the `main` folder.
5. **Commit history (`git log`):** The `"Add install script"` commit from `feature-script` now appears in `main`'s history.
6. Delete branch after merging: `git branch -d feature-script`

## Part 9: Push to GitHub

```
git remote add origin https://github.com/virgdrnd/my-first-repo.git
git push -u origin main
```

- **After refreshing GitHub:** Both `readme.txt` and `install.sh` are visible on GitHub with the commit history.

## Part 10: Delete and clone

```
cd ..
rm -rf my-first-repo
git clone [https://github.com/virgdrnd/my-first-repo.git](https://github.com/virgdrnd/my-first-repo.git)
cd my-first-repo
ls
```

## Part 11: Full workflow practice

```bash
cd ..
rm -rf my-first-repo
mkdir bash-installer
cd bash-installer
git init
echo "# Bash Installer" > README.md
git add README.md
git commit -m "Add README"
git checkout -b feature-install
cp ../env_install.sh .
git add env_install.sh
git commit -m "Add install script"
git checkout main
git merge feature-install
git branch -d feature-install
git remote add origin https://github.com/virgdrnd/bash-installer.git
git push -u origin main
```

## Reflection questions

1. **Why is version control useful?**
   It keeps a full history of changes, lets you go back to an older version if you break something, and makes working with other people much easier.
2. **What is the difference between staging and committing?**
   Staging (`git add`) chooses which modified files you want to include in the next save. Committing (`git commit`) actually saves that snapshot into the history.
3. **When should you make a commit?**
   Every time you finish a small, working piece of code (like adding a function or fixing a bug), so it is easy to track what changed.
4. **What is the difference between `git init` and `git clone`?**
   `git init` creates a new empty Git repository on your computer, while `git clone` downloads an existing repository from GitHub with all its files and history.
5. **Why should you write good commit messages?**
   To quickly understand what each commit changed without having to read all the code again.
6. **What is the purpose of using branches?**
   Branches let you work on new features or tests safely without breaking the main working code.
7. **When would you create a new branch instead of working on `main`?**
   Whenever you start working on a new feature, a bug fix, or an experiment, so `main` always stays clean and working.
