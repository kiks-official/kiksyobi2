import streamlit as st
import random

# 1. ページ設定
st.set_page_config(page_title="北神総合 系列選択ナビ", page_icon="🎓", layout="centered")

# --- データ定義 (既存の文言・ロジックは一切変更なし) ---
DESCRIPTIONS = {
    "宇宙気象系列": "めざせ宇宙！守れ地球！の理数学習を進める。宇宙・気象への興味関心を高め、人類が今後目指すことになる宇宙に関連した産業や、地球の気候をふまえた暮らしや産業をリードする人材を育成する。",
    "DX系列": "ＡＩやＩｏＴを始めとするデジタル技術を活用して、産業社会における製品やサービス、ビジネスモデルそのものを変革する等、新たな価値を創造する人材を育成する。",
    "兵庫からスタートアップ系列": "豊かな観光資源に恵まれた兵庫の魅力について学び、それを生かした仕事の創出やまちおこし、観光ビジネスに力を発揮できる、アントレプレナーシップを有する人材を育成する。",
    "スポーツアウトドアと防災系列": "スポーツやアウトドアアクティビティといった活動と、防災活動、ボランティア活動、スポーツビジネスといった人間の社会生活を結びつけ、新たな価値や生きがいを創出することのできる人材を育成する。",
    "ダイバーシティー&インクルージョン系列": "文化や年齢・様々な特性等を超えて、多様な人々と関わり理解し合うための学びを通じて、互いを認め合い生かし合えるグローバルなビジネスや文化、共生社会の担い手となる人材を育成する。",
    "リベラルアーツ理系系列": "普通科の教育課程に準じた科目配置に加えて、芸術系の科目や「キャリア探究」を設置し、複雑化する社会の諸問題に対して様々な視点を持ち、自分らしく生きるための基本となる教養を身に付ける。",
    "リベラルアーツ文系系列": "普通科の教育課程に準じた科目配置に加えて、芸術系の科目や「キャリア探究」を設置し、複雑化する社会の諸問題に対して様々な視点を持ち、自分らしく生きるための基本となる教養を身に付ける。"
}

# 追加機能：向いているキーワード
KEYWORDS = {
    "宇宙・気象系列": ["宇宙開発", "環境保護", "気象観測", "理数探究"],
    "DX系列": ["プログラミング", "AI活用", "ビジネス変革", "論理的思考"],
    "ひょうごからスタートアップ系列": ["地域創生", "起業家精神", "観光ビジネス", "企画力"],
    "スポーツ・アウトドアと防災系列": ["リーダーシップ", "野外活動", "地域防災", "健康科学"],
    "ダイバーシティー&インクルージョン系列": ["国際理解", "共生社会", "多様性", "コミュニケーション"],
    "リベラルアーツ理系系列": ["幅広い教養", "芸術的感性", "キャリア探究", "理系基礎"],
    "リベラルアーツ文系系列": ["多角的視点", "文化・芸術", "自己探究", "文系基礎"]
}

# 追加機能: 学校生活ヒントの定義
SCHOOL_TIPS = [
    "色々なクラブ活動に参加して、新しい友達を作ろう！",
    "先生や先輩に気軽に質問してみよう。きっと新しい発見があるよ！",
    "興味のあることには積極的に挑戦しよう。それが未来につながる第一歩！",
    "図書館や自習室を活用して、自分のペースで学習を進めよう。",
    "ボランティア活動に参加して、地域とのつながりを深めよう！"
]

# --- セッション状態の初期化 ---
if 'step' not in st.session_state:
    st.session_state.step = 'start'
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'history_steps' not in st.session_state:
    st.session_state.history_steps = ['start']  # 戻る機能用の遷移履歴
if 'diagnosis_history' not in st.session_state:
    st.session_state.diagnosis_history = []  # 診断結果履歴


if 'diagnosis_history' not in st.session_state:
    st.session_state.diagnosis_history = []

# --- 関数定義 ---
def move_to(next_step):
    """次のステップへ進む（履歴に保存）"""
    st.session_state.history_steps.append(next_step)
    st.session_state.step = next_step

def go_back():
    """一つ前のステップに戻る"""
    if len(st.session_state.history_steps) > 1:
        st.session_state.history_steps.pop()  # 現在のステップを削除
        st.session_state.step = st.session_state.history_steps[-1] # 一つ前に戻る

def reset_app():
    """アプリを初期化"""
    st.session_state.step = 'start'
    st.session_state.result = ""
    st.session_state.history_steps = ['start']

def save_diagnosis(res):
    """診断結果を履歴に保存（重複回避）"""
    if not st.session_state.diagnosis_history or st.session_state.diagnosis_history[-1] != res:
        st.session_state.diagnosis_history.append(res)

# 新質問用セッション変数の初期化
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'is_decided' not in st.session_state:
    st.session_state.is_decided = False

# --- サイドバー ---
with st.sidebar:
    st.title("🔗 リンク・情報")
    st.info("このアプリは新入生が自分の興味・関心に合わせて系列を考えるためのガイドです。")

    # 追加機能：診断履歴
    st.divider()
    st.subheader("📜 診断履歴")
    if st.session_state.diagnosis_history:
        for idx, item in enumerate(reversed(st.session_state.diagnosis_history)):
            st.write(f"{len(st.session_state.diagnosis_history)-idx}. {item}")
    else:
        st.caption("履歴はまだありません")

    st.divider()
    st.write("📖 **学校公式リンク**")
    st.markdown("- [北神戸総合高校 HP](https://dmzcms.hyogo-c.ed.jp/kitakobesogo-hs/NC3/)")
    st.markdown("- [学校案内パンフレット](https://dmzcms.hyogo-c.ed.jp/kitakobesogo-hs/NC3/wysiwyg/file/download/1/151)")
    # ... インスタリンクは既存コード通り (省略せず表示)
    st.markdown("- [KIKS委員公式インスタグラム](https://www.instagram.com/kitakobe_kiks.pr/?hl=ja$0)")
    st.markdown("- [KIKS男子ソフトテニスインスタグラム](https://www.instagram.com/kiks_soft.tennis_club01/)")
    st.markdown("- [KIKS女子ソフトテニスインスタグラム](https://www.instagram.com/kiks1__soft_tennis/)")
    st.markdown("- [KIKS卓球部インスタグラム](https://www.instagram.com/kiks_ttc/)")
    st.markdown("- [KIKS陸上競技部一期生インスタグラム](https://www.instagram.com/kiks._.tf1/)")
    st.markdown("- [KIKS陸上競技部二期生インスタグラム](https://www.instagram.com/kiksss2_tf/?hl=ja)")
    st.markdown("- [KIKS写真部インスタグラム](https://www.instagram.com/kikssyashinbu/)")
    st.markdown("- [KIKS放送部インスタグラム](https://www.instagram.com/kiks_hbc_official/)")
    st.divider()

    if st.button("🔄 アプリをリセット", use_container_width=True):
        reset_app()
        st.rerun()

# --- メイン画面 ---
st.title("🎓 系列になやむ人のための系列選択ナビ")

# プログレスバー
steps_map = {'IE': 10, 'IIE': 5, 'NOT': 5, 'Q1': 18, 'Q2': 26,'Q3': 34, 'Q4': 42, 'Q5': 50, 'Q6': 58, 'Q7': 66, 'Q8': 74, 'Q9': 82, 'Q10': 90, 'suki': 99, 'tiga': 0, 'tya': 0, 'goal': 100}
if st.session_state.step in steps_map:
    progress = steps_map[st.session_state.step]
    st.progress(progress / 100)
    st.caption(f"診断の進み具合: {progress}%")
    
