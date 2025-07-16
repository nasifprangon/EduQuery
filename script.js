async function askQuestion() {
  const question = document.getElementById("question").value;
  const res = await fetch("http://localhost:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question })
  });
  const data = await res.json();
  document.getElementById("response").innerText = data.answer;
}
