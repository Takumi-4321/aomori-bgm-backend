// 💡 バックエンド（FastAPI）のURL
const API_URL = "http://localhost:8000";

// フォームの送信イベントを監視する
document
  .getElementById("loginForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault(); // 画面が勝手にリロードされるのを防ぐ

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // FastAPIの /token は「Formデータ（x-www-form-urlencoded）」で送るルールになっています
    const formData = new URLSearchParams();
    formData.append("username", email); // FastAPI側は「username」という名前でメールを受け取ります
    formData.append("password", password);

    try {
      // 🚀 バックエンドの /token にデータを送信！
      const response = await fetch(`${API_URL}/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("メールアドレスかパスワードが間違っています。");
      }

      const data = await response.json();

      // 🎫 無事に発行された「会員証（トークン）」をブラウザに保存する！
      localStorage.setItem("token", data.access_token);

      alert("ログインに成功しました！会員証を保存しました。");
      console.log("保存されたトークン:", data.access_token);
    } catch (error) {
      alert(`ログイン失敗: ${error.message}`);
    }
  });
