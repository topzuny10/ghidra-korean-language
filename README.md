# ghidra-ko

NSA Ghidra의 **비공식 한국어 부분 번역 스타터**입니다. 완전한 한글판이나 설치형 확장 플러그인이 아닙니다. Ghidra 소스에 작은 패치를 적용하고 직접 빌드합니다. 공식 바이너리의 JAR를 덮어쓰지 않습니다.

## 현재 범위와 검증 상태

2026-10-21 공식 GitHub 릴리스 API에서 확인한 최신 안정판은 **12.1.4**입니다.
기준 태그: `Ghidra_12.1.4_build`, 커밋: `8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc`.
지원 기준은 이 태그의 `Ghidra/application.properties`와 대상 Java 파일의 SHA-256입니다. master는 별도 개발 버전이며 요구 JDK가 다를 수 있습니다.

| 원문 | 표시 번역 | 접근성 이름 |
|---|---|---|
| OK | 확인(K) | 확인 |
| Cancel | 취소(C) | 취소 |
| Dismiss | 닫기(D) | 닫기 |
| Apply | 적용(A) | 적용 |

대상: `Ghidra/Framework/Docking/src/main/java/docking/DialogComponentProvider.java`의 `addOKButton`, `addCancelButton`, `addDismissButton`, `addApplyButton`.
총 4개 문구의 표시/접근성 설정 8곳입니다. 이 기본 생성 메서드를 쓰는 대화상자에서만 효과가 있습니다. 하위 클래스가 텍스트를 다시 지정하면 영어가 나타날 수 있습니다. `OptionDialog`의 별도 OK 버튼, 메뉴, 분석기, 도움말, 오류 메시지는 번역하지 않았습니다.

`setName("OK")` 등의 식별자, mnemonic K/C/D/A, 콜백, 비교 로직은 유지합니다. 표시에는 기존 mnemonic을 괄호로 남깁니다. 접근성 이름은 한국어로 변경합니다. 키보드 입력과 스크린리더 동작은 실제 GUI에서 추가 확인해야 합니다.

자동 테스트와 실제 기준 소스의 메모리 내 unified diff 정방향·역방향 검증을 수행했습니다. 로컬 Git 실행 제한으로 `git apply`는 여기서 실행하지 못했으며, Git 기반 검사는 CI와 아래 명령으로 재현하도록 구성했습니다. **Ghidra 전체 컴파일, Swing GUI, Fedora Asahi Remix 44 aarch64 실행은 검증하지 않았습니다.** 아래 명령은 재현 절차이며 성공을 보장하는 실기기 테스트 결과가 아닙니다. `docs/VERIFICATION.md` 참고.

## 구조와 방식

Ghidra는 Java/Swing Docking UI, Features/Framework/Processors 모듈, C/C++ 네이티브 도구와 Python 구성요소를 가진 Gradle 프로젝트입니다. 확인한 버튼은 Java 문자열 리터럴이며 이 패치는 ResourceBundle이나 언어 선택 기능을 추가하지 않습니다. `LANG=ko_KR.UTF-8`만으로 이 문자열이 번역되지 않습니다. 이 결과물은 한국어로 고정된 부분 빌드입니다.

`scripts/make_patch.py`는 Python 표준 라이브러리만 사용하며 **소스 파일을 수정하지 않고** unified diff를 생성합니다. 버전과 원본 해시를 검사하고 각 치환 앵커가 정확히 한 번 있는지 확인합니다. 이미 적용된 소스, 중복·누락 앵커, 변경된 기준 파일은 기본적으로 거부합니다. JSON에는 영어/한국어, 소스 위치, 검증 해시가 함께 들어 있습니다.

## 소스 준비와 패치 설치

Python 3.9 이상, Git이 필요합니다. 아래는 `ghidra-ko` 저장소 루트에서 실행합니다. 기존 작업이 없는 별도 upstream 체크아웃을 사용하세요.

