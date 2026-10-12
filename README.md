# onmaeul-insta

1. `py make_card.py` → images/ 생성 (글 수정 시 재실행)
2. GitHub **공개** 저장소에 push (raw URL이 이미지 URL이 됨)
3. 저장소 Settings → Secrets 에 `IG_USER_ID`, `IG_TOKEN` 등록
4. Actions 탭 → instagram-post → Run workflow 로 1회 수동 실행 → 인스타 확인

## 토큰 발급 (1회, Instagram 로그인 API — Facebook 페이지 불필요)
1. Instagram 앱 → 설정 → 계정 유형 → 프로페셔널(비즈니스) 전환
2. developers.facebook.com → 내 앱 → 앱 만들기 → 사용 사례 **"Instagram"** 선택 → 앱 유형 비즈니스
3. 대시보드 → Instagram → **API setup with Instagram login**
   - 1단계 "Generate access tokens" → **Add account** → 인스타 계정으로 로그인·승인
   - 계정 옆 **Generate token** 클릭 → 뜨는 값이 `IG_TOKEN` (60일 장기 토큰), 계정 옆 숫자가 `IG_USER_ID`
4. 등록: `gh secret set IG_USER_ID`, `gh secret set IG_TOKEN`
5. 60일마다 3단계 Generate token 다시 → Secret 교체. 만료되면 Actions 실패 메일 옴.

로컬 확인: `py publish.py` (토큰 없으면 캡션만 출력, 파일 변경 없음)
