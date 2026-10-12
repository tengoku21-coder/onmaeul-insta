# onmaeul-insta

1. `py make_card.py` → images/ 생성 (글 수정 시 재실행)
2. GitHub **공개** 저장소에 push (raw URL이 이미지 URL이 됨)
3. 저장소 Settings → Secrets 에 `IG_USER_ID`, `IG_TOKEN` 등록
4. Actions 탭 → instagram-post → Run workflow 로 1회 수동 실행 → 인스타 확인

## 토큰 발급 (1회)
- Instagram 프로페셔널(비즈니스) 전환 → Facebook 페이지 연결
- developers.facebook.com 앱 생성 → Graph API 탐색기 → 권한 `instagram_basic, instagram_content_publish, pages_show_list`
- 단기 토큰 → 장기 토큰(60일) 교환: `GET /oauth/access_token?grant_type=fb_exchange_token&client_id=..&client_secret=..&fb_exchange_token=..`
- IG_USER_ID: `GET /me/accounts` → page id → `GET /{page-id}?fields=instagram_business_account`
- 60일마다 토큰 갱신 필요. 만료되면 Actions 실패 메일 옴 → 그때 갱신해서 Secret 교체.

로컬 확인: `py publish.py` (토큰 없으면 캡션만 출력, 파일 변경 없음)
