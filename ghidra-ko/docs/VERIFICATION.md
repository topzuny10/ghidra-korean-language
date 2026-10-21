# 검증 기록

기준일: 2026-10-21. 공식 releases/latest 응답의 태그: Ghidra_12.1.4_build.
공식 GitHub API로 태그 커밋을 확인하고 raw 소스를 내려받아 검사했습니다.
커밋: 8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc.
정확한 대상 파일 SHA-256은 translations/ko.json에 기록되어 있습니다.

실행 결과:

- Python unittest 3개 통과: 알 수 없는 버전 기본 거부, 검토 모드/원본 불변, 앵커 누락·중복·이미 번역된 상태 거부.
- 실제 upstream application.properties와 Java 파일로 생성: baseline_verified=True.
- tests/verify_upstream.py 통과: 번들 패치 동일성, 독립적인 엄격한 hunk 문맥/길이 검사, 메모리 내 적용, 8개 치환, 원문 영어 식별자 보존, 역적용 후 원문 동일성.
- 소스 검토: 기존 mnemonic, setName, listener, 콜백 유지. 접근성 이름은 한국어로 변경.

실행하지 못한 검증:

- 로컬 git apply: 이 환경의 /app/bin/git은 외부 실행 포털을 사용하며 작업 경로를 찾지 못했습니다. 실제 Git 적용 성공으로 보고하지 않습니다. GitHub Actions에는 Git 기반 적용·역적용 검사를 넣었지만 아직 실행되지 않았습니다.
- 전체 Ghidra 컴파일 및 upstream Java 테스트.
- 실제 Swing 화면, 스크린리더, Alt 단축키와 UI 폭.
- Fedora Asahi Remix 44 aarch64 설치·실행과 네이티브 도구 검증.

따라서 부분 소스 번역 스타터이며, 검증된 실행 바이너리 배포판이 아닙니다.
