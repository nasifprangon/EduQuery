const BACKEND_URL = "https://eduquery-o6vc.onrender.com";  // ✅Render URL


async function askQuestion() {
  const question = document.getElementById("question").value;
  const responseElement = document.getElementById("response");

  if (!question.trim()) {
    responseElement.innerText = "Please enter a question.";
    return;
  }

  responseElement.innerText = "Thinking... 🤔";

  try {
    const res = await fetch(`${BACKEND_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    responseElement.innerText = data.answer;
  } catch (err) {
    console.error(err);
    responseElement.innerText = "Something went wrong. Try again.";
  }
}