```sh
python3 -m unittest discover -s tests -v
git clone --depth 1 --branch Ghidra_12.1.4_build https://github.com/NationalSecurityAgency/ghidra.git ../ghidra-src
git -C ../ghidra-src rev-parse HEAD
# 위 기준 커밋과 일치하는지 확인
python3 tests/verify_upstream.py ../ghidra-src
python3 scripts/make_patch.py ../ghidra-src --output "$PWD/local-ko.patch"
git -C ../ghidra-src apply --check "$PWD/local-ko.patch"
git -C ../ghidra-src apply "$PWD/local-ko.patch"
git -C ../ghidra-src diff --check
git -C ../ghidra-src diff
```

미리 생성된 `patches/ghidra-12.1.4-ko.patch`도 같은 기준 소스에 사용할 수 있습니다. 다른 버전에는 생성기로 다시 확인하세요. 이 ZIP은 Ghidra 실행 파일을 포함하지 않습니다.

## Fedora Asahi Remix 44 / aarch64 빌드

Apple Silicon에서 **Linux ARM64 JDK와 네이티브 바이너리**를 사용해야 합니다. macOS ARM64나 Linux x86_64 실행 파일과 혼용하지 마세요. upstream 네이티브 플랫폼 정의는 `aarch64`를 `linux_arm_64`로 매핑하고 디컴파일러 빌드에도 이 대상이 있습니다. 이것이 Fedora Asahi 전체 기능의 검증을 의미하지는 않습니다. 특히 GPU/디스플레이, 디버거 및 선택적 네이티브 구성요소는 별도 확인이 필요합니다.

기준 12.1.4 요구사항은 **64비트 JDK 21**, Gradle 8.5 이상 또는 제공 wrapper, Python 3.9–3.14와 pip, GCC/Clang 및 make입니다. 우선 해당 태그의 README와 DevGuide를 따르세요. 다른 버전은 `application.java.compiler`, `application.java.min`, `application.gradle.min`과 그 버전 문서를 다시 확인합니다.

다음은 Fedora에서 통상 사용하는 패키지명에 따른 준비 예시입니다. Asahi 44 저장소에서 이 목록의 설치 여부는 여기서 검증하지 않았습니다. 패키지가 없으면 `dnf search`로 확인하고 Linux aarch64 JDK 21을 사용하세요.

```sh
uname -m                 # aarch64 확인
cat /etc/os-release
sudo dnf install git unzip zip python3 python3-pip java-21-openjdk-devel gcc gcc-c++ make fontconfig google-noto-sans-cjk-fonts
java -version
javac -version
# 시스템 Java가 다른 버전이면 각각 JDK 21을 선택
sudo alternatives --config java
sudo alternatives --config javac
# JAVA_HOME을 설정했다면 같은 Linux aarch64 JDK 21 디렉터리인지 확인
```

한국어 글꼴이 없으면 네모가 나타납니다. `fc-match 'Noto Sans CJK KR'`로 확인하세요. 한글 입력 문제와 번역 적용 여부는 별개입니다.

앞 단계로 패치한 체크아웃에서 빌드합니다. 처음 실행은 Gradle과 외부 의존성을 다운로드하므로 인터넷 연결이 필요합니다. 서브프로젝트의 별도 라이선스 고지도 유지됩니다.

```sh
cd ../ghidra-src
./gradlew --version
./gradlew -I gradle/support/fetchDependencies.gradle
./gradlew buildNatives
./gradlew buildGhidra
ls build/dist
```

upstream DevGuide에 따르면 `buildGhidra`는 빌드한 플랫폼용 압축 배포판을 `build/dist`에 만듭니다. 생성 ZIP을 **새 디렉터리**에 풀고 그 안에서 `./ghidraRun`을 실행하세요. 기존 설치 위에 압축을 풀지 마세요. 네이티브 도구 오류가 나면 빌드 로그와 `linux_arm_64` 산출물 유무부터 확인하세요. 이 프로젝트는 Asahi용 커널/네이티브 호환성 패치를 제공하지 않습니다.

## 테스트 및 제거

