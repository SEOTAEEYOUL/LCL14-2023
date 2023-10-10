# Git


## git commit 취소하기
- 완료한 commit 취소하기
  - 너무 일찍 commit 한 경우
  - 어떤 파일을 빼 먹고 commit 한 경우, 이때 `git reset HEAD^` 명령을 통해 git commit 를 취소할 수 있다.
#### commit 목록 확인
```
git log
```
#### commit 취소하기
```
git reset HEAD^
git reset --hard HEAD^
```

#### commit을 취소하고 해당 파일들은 staged 상태로 워킹 디렉터리에 보존
```
git reset --soft HEAD^
```

#### commit을 취소하고 해당 파일들은 unstaged 상태로 워킹 디렉터리에 보존
```
git reset HEAD^
```

#### 마지막 2개의 commit 취소 
```
git reset HEAD~2
```

#### commit 를 취소하고 해당 파일들은 unstaged 상태로 워킹 디렉토리에서 삭제
```
git reset --hard HEAD^
```

## Branch
```
PS > git branch
* main
PS > git checkout -b cost_optimizing
Switched to a new branch 'cost_optimizing'
PS > git branch
* cost_optimizing
  main
PS > 
PS > git add .
PS > git commit -m "20230825"       
[cost_optimizing 7310b3a] 20230825
 2 files changed, 44 insertions(+), 37 deletions(-)
 create mode 100644 "03.\354\232\264\354\230\201\354\236\220\353\243\214/DataDog/Python/230825_datadog_alert_report.xlsx"
PS > git push
fatal: The current branch cost_optimizing has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin cost_optimizing

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

PS > git push --set-upstream origin cost_optimizing
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 16 threads
Compressing objects: 100% (7/7), done.
Writing objects: 100% (7/7), 64.00 KiB | 10.67 MiB/s, done.
Total 7 (delta 5), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (5/5), completed with 5 local objects.
remote: 
remote: Create a pull request for 'cost_optimizing' on GitHub by visiting:
remote:      https://github.com/SEOTAEEYOUL/LCL-14/pull/new/cost_optimizing
remote:
To https://github.com/SEOTAEEYOUL/LCL-14.git
 * [new branch]      cost_optimizing -> cost_optimizing
branch 'cost_optimizing' set up to track 'origin/cost_optimizing'.
PS > 
```