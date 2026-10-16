import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. ページの設定（スマホ対応・タイトル）
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI思考整理システム",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI思考整理システム")
st.caption("散らかったメモを入力するだけで、AIがサクッと構造化します。")

# ---------------------------------------------------------
# 2. サイドバーの設定（APIキー入力のみ）
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 設定")
    # APIキーの入力欄（パスワード隠し表示）
    api_key = st.text_input("Google AI Studio API Key", type="password", help="Gemini APIキーを入力してください")
    st.divider()
    st.markdown("💡 **使い方**\n1. APIキーを入力\n2. 下の欄にメモを入力\n3. ボタンを押して実行！")

# ---------------------------------------------------------
# 3. メイン画面：整理したい散らかったメモの入力欄
# ---------------------------------------------------------
st.subheader("3. 整理したい散らかったメモを入力")

user_memo = st.text_area(
    "ここにアイデアやメモを自由に書き込んでください",
    height=200,
    placeholder="例：新しいアプリのアイデア。大学の講義ノートを写真で撮ったら自動で単語帳を作ってくれる仕組み。初心者でも作れるかな？"
)

# 実行ボタン
if st.button("✨ メモを構造化・整理する", type="primary", use_container_width=True):
    # 入力チェック
    if not api_key:
        st.error("⚠️ 左側のサイドバーに Google AI Studio の APIキー を入力してください。")
    elif not user_memo.strip():
        st.warning("⚠️ 整理したいメモテキストを入力してください。")
    else:
        # 基本モード（シングルモード）のシステム指示
        system_instruction = """
        あなたは優秀な思考整理・要約アシスタントです。
        ユーザーから入力された雑多なメモやアイデアを整理し、以下の構成で分かりやすく出力してください。

        1. 【概要】：このアイデアの一言まとめ
        2. 【主要な要素・ポイント】：内容を箇条書きで整理
        3. 【課題や懸念点】：見落としているかもしれないポイント
        4. 【ネクストアクション】：今すぐ取り組むべき具体的な一歩

        出力はMarkdown形式で、見やすく綺麗に整えてください。
        """

        # Gemini API の呼び出し処理
        with st.spinner("AIが思考を整理中です..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=user_memo,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.3
                    )
                )
                
                # 画面への出力
                st.success("整理が完了しました！")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")