function getInput() {
  try {
    return JSON.parse(document.getElementById("input").value);
  } catch (e) {
    alert("Invalid JSON input!");
    return null;
  }
}

let lastSchedule = [];

async function simulate() {
  const processes = getInput();
  if (!processes) return;

  const quantumValue = parseInt(document.getElementById("quantum").value);
  const quantum = quantumValue > 0 ? quantumValue : 2;

  const res = await fetch('/simulate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      algorithm: document.getElementById("algo").value,
      processes: processes,
      quantum: quantum
    })
  });

  const data = await res.json();
  lastSchedule = data;
  document.getElementById("output").textContent = JSON.stringify(data, null, 2);
  document.getElementById("gantt-container").innerHTML = ""; // clear previous gantt on simulate
}

async function recommend() {
  const processes = getInput();
  if (!processes) return;

  const res = await fetch('/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ processes: processes })
  });

  const data = await res.json();
  alert("Recommended Algorithm: " + data.suggested);
}

async function generateGantt() {
  if (!lastSchedule.length) {
    alert("Please run a simulation first!");
    return;
  }

  const res = await fetch('/gantt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lastSchedule)
  });

  const html = await res.text();
  document.getElementById("gantt-container").innerHTML = html;
}
