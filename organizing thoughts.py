import streamlit as st
import time
from google import genai
from google.genai import types

# ページの設定
st.set_page_config(page_title="思考整理・構造化ツール", page_icon="💡", layout="centered")

st.title("💡 思考整理・構造化ツール")
st.write("散らかったメモやアイデアを入力すると、分かりやすく4つの項目に整理してくれます。")

# ※もしここで st.secrets などからAPIキーを読み込んでいる場合は、元の記述に書き換えてください
# 例: api_key = st.secrets["GEMINI_API_KEY"] など
api_key = st.text_input("Google AI Studio APIキーを入力してください", type="password")

# 整理したいメモの入力
user_memo = st.text_area("ここにアイデアやメモを自由に書き込んでください", placeholder="例：大学の勉強法教えて")

# 構造化ボタン
if st.button("✨ メモを構造化・整理する", type="primary"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    elif not user_memo:
        st.warning("メモを入力してください。")
    else:
        # システムプロンプトの定義
        system_instruction = """
        あなたは優秀な思考整理アシスタントです。
        ユーザーから入力された散らかったメモやアイデアを受け取り、以下の4つの項目にきれいに整理・構造化して出力してください。

        1. **概要**: メモ全体の要約（1〜2行）
        2. **主要な要素**: 抽出された重要なポイントやキーワード（箇条書き）
        3. **課題**: そこから見えてくる問題点や懸念点
        4. **ネクストアクション**: 次に具体的に取るべき行動

        出力はMarkdown形式で、見やすさを重視してください。
        """

        # Gemini API の呼び出し処理（自動リトライ付き）
        with st.spinner("AIが思考を整理中です..."):
            max_retries = 3  # 最大3回まで自動でやり直す
            response = None  # レスポンス変数の初期化
            
            for attempt in range(max_retries):
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
                    # 成功したらループを抜ける
                    break
                except Exception as e:
                    # 最後の挑戦でもダメだった場合はエラーを表示
                    if attempt == max_retries - 1:
                        st.error(f"エラーが発生しました: {e}")
                    else:
                        # 一時的なエラーの場合は2秒待ってから自動で再試行
                        time.sleep(2)
            
            # 正常にレスポンスが取得できている場合のみ表示
            if response:
                st.subheader("📋 整理されたメモ")
                st.markdown(response.text)