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
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'DXkaisetu':
    st.info(f"### DX系列\n{DESCRIPTIONS['DX系列']}")
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
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'autodoakaisetu':
    st.success(f"### スポーツ・アウトドアと防災系列\n{DESCRIPTIONS['スポーツアウトドアと防災系列']}")
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
    if st.button("一覧に戻る"): go_back(); st.rerun()

elif st.session_state.step == 'riberikaisetu':
    st.warning(f"### リベラルアーツ系列\n{DESCRIPTIONS['リベラルアーツ文系系列']}")
    if st.button("一覧に戻る"): go_back(); st.rerun()

# --- 診断ロジック（ロジック維持＋機能追加） ---
elif st.session_state.step == 'IE':
    st.subheader("Q1. 北神戸総合高校は好きですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい!",use_container_width=True): move_to("Q1"); st.rerun()
    with col2:
        if st.button("いいえ",use_container_width=True): move_to("NOT"); st.rerun()

elif st.session_state.step == 'NOT':
    st.subheader("Q1. 本当に好きじゃないですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい",use_container_width=True): move_to("IIE"); st.rerun()
    with col2:
        if st.button("いいえ",use_container_width=True):move_to("Q1"); st.rerun()

elif st.session_state.step == 'IIE':
    st.subheader("Q1. 本当にそうですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい", use_container_width=True): move_to('NOT'); st.rerun()
    with col2:
        if st.button("いいえ", use_container_width=True): move_to('Q1'); st.rerun()

elif st.session_state.step == 'Q1':
    st.subheader("Q1. 目の前に「絶対に開かない宝箱」があります。あなたならどうする？")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("A. 道具を使って開ける", use_container_width=True):
            st.session_state.scores["リベラルアーツ理系系列"] += 1
            st.session_state.step = 'Q2'
            st.rerun()
    with col2:
        if st.button("B. 箱を観察する", use_container_width=True):
            st.session_state.scores["宇宙・気象系列"] += 1
            st.session_state.step = 'Q2'
            st.rerun()
    with col3:
        if st.button("C. 人と協力して開ける", use_container_width=True):
            st.session_state.scores["ダイバーシティー&インクルージョン系列"] += 1
            st.session_state.step = 'Q2'
            st.rerun()
    with col4:
        if st.button("D. 箱の仕組みを考える", use_container_width=True):
            st.session_state.scores["リベラルアーツ理系系列"] += 1
            st.session_state.step = 'Q2'
            st.rerun()

elif st.session_state.step == 'Q2':
  st.subheader("Q2. 旅の途中で、見たこともない奇妙な形の植物を見つけました。最初にすることは？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. 植物を観察する", use_container_width=True):
            st.session_state.scores["宇宙・気象系列"] += 1
            st.session_state.step = 'Q3'
            st.rerun()
  with col2:
      if st.button("B.店を開いてお土産として売る", use_container_width=True):
            st.session_state.scores["ひょうごからスタートアップ系列"] += 1
            st.session_state.step = 'Q3'
            st.rerun()
  with col3:
      if st.button("C. 友達に言葉で伝える", use_container_width=True):
            st.session_state.scores["リベラルアーツ文系系列"] += 1
            st.session_state.step = 'Q3'
            st.rerun()
  with col4:
      if st.button("D. 注意を促す看板を作る", use_container_width=True):
            st.session_state.scores["スポーツ・アウトドアと防災系列"] += 1
            st.session_state.step = 'Q3'
            st.rerun()

elif st.session_state.step == 'Q3':
  st.subheader("Q3. あなたはタイムマシンで「22世紀の未来」へ飛ばされました。最初にチェックするものは？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. スマホやPCなどの文明の進化", use_container_width=True):
            st.session_state.scores["DX系列"] += 1
            st.session_state.step = 'Q4'
            st.rerun()
  with col2:
      if st.button("B. 火星や月への移住", use_container_width=True):
            st.session_state.scores["宇宙・気象系列"] += 1
            st.session_state.step = 'Q4'
            st.rerun()
  with col3:
      if st.button("C. 地元の建物や伝統文化", use_container_width=True):
            st.session_state.scores["ひょうごからスタートアップ系列"] += 1
            st.session_state.step = 'Q4'
            st.rerun()
  with col4:
      if st.button("D.科学技術やエネルギー事情", use_container_width=True):
            st.session_state.scores["リベラルアーツ理系系列"] += 1
            st.session_state.step = 'Q4'
            st.rerun()

elif st.session_state.step == 'Q4':
  st.subheader("Q4. 友達と2人で無人島に漂流してしまいました。あなたの担当（役割）はどれ？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. 周囲を散策し観察する", use_container_width=True):
            st.session_state.scores["宇宙・気象系列"] += 1
            st.session_state.step = 'Q5'
            st.rerun()
  with col2:
      if st.button("B. 危ないところがないか確認する", use_container_width=True):
            st.session_state.scores["スポーツ・アウトドアと防災系列"] += 1
            st.session_state.step = 'Q5'
            st.rerun()
  with col3:
      if st.button("C. ルールを決める", use_container_width=True):
            st.session_state.scores["ダイバーシティー&インクルージョン系列"] += 1
            st.session_state.step = 'Q5'
            st.rerun()
  with col4:
     if st.button("D. 娯楽を作る", use_container_width=True):
            st.session_state.scores["リベラルアーツ文系系列"] += 1
            st.session_state.step = 'Q5'
            st.rerun()

elif st.session_state.step == 'Q5':
  st.subheader("Q5. 魔法の絵の具をもらいました。描いた絵が本物になるとしたら、何を描く？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. 超高性能なPC", use_container_width=True):
            st.session_state.scores["DX系列"] += 1
            st.session_state.step = 'Q6'
            st.rerun()
  with col2:
      if st.button("B. ゴミをエネルギーに変えるマシン", use_container_width=True):
            st.session_state.scores["宇宙・気象系列"] += 1
            st.session_state.step = 'Q6'
            st.rerun()
  with col3:
      if st.button("C. 新しいお店やテーマパーク", use_container_width=True):
            st.session_state.scores["ひょうごからスタートアップ系列"] += 1
            st.session_state.step = 'Q6'
            st.rerun()
  with col4:
      if st.button("D翻訳機能付きのイヤリング. ", use_container_width=True):
            st.session_state.scores["ダイバーシティー&インクルージョン系列"] += 1
            st.session_state.step = 'Q6'
            st.rerun()

elif st.session_state.step == 'Q6':
  st.subheader("Q6. 朝起きたら、なぜか自分の体が「透明人間」になっていました！最初にする行動は？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. 国家機密を盗み出す", use_container_width=True):
            st.session_state.scores["DX系列"] += 1
            st.session_state.step = 'Q7'
            st.rerun()
  with col2:
      if st.button("B. バズってる店の裏側をみる", use_container_width=True):
            st.session_state.scores["ひょうごからスタートアップ系列"] += 1
            st.session_state.step = 'Q7'
            st.rerun()
  with col3:
      if st.button("C. 人助けをする", use_container_width=True):
            st.session_state.scores["スポーツ・アウトドアと防災系列"] += 1
            st.session_state.step = 'Q7'
            st.rerun()
  with col4:
      if st.button("D. 閉館後の美術館や図書館に行く", use_container_width=True):
            st.session_state.scores["リベラルアーツ文系系列"] += 1
            st.session_state.step = 'Q7'
            st.rerun()