if 'scores' not in st.session_state:
    st.session_state.scores = {
        "宇宙・気象系列": 0,
        "DX系列": 0,
        "リベラルアーツ理系系列": 0,
        "ひょうごからスタートアップ系列": 0,
        "スポーツ・アウトドアと防災系列": 0,
        "ダイバーシティー&インクルージョン系列": 0,
        "リベラルアーツ文系系列": 0
    }

# 新質問データ（全21問）の定義
DIAGNOSIS_QUESTIONS = [
    # 宇宙・気象系列 (5問)
    {"question": "Q1. グラフ・表などのデータから傾向や変化を読み取ることが好きだ", "track": "宇宙・気象系列"},
    {"question": "Q2. 天気・宇宙などに興味がある", "track": "宇宙・気象系列"},
    {"question": "Q3. 数学の計算や公式を使って、問題を解くことに抵抗がない", "track": "宇宙・気象系列"},
    {"question": "Q4. 夜空の星や天体観測、気象現象の仕組みについて調べるのが好きだ", "track": "宇宙・気象系列"},
    {"question": "Q5. 地球温暖化や気候変動などの環境問題に関心がある", "track": "宇宙・気象系列"},
    
    # DX系列 (5問)
    {"question": "Q6. パソコン・スマートフォン操作が得意だ", "track": "DX系列"},
    {"question": "Q7. 将来Web・アプリ・ゲームに関係する職に就きたいと思う", "track": "DX系列"},
    {"question": "Q8. 「こんなサービスがあったらいいのに」など新しいものを考えるのが好きだ", "track": "DX系列"},
    {"question": "Q9. プログラミングやIT技術を使って何かを作ってみたい", "track": "DX系列"},
    {"question": "Q10. AI（人工知能）や最新テクノロジーの進化にワクワクする", "track": "DX系列"},

    # ひょうごからスタートアップ系列 (5問)
    {"question": "Q11. 地元の魅力をみんなに知ってもらいたい！", "track": "ひょうごからスタートアップ系列"},
    {"question": "Q12. イベントやサービスの企画がとても好きだ", "track": "ひょうごからスタートアップ系列"},
    {"question": "Q13. 将来起業することに興味がある", "track": "ひょうごからスタートアップ系列"},
    {"question": "Q14. 地域の課題を解決するための新しいアイデアを出すのが得意だ", "track": "ひょうごからスタートアップ系列"},
    {"question": "Q15. 商品の開発やマーケティング、ビジネスの仕組みに興味がある", "track": "ひょうごからスタートアップ系列"},
    
    # スポーツ・アウトドアと防災系列 (5問)
    {"question": "Q16. 体を動かすことがとても好きだ", "track": "スポーツ・アウトドアと防災系列"},
    {"question": "Q17. 地震や豪雨などの自然災害時に人を助けたりすることに興味がある", "track": "スポーツ・アウトドアと防災系列"},
    {"question": "Q18. グループで協力して課題や活動に取り組むことが好きだ", "track": "スポーツ・アウトドアと防災系列"},
    {"question": "Q19. キャンプやハイキングなど野外・アウトドア活動が好きだ", "track": "スポーツ・アウトドアと防災系列"},
    {"question": "Q20. 応急手当や救急救命・防災グッズの知識を身につけたい", "track": "スポーツ・アウトドアと防災系列"},
    
    # ダイバーシティ&インクルージョン系列 (5問)
    {"question": "Q21. 当たり前のことになぜ？と疑問を持てる", "track": "ダイバーシティー&インクルージョン系列"},
    {"question": "Q22. 自分と違う考え方の人の意見に興味がある", "track": "ダイバーシティー&インクルージョン系列"},
    {"question": "Q23. 一つの問題に様々な立場の人の意見を考えることができる", "track": "ダイバーシティー&インクルージョン系列"},
    {"question": "Q24. 海外の文化や外国語でのコミュニケーションに興味がある", "track": "ダイバーシティー&インクルージョン系列"},
    {"question": "Q25. 看護・医療・福祉など人の役に立つ仕事に関心がある", "track": "ダイバーシティー&インクルージョン系列"},
    
    # リベラルアーツ理系系列 (5問)
    {"question": "Q26. 「なぜそうなるか」を、理由や仕組みから理解することが好き", "track": "リベラルアーツ理系系列"},
    {"question": "Q27. 将来理系の大学に進みたいが分野が決まっていない", "track": "リベラルアーツ理系系列"},
    {"question": "Q28. 仮説をたてて試行錯誤しながら答えを導くのが好きだ", "track": "リベラルアーツ理系系列"},
    {"question": "Q29. 物理・化学・生物などの実験や観察をするのが好きだ", "track": "リベラルアーツ理系系列"},
    {"question": "Q30. 幅広い理系知識を学びながら将来の進路をじっくり見つけたい", "track": "リベラルアーツ理系系列"},
    
    # リベラルアーツ文系系列 (5問)
    {"question": "Q31. 自分の考えを文章で表すことが好きだ", "track": "リベラルアーツ文系系列"},
    {"question": "Q32. 将来文系の大学に進みたいが分野が決まっていない", "track": "リベラルアーツ文系系列"},
    {"question": "Q33. 言語学や社会学に興味がある", "track": "リベラルアーツ文系系列"},
    {"question": "Q34. 本を読むことや歴史・人間・社会のニュースについて考えるのが好きだ", "track": "リベラルアーツ文系系列"},
    {"question": "Q35. 幅広い文系知識を学びながら自分のやりたいことを見つけたい", "track": "リベラルアーツ文系系列"}
]