1. 위 Python 테스트와 `git apply --check`, `git diff --check`를 실행합니다. CI도 기준 커밋을 받아 적용·역적용을 확인하며 Ghidra를 컴파일하지 않습니다.
2. 전체 빌드를 성공시킨 후 새로운 배포 디렉터리에서 실행합니다.
3. 위 네 기본 버튼 생성 메서드를 호출하는 대화상자를 소스 검색으로 찾아 엽니다. 단순히 아무 창이나 열면 번역이 나타나는 것은 아닙니다.
   `rg 'add(OK|Cancel|Dismiss|Apply)Button\(' Ghidra/Framework/Docking/src/main/java`
4. 번역 표시, 폭/잘림, Tab 이동, Alt+K/C/D/A, Enter/Escape, 확인/취소/적용/닫기 콜백과 스크린리더 이름을 점검합니다. 영어 식별자 기반 테스트도 유지되는지 확인합니다. 모든 대화상자에 모든 단축키가 있는 것은 아닙니다.
5. 같은 창의 원본 빌드와 비교해 보고, 검증한 OS/JDK/커밋 및 화면을 기여 문서에 기록합니다.

소스 패치를 제거하려면 `ghidra-ko` 루트에서 다음을 실행하고 원본을 다시 빌드하세요. 생성 배포판에는 소스 역적용이 자동 반영되지 않습니다.

```sh
git -C ../ghidra-src apply -R --check "$PWD/local-ko.patch"
git -C ../ghidra-src apply -R "$PWD/local-ko.patch"
```

## 다른 버전에 이식

기본 모드는 기준 버전/파일 해시가 다르면 중단합니다. 먼저 upstream diff를 검토한 다음 다음 옵션으로 **미검증 후보**를 생성할 수 있습니다.

```sh
python3 scripts/make_patch.py /path/to/other-ghidra-source --allow-unverified --output "$PWD/local-candidate.patch"
```

이 옵션도 정확한 앵커 8개를 요구하지만 의미적 호환성을 보장하지 않습니다. 비교, 식별자, 콜백, 접근성, 빌드, GUI를 검증하고 별도 버전 매니페스트/테스트를 추가하세요. 단순히 버전과 해시만 갱신해 지원을 주장하지 마세요. 장기적으로는 upstream과 논의하여 표시 문자열을 리소스로 분리하는 것이 적합합니다.

## 라이선스와 GitHub 게시

새 스크립트·번역·문서는 Apache-2.0으로 제공합니다. `LICENSE`는 기준 upstream의 Apache-2.0 전문이며 `UPSTREAM-NOTICE`는 원문 그대로 보존했습니다. `NOTICE`에는 출처와 변경 사실을 적었습니다. 패치에도 수정 지점을 주석으로 표시하며 원본 Java 라이선스 헤더를 유지합니다. NSA의 공식 제품/인증으로 표시하지 마세요.

이 스타터는 위 고지를 포함하여 GitHub에 게시하도록 구성했습니다. **GitHub에 업로드하거나 push하지 않았습니다.** 전체 Ghidra나 바이너리를 별도로 재배포할 때는 포함된 제3자 모듈의 `LICENSE.txt`, `licenses/`, NOTICE와 GPL 디렉터리의 별도 조건도 보존·검토해야 합니다. 저장소 전체가 오직 Apache-2.0인 것으로 재표시하면 안 됩니다.

ZIP을 풀어 내용을 검토한 뒤 원하면 직접 초기화할 수 있습니다. 아래 명령에는 원격 생성이나 push가 없습니다.

```sh
git init -b main
git add .
git commit -m "Initial Korean localization starter for Ghidra 12.1.4"
```

## 공식 근거

- [12.1.4 릴리스](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.1.4_build)
- [기준 README: 설치 및 빌드 요구사항](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/README.md)
- [기준 DevGuide: 빌드 및 테스트](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/DevGuide.md)
- [대상 UI 소스](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/Ghidra/Framework/Docking/src/main/java/docking/DialogComponentProvider.java)
- [기준 application.properties](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/Ghidra/application.properties)
- [네이티브 플랫폼 정의](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/GPL/nativePlatforms.gradle)
- [디컴파일러 빌드 대상](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/Ghidra/Features/Decompiler/buildNatives.gradle)
- [upstream LICENSE](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/LICENSE), [NOTICE](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1.4_build/NOTICE)