elif st.session_state.step == 'Q7':
  st.subheader("Q7. 学校の自動販売機に「？ボタン」という謎のボタンが出現しました。あなたなら？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. 出てきたものを記録し統計をとる", use_container_width=True):
            st.session_state.scores["リベラルアーツ理系系列"] += 1
            st.session_state.step = 'Q8'
            st.rerun()
  with col2:
      if st.button("B. 新しいビジネスとして広める", use_container_width=True):
            st.session_state.scores["ひょうごからスタートアップ系列"] += 1
            st.session_state.step = 'Q8'
            st.rerun()
  with col3:
      if st.button("C. 友達と何が出てくるか相談して押す", use_container_width=True):
            st.session_state.scores["ダイバーシティー&インクルージョン系列"] += 1
            st.session_state.step = 'Q8'
            st.rerun()
  with col4:
      if st.button("D. 誰が仕掛けてるか考える", use_container_width=True):
            st.session_state.scores["リベラルアーツ文系系列"] += 1
            st.session_state.step = 'Q8'
            st.rerun()

elif st.session_state.step == 'Q8':
  st.subheader("Q8. あなたは映画の監督になりました。どんなジャンルの作品を撮りたい？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. AIが人類を救う物語", use_container_width=True):
            st.session_state.scores["DX系列"] += 1
            st.session_state.step = 'Q9'
            st.rerun()
  with col2:
      if st.button("B. 壮大な自然のドキュメンタリー", use_container_width=True):
            st.session_state.scores["宇宙・気象系列"] += 1
            st.session_state.step = 'Q9'
            st.rerun()
  with col3:
      if st.button("C. 寂れた港町を復興させる物語", use_container_width=True):
            st.session_state.scores["ひょうごからスタートアップ系列"] += 1
            st.session_state.step = 'Q9'
            st.rerun()
  with col4:
      if st.button("D. 人々が、音楽を通じて一つになる物語", use_container_width=True):
            st.session_state.scores["ダイバーシティー&インクルージョン系列"] += 1
            st.session_state.step = 'Q9'
            st.rerun()

elif st.session_state.step == 'Q9':
  st.subheader("Q9. 街で迷子になっている外国人の子供を見かけました。言葉が通じないようです。どうする？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. 翻訳アプリで会話", use_container_width=True):
            st.session_state.scores["DX系列"] += 1
            st.session_state.step = 'Q10'
            st.rerun()
  with col2:
      if st.button("B. 身振り手振りのジェスチャーで安心させる", use_container_width=True):
            st.session_state.scores["ダイバーシティー&インクルージョン系列"] += 1
            st.session_state.step = 'Q10'
            st.rerun()
  with col3:
      if st.button("C. 周りの大人や警察にすぐ連絡する", use_container_width=True):
            st.session_state.scores["スポーツ・アウトドアと防災系列"] += 1
            st.session_state.step = 'Q10'
            st.rerun()
  with col4:
      if st.button("D. 子供を観察しその子に適した手助けをする", use_container_width=True):
            st.session_state.scores["リベラルアーツ文系系列"] += 1
            st.session_state.step = 'Q10'
            st.rerun()

elif st.session_state.step == 'Q10':
  st.subheader("Q10. 1日だけ「校長先生」になれるチケットを手に入れました。何を企画する？")
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      if st.button("A. 全校生徒でeスポーツ大会を開く", use_container_width=True):
            st.session_state.scores["DX系列"] += 1
            st.session_state.step = 'suki'
            st.rerun()
  with col2:
      if st.button("B. みんなでBBQをする", use_container_width=True):
            st.session_state.scores["スポーツ・アウトドアと防災系列"] += 1
            st.session_state.step = 'suki'
            st.rerun()
  with col3:
      if st.button("C. 山にキャンプで泊まりに行く", use_container_width=True):
            st.session_state.scores["宇宙・気象系列"] += 1
            st.session_state.step = 'suki'
            st.rerun()
  with col4:
      if st.button("D. 時間割をなくし自由登校にする", use_container_width=True):
            st.session_state.scores["リベラルアーツ文系系列"] += 1
            st.session_state.step = 'suki'
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
