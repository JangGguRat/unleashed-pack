# UNLEASHED 모드팩 (관리자용 안내)

모드를 고칠 때마다 `update.bat` 를 더블클릭하면 끝입니다.
친구들은 게임을 켤 때마다 바뀐 모드만 자동으로 받고, 곧바로 서버에 접속합니다.

```
내 PC                          GitHub                         친구 PC (Prism Launcher)
update.bat ──push──▶ Actions: index 생성 + Pages 배포 ──▶ 게임 실행 → 자동 업데이트 → 서버 접속
```

---

## 처음 한 번만 하는 설정

### 1. GitHub 저장소 만들기
1. GitHub에서 새 저장소를 만듭니다. 예: `unleashed-pack`
   - **Public** 으로 만들어야 GitHub Pages가 무료입니다. 모드 jar가 공개된다는 점은 알아두세요.
2. 이 폴더 전체를 그 저장소에 올립니다. 기본 브랜치 이름은 `main` 이어야 합니다.
   ```
   git init -b main
   git remote add origin https://github.com/<내아이디>/unleashed-pack.git
   git add -A
   git commit -m "init"
   git push -u origin main
   ```
3. 저장소의 **Settings → Pages → Build and deployment → Source** 를 **GitHub Actions** 로 바꿉니다.
4. **Actions** 탭에서 `Deploy modpack` 이 초록색으로 끝나는지 확인합니다.
   실패했다면 Actions 탭에서 `Run workflow` 를 한 번 눌러 주세요. 3번 설정 전에 push하면 첫 실행이 실패합니다.
5. `https://<내아이디>.github.io/unleashed-pack/` 에 들어가서 안내 페이지가 보이면 성공입니다.

### 2. 서버 주소 넣기: `tools/instance.json`
```json
"server_address": "내서버주소:25565"
```
이 값을 넣으면 친구가 게임을 켜자마자 서버로 바로 들어갑니다.
포트가 25565면 `:25565` 는 생략해도 됩니다.

### 3. 내 모드 프로젝트 등록: `tools/mod-projects.txt`
```
unleashed-combat|C:\Users\me\IdeaProjects\unleashed-combat
animstudio|C:\Users\me\IdeaProjects\animstudio
```
- 왼쪽은 모드팩 안에서 쓸 파일 이름이고, `mods\unleashed-combat.jar` 처럼 들어갑니다.
- 오른쪽은 Gradle 프로젝트 폴더입니다. `gradlew.bat` 가 있는 폴더를 적으면 됩니다.

### 4. (선택) `update.bat` 위쪽 설정
- `SERVER_MODS` 에 서버 mods 폴더 경로를 넣으면 서버에도 같은 jar가 같이 복사됩니다.
  - 처음 한 번은 서버 mods 폴더에 있던 **버전 번호가 붙은 옛 jar를 직접 지워 주세요.**
    예를 들어 `unleashed-combat-1.0.0.jar` 같은 파일이 남아 있으면 같은 모드가 두 개 로드됩니다.
- `BUILD=0` 으로 두면 빌드는 건너뛰고, 이미 빌드된 jar만 복사합니다.

---

## 평소 업데이트 방법
1. 모드 코드를 고칩니다.
2. `update.bat` 를 더블클릭합니다. 빌드, 복사, push가 자동으로 진행됩니다.
3. 1~2분 정도 기다리면 배포가 끝납니다. Actions 탭에서 진행 상황을 볼 수 있습니다.
4. 친구들은 그냥 게임을 다시 켜기만 하면 됩니다.

> 게임이 켜져 있는 동안에는 업데이트가 반영되지 않습니다. 업데이트는 **게임을 실행할 때** 확인합니다.

---

## 그 밖의 작업

| 하고 싶은 것 | 방법 |
|---|---|
| 다른 사람이 만든 모드 추가 (Sodium 등) | jar 파일을 `mods\` 폴더에 넣고 `update.bat` 실행 |
| 모드 설정 파일 배포 | `config\` 폴더를 만들어 넣으면 친구 쪽 `config\` 에도 똑같이 들어감 |
| 리소스팩 배포 | `resourcepacks\` 폴더에 넣기 |
| 모드 삭제 | `mods\` 에서 지우고 `update.bat` 실행하면 친구 쪽에서도 지워짐 |
| Fabric API 버전 올리기 | `mods\fabric-api.pw.toml` 을 지우고 새 Fabric API jar를 `mods\` 에 넣기 |
| Minecraft / Fabric Loader 버전 변경 | `pack.toml` 의 `[versions]` 수정. 이건 친구들이 인스턴스를 **새로 가져와야** 반영됨 |

- `index.toml` 은 GitHub Actions가 자동으로 만들기 때문에 직접 고칠 필요가 없습니다.
  로컬에서 확인하고 싶다면 `python tools/refresh.py` 를 실행하면 됩니다.
- 원래의 [packwiz](https://packwiz.infra.link) CLI도 그대로 쓸 수 있습니다. 같은 포맷이라 호환됩니다.

---

## 친구에게 보낼 것
주소 하나만 보내면 됩니다.
```
https://<내아이디>.github.io/unleashed-pack/UNLEASHED.zip
```
설치 방법은 친구용 가이드 문서를 같이 보내 주세요.
