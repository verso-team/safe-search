from app.schemas.analysis import Agency


POLICE = Agency(
    id="police",
    name="경찰청",
    role="긴급 신고 및 사이버범죄 신고·상담",
    phone="112",
    website="https://ecrm.police.go.kr",
)

D4U = Agency(
    id="d4u",
    name="중앙디지털성범죄피해자지원센터",
    role="디지털 성범죄 상담, 삭제 지원, 수사·법률·의료 연계",
    phone="02-735-8994",
    website="https://d4u.stop.or.kr",
)

KISA_118 = Agency(
    id="kisa-118",
    name="한국인터넷진흥원 118",
    role="해킹, 스미싱, 개인정보 침해 및 불법 스팸 상담",
    phone="118",
    website="https://www.kisa.or.kr/118/",
)

FSS_1332 = Agency(
    id="fss-1332",
    name="금융감독원",
    role="보이스피싱·금융사기 상담 및 금융민원 안내",
    phone="1332",
    website="https://www.fss.or.kr",
)

WOMEN_1366 = Agency(
    id="women-1366",
    name="여성긴급전화 1366",
    role="스토킹·데이트폭력·성폭력 등 여성폭력 긴급 상담과 연계",
    phone="1366",
    website="https://www.women1366.kr",
)