DECIDED_OPTIONS = [
    {"text": "宇宙・理学・気象・データ解析系", "track": "宇宙・気象系列"},
    {"text": "IT・情報・Web・ゲームアプリ系", "track": "DX系列"},
    {"text": "経営・経済・地域創生・ビジネス企画系", "track": "ひょうごからスタートアップ系列"},
    {"text": "スポーツ・健康・防災・社会安全系", "track": "スポーツ・アウトドアと防災系列"},
    {"text": "社会学・国際共生・福祉・人権系", "track": "ダイバーシティー&インクルージョン系列"},
    {"text": "理系全般（まだ具体的な学科を絞りたくない）", "track": "リベラルアーツ理系系列"},
    {"text": "文系全般（まだ具体的な学科を絞りたくない）", "track": "リベラルアーツ文系系列"}
]

FOUR_CHOICES = [
    {"text": "とても当てはまる", "score": 4},
    {"text": "やや当てはまる", "score": 1},
    {"text": "あまり当てはまらない", "score": -1},
    {"text": "全く当てはまらない", "score": -2}
]


# --- 各画面の出し分け ---

# 1. スタート画面
if st.session_state.step == 'start':
    st.subheader("北神戸総合高校へようこそ！")
    st.write("あなたの未来をデザインする「系列選択」をお手伝いします。")

    # 追加機能：学校生活ヒント
    st.success(f"💡 **あなたへのヒント**\n{random.choice(SCHOOL_TIPS)}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("診断を始める", use_container_width=True, type="primary"):
            move_to('IE')
            st.rerun()
    with col2:
        if st.button("系列（天・地・人）の説明を見る", use_container_width=True):
            move_to('NO')
            st.rerun()
    # ➕ 追加：KIKSの系列の活動を見るボタン
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    if st.button("📸 KIKSの系列の活動を見る", use_container_width=True):
        move_to('kiks_activities')
        st.rerun()

# 2. 系列解説トップ
elif st.session_state.step == 'NO':
    st.subheader('KIKS系列体系「天・地・人」')
    st.write("本校の学びは、大きく3つの視点に分かれています。解説を選んでください。")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✨ 天の学び", use_container_width=True): move_to('tennkaisetu'); st.rerun()
    with col2:
        if st.button("🌍 地の学び", use_container_width=True): move_to('tikaisetu'); st.rerun()
    with col3:
        if st.button("🤝 人の学び", use_container_width=True): move_to('zinnkaisetu'); st.rerun()

# --- 解説詳細（ロジック維持） ---
elif st.session_state.step == 'tennkaisetu':
    st.subheader('✨ 天の学び')
    col1, col2 = st.columns(2)
    with col1:
        if st.button("宇宙・気象系列"): move_to('utyuukaisetu'); st.rerun()
    with col2:
        if st.button("DX系列"): move_to('DXkaisetu'); st.rerun()

elif st.session_state.step == 'utyuukaisetu':
    st.info(f"### 宇宙・気象系列\n{DESCRIPTIONS['宇宙気象系列']}")
    st.write('**📚特徴的なカリキュラム**')
    st.write('&emsp;宇宙と気象')
    st.write('&emsp;宇宙と開発')
    st.write('&emsp;古典と気象')
    st.image("utyuu.zyugyou.png", caption="宇宙・気象系列授業内容", use_container_width=True)
    st.write('・進路')
    st.write('&emsp;数学・理科を中心としたカリキュラム✨')
    st.write('&emsp;国公立・私立大学の理学部・工学部をめざすことができる系列')
    st.write('・私立大学')
    st.write('&emsp;関西学院大学の理学部など')
    st.write('・国公立大学')
    st.write('&emsp;兵庫県立大学の理学部など')
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'DXkaisetu':
    st.info(f"### DX系列\n{DESCRIPTIONS['DX系列']}")
    st.write('**📚特徴的なカリキュラム**')
    st.write('&emsp;情報Ⅱ')
    st.write('&emsp;情報システムのプログラミング')
    st.write('&emsp;ネットワークシステム')
    st.image("DX.zyugyou.png", caption="DX系列授業内容", use_container_width=True)
    st.write('・進路')
    st.write('&emsp;数学・理科・情報を中心としたカリキュラム✨')
    st.write('&emsp;国公立・私立大学の情報系学部をめざすことができる系列')
    st.write('・私立大学')
    st.write('&emsp;大阪電気通信大学、大和大学の情報学部など')
    st.write('・専門学校')
    st.write('&emsp;神戸電子専門学校')
    st.write('&emsp;神戸甲陽デザイン&テクノロジー専門学校など')
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'tikaisetu':
    st.subheader('🌍 地の学び')
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ひょうごからスタートアップ系列"): move_to('hyogokaisetu'); st.rerun()
    with col2:
        if st.button("スポーツ・アウトドアと防災系列"): move_to('autodoakaisetu'); st.rerun()

elif st.session_state.step == 'hyogokaisetu':
    st.success(f"### 兵庫からスタートアップ系列\n{DESCRIPTIONS['兵庫からスタートアップ系列']}")
    st.write('**📚特徴的なカリキュラム**')
    st.write('&emsp;ひょうごからスタートアップ')
    st.write('&emsp;観光ビジネス')
    st.write('&emsp;マーケティング')
    st.image("hyousuta.zyugyou.png", caption="ひょうごからスタートアップ系列授業内容", use_container_width=True)
    st.write('・進路')
    st.write('&emsp;社会・英語・商業を中心としたカリキュラム✨')
    st.write('&emsp;国公立・私立大学の経営系学部や公務員・起業家をめざすことができる系列')
    st.write('・私立大学')
    st.write('&emsp;法学部・文学部・経営学部・商学部')
    st.write('&emsp;武庫川大学、甲南大学、立命館大学など')
    st.write('・専門学校')
    st.write('&emsp;代々木アニメーション学院')
    st.write('&emsp;神戸ベルェベル専門学校')
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'autodoakaisetu':
    st.success(f"### スポーツ・アウトドアと防災系列\n{DESCRIPTIONS['スポーツアウトドアと防災系列']}")
    st.write('**📚特徴的なカリキュラム**')
    st.write('&emsp;アウトドア防災')
    st.write('&emsp;スポーツⅠ')
    st.write('&emsp;生涯スポーツ')
    st.image("supobou.zyugyou.png", caption="スポーツ・アウトドアと防災系列授業内容", use_container_width=True)
    st.write('・進路')
    st.write('&emsp;社会・英語・体育を中心としたカリキュラム✨')
    st.write('&emsp;国公立・私立大学の教育系学部・公務員(消防士・警察官)をめざすことができる系列')
    st.write('・私立大学')
    st.write('&emsp;法学部・教育学部')
    st.write('&emsp;甲南大学、武庫川大学など')
    st.write('・専門学校')
    st.write('&emsp;大阪ブライダル専門学校')
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'zinnkaisetu':
    st.subheader('🤝 人の学び')
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ダイバーシティ＆インクルージョン系列"): move_to('daibakaisetu'); st.rerun()
    with col2:
        if st.button("リベラルアーツ系列"): move_to('riberikaisetu'); st.rerun()

elif st.session_state.step == 'daibakaisetu':
    st.warning(f"### ダイバーシティ系列＆インクルージョン系列\n{DESCRIPTIONS['ダイバーシティー&インクルージョン系列']}")
    st.write('**📚特徴的なカリキュラム**')
    st.write('&emsp;ウェルビーイング')
    st.write('&emsp;舞台芸術とコミュニケーション')
    st.write('&emsp;韓国朝鮮語・中国語')
    st.write('&emsp;キャリア探求')
    st.image("daiba.zyugyou.png", caption="ダイバーシティー&インクルージョン系列授業内容", use_container_width=True)
    st.write('・進路')
    st.write('&emsp;英語・国語・家庭を中心としたカリキュラム✨')
    st.write('&emsp;国公立・私立大学の国際・教育系学部・公務員・NPOをめざすことができる系列')
    st.write('・国公立大学')
    st.write('&emsp;神戸市外国語大学、芸術文化専門職大学の外国語学部')
    st.write('・私立大学')
    st.write('&emsp;家政学・社会学部・心理学部・看護学部')
    st.write('&emsp;神戸女子大学、大和大学、同志社大学など')
    st.write('・専門学校')
    st.write('&emsp;関西美容専門学校')
    st.write('&emsp;神戸電子専門学校')
    st.write('&emsp;神戸医療福祉専門学校')
    st.write('&emsp;ESPエンタテインメント専門学校')
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'riberikaisetu':
    st.warning(f"### リベラルアーツ系列\n{DESCRIPTIONS['リベラルアーツ文系系列']}")
    st.write('**📚特徴的なカリキュラム**')
    st.write('・リベラルアーツ理系系列')
    st.write('&emsp;物理・化学・生物・地理')
    st.write('&emsp;数学B・C')
    st.write('&emsp;古典探究')
    st.write('・リベラルアーツ文系系列')
    st.write('&emsp;古典探究')
    st.write('&emsp;日本史・世界史')
    st.write('&emsp;数学B')
    st.write('&emsp;芸術科目')
    st.write('&emsp;英語実践')
    st.write('&emsp;政治経済')
    st.write('&emsp;キャリア探究')
    st.image("rireraru.zyugyou.png", caption="リベラルアーツ系列授業内容", use_container_width=True)
    st.write('・進路')
    st.write('&emsp;リベラルアーツ理系系列')
    st.write('&emsp;英語・数学・理化を中心としたカリキュラム✨')
    st.write('&emsp;理系の国公立・私立大学をめざすことができる系列')
    st.write('&emsp;リベラルアーツ文系系列')
    st.write('&emsp;英語・国語・社会・芸術を中心としたカリキュラム✨')
    st.write('&emsp;文系の国公立・私立大学をめざすことができる系列')
    st.write('・リベラルアーツ理系系列')
    st.write('&emsp;国公立大学の理学部')
    st.write('&emsp;私立大学の理学部・工学部など')
    st.write('・リベラルアーツ文系系列')
    st.write('&emsp;私立大学の美術・保育・医療')
    st.write('&emsp;神戸芸術工科大学など')
    st.write('・専門学校')
    st.write('&emsp;神戸元町こども&医療専門学校')
    st.write('&emsp;トヨタ神戸自動車大学校')
    if st.button("一覧に戻る"): go_back(); st.rerun()

# --- 診断ロジック（ロジック維持＋機能追加） ---
elif st.session_state.step == 'IE':
    st.subheader("Q1. 北神戸総合高校は好きですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい!",use_container_width=True): move_to("branch"); st.rerun()
    with col2:
        if st.button("いいえ",use_container_width=True): move_to("NOT"); st.rerun()

elif st.session_state.step == 'NOT':
    st.subheader("Q1. 本当に好きじゃないですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい",use_container_width=True): move_to("IIE"); st.rerun()
    with col2:
        if st.button("いいえ",use_container_width=True):move_to("branch"); st.rerun()

elif st.session_state.step == 'IIE':
    st.subheader("Q1. 本当にそうですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい", use_container_width=True): move_to('NOT'); st.rerun()
    with col2:
        if st.button("いいえ", use_container_width=True): move_to('branch'); st.rerun()

# --- 新しい質問・分岐システム ---
elif st.session_state.step == 'branch':
    st.subheader("進学希望について教えてください")
    st.write("教えて！進学したい大学や学びたい分野は、もう具体的に決まっているかな？")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい！決まっている✨\n(目的の分野から指定)", use_container_width=True):
            st.session_state.is_decided = True
            move_to('decided_select')
            st.rerun()
    with col2:
        if st.button("まだ探している！🤔\n(質問に答えて診断)", use_container_width=True):
            st.session_state.is_decided = False
            st.session_state.q_idx = 0
            st.session_state.scores = {k: 0 for k in st.session_state.scores}
            move_to('quiz')
            st.rerun()
elif st.session_state.step == 'decided_select':
    st.subheader("志望分野の選択")
    st.write("進学したい大学の学部や学びたい分野の方向性はどれに近い？")

    for opt in DECIDED_OPTIONS:
        if st.button(opt["text"], use_container_width=True):
            st.session_state.scores[opt["track"]] = 12
            move_to('goal')
            st.rerun()

elif st.session_state.step == 'quiz':
    # ランダム化された質問リストを取得
    questions = st.session_state.get('shuffled_questions', DIAGNOSIS_QUESTIONS)
    total_q = len(questions)
    curr_q = st.session_state.q_idx + 1
    q_data = questions[st.session_state.q_idx]

    st.subheader(f"質問 {curr_q} / {total_q}")
    st.info(f"**{q_data['question']}**")

    # 4段階評価ボタン
    for choice in FOUR_CHOICES:
        if st.button(f"{choice['text']} (+{choice['score']}pt)", use_container_width=True):
            st.session_state.scores[q_data['track']] += choice['score']
            if st.session_state.q_idx + 1 < total_q:
                st.session_state.q_idx += 1
                st.rerun()
            else:
                move_to('suki')
                st.rerun()

elif st.session_state.step == 'suki':
    st.subheader("Q1. 北神戸総合高校を好きになりましたか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい!",use_container_width=True): move_to("goal"); st.rerun()
    with col2:
        if st.button("いいえ",use_container_width=True): move_to("tiga"); st.rerun()

elif st.session_state.step == 'tiga':
    st.subheader("Q1. 本当に好きじゃないですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい",use_container_width=True): move_to("tya"); st.rerun()
    with col2:
        if st.button("いいえ",use_container_width=True):move_to("suki"); st.rerun()

elif st.session_state.step == 'tya':
    st.subheader("Q1. 本当にそうですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい", use_container_width=True): move_to('tiga'); st.rerun()
    with col2:
        if st.button("いいえ", use_container_width=True): move_to('suki'); st.rerun()

# --- 結果画面 ---
elif st.session_state.step == 'goal':
    st.balloons()
    highest_series = max(st.session_state.scores, key=st.session_state.scores.get)

    # 👇 ここから：結果を履歴に追加するコードを追加！
    if 'diagnosis_history' not in st.session_state:
        st.session_state.diagnosis_history = []
    # まだ今回の結果が履歴の最後に入っていない場合だけ追加（重複防止）
    if not st.session_state.diagnosis_history or st.session_state.diagnosis_history[-1] != highest_series:
        st.session_state.diagnosis_history.append(highest_series)
    # 👆 ここまでを追加
    
    st.success(f"診断完了！あなたにおすすめなのは…\n\n## 🌟 **【{highest_series}】**")
    
    descriptions = {
        "宇宙・気象系列": "めざせ宇宙！守れ地球！の理数学習を進める。宇宙・気象への興味関心を高め、人類が今後目指すことになる宇宙に関連した産業や、地球の気候をふまえた暮らしや産業をリードする人材を育成する。",
        "DX系列": "ＡＩやＩｏＴを始めとするデジタル技術を活用して、産業社会における製品やサービス、ビジネスモデルそのものを変革する等、新たな価値を創造する人材を育成する。",
        "ひょうごからスタートアップ系列": "豊かな観光資源に恵まれた兵庫の魅力について学び、それを生かした仕事の創出やまちおこし、観光ビジネスに力を発揮できる、アントレプレナーシップを有する人材を育成する。",
        "スポーツ・アウトドアと防災系列": "スポーツやアウトドアアクティビティといった活動と、防災活動、ボランティア活動、スポーツビジネスといった人間の社会生活を結びつけ、新たな価値や生きがいを創出することのできる人材を育成する。",
        "ダイバーシティー&インクルージョン系列": "文化や年齢・様々な特性等を超えて、多様な人々と関わり理解し合うための学びを通じて、互いを認め合い生かし合えるグローバルなビジネスや文化、共生社会の擔い手となる人材を育成する。",
        "リベラルアーツ理系系列": "理数教育を軸としつつ、幅広い視野を養います。複雑化する社会の諸問題に対して数理・科学的な多角的視点を持ってアプローチし、自分らしく生きるための教養を身に付ける。",
        "リベラルアーツ文系系列": "普通科の教育課程に準じた科目配置に加えて、芸術系の科目や「キャリア探究」を設置し、複雑化する社会の諸問題に対して様々な視点を持ち、自分らしく生きるための基本となる教養を身に付ける。"
    }
    st.info(descriptions[highest_series])
    
    st.divider()
    st.write("📊 **キミの診断結果スコア**")
    for series, score in st.session_state.scores.items():
        st.write(f"- {series}: {score}点")

    # 追加機能：向いているキーワード
    st.write("---")
    st.write("**🔍 この系列に向いているキーワード**")

    # 追加機能：向いているキーワーdo
    # highest_series（一番高かった系列）のキーワードを取得
    current_keywords = KEYWORDS.get(highest_series, [])
    
    if current_keywords:
        k_cols = st.columns(len(current_keywords))
        for i, kw in enumerate(current_keywords):
            k_cols[i].markdown(f"✅ {kw}")
    else:
        st.write("該当するキーワードがありません。")

    st.write("---")
    st.write("※あくまでもKIKS委員の偏見に基づいているので、今回の診断は参考程度に留めておいてくださいね！")
 
    st.divider()
    if st.button("最初からやり直す", type="primary", use_container_width=True):
        st.session_state.step = 'start'
        st.session_state.scores = {k: 0 for k in st.session_state.scores}
        st.rerun()

# --- 共通の戻るボタン (スタート画面と結果画面以外で表示) ---
if st.session_state.step not in ['start', 'goal']:
    st.divider()
    if st.button("← 前の画面に戻る"):
        go_back()
        st.rerun()
