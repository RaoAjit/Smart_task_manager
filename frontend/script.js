document.getElementById("analyzeBtn").onclick = async () => {
    const raw = document.getElementById("taskInput").value;

    let tasks;
    try {
        tasks = JSON.parse(raw);
    } catch (e) {
        alert("Invalid JSON");
        return;
    }
    console.log(raw)
    console.log('akiy')
    const res = await fetch("http://localhost:8000/api/tasks/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tasks)
    });

    const data = await res.json();
    console.log(data)

    const container = document.getElementById("results");
    container.innerHTML = "";

    data.forEach(t => {
        const box = document.createElement("div");
        box.className = "task-box";
        box.innerHTML = `
            <h3>${t.title}</h3>
            <p><strong>Score:</strong> ${t.score}</p>
            <p>${t.explanation}</p>
        `;
        container.appendChild(box);
    });
};