const API_URL = "http://localhost:8000";

const loginSection = document.getElementById("loginSection");
const memberSection = document.getElementById("memberSection");
const bgmList = document.getElementById("bgmList");

// 🔄 画面の表示を切り替える関数
function checkAuth() {
  const token = localStorage.getItem("token");
  if (token) {
    // 会員証がある ➔ ログイン画面を隠して、会員エリアを表示
    loginSection.classList.add("hidden");
    memberSection.classList.remove("hidden");
    fetchBGMList(); // BGM一覧を取得しに行く
  } else {
    // 会員証がない ➔ 会員エリアを隠して、ログイン画面を表示
    loginSection.classList.remove("hidden");
    memberSection.classList.add("hidden");
  }
}

// 📥 バックエンドからBGM一覧を取得して画面に表示する関数
async function fetchBGMList() {
  try {
    const response = await fetch(`${API_URL}/bgms`);
    if (!response.ok) throw new Error("BGMの取得に失敗しました");

    const bgms = await response.json();
    bgmList.innerHTML = ""; // 一旦リストを空にする

    if (bgms.length === 0) {
      bgmList.innerHTML = "<li>登録されているBGMがありません。</li>";
      return;
    }

    // 取得したBGMを1件ずつ画面に追加していく
    bgms.forEach((bgm) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${bgm.title}</strong> (by User #${bgm.owner_id})`;
      bgmList.appendChild(li);
    });
  } catch (error) {
    console.error("エラー:", error);
  }
}

// 🎫 ログインフォームの送信処理
document
  .getElementById("loginForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
      const response = await fetch(`${API_URL}/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      if (!response.ok)
        throw new Error("メールアドレスかパスワードが間違っています。");

      const data = await response.json();
      localStorage.setItem("token", data.access_token); // トークン保存

      alert("ログイン成功！");
      checkAuth(); // 👈 画面を切り替える！
    } catch (error) {
      alert(`ログイン失敗: ${error.message}`);
    }
  });

// 🚪 ログアウト処理
document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token"); // 会員証を捨てる
  alert("ログアウトしました。");
  checkAuth(); // 👈 画面を切り替える！
});

// 🚀 ページを読み込んだ瞬間に、すでにログイン済みかチェックする
checkAuth();
