const apiURL = "http://localhost:8000";  // URL backend, adapte en prod

const licenseScreen = document.getElementById("license-screen");
const chatScreen = document.getElementById("chat-screen");
const licenseInput = document.getElementById("license-input");
const licenseBtn = document.getElementById("license-btn");
const legalLink = document.getElementById("legal");
const modalLegal = document.getElementById("modal-legal");
const closeModal = document.getElementById("close-modal");

const chatWindow = document.getElementById("chat-window");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const modeBtn = document.getElementById("mode-btn");
const leaveBtn = document.getElementById("leave-btn");
const webSearchInput = document.getElementById("web-search-input");
const webSearchBtn = document.getElementById("web-search-btn");

let userLicense = "";
let mode = "normal"; // "normal" ou "vulgaire"

licenseBtn.addEventListener("click", async () => {
  const license = licenseInput.value.trim();
  if (!license) return alert("Veuillez entrer une licence.");
  try {
    const res = await fetch(`${apiURL}/check_license`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ license })
    });
    if (res.ok) {
      userLicense = license;
      licenseScreen.style.display = "none";
      chatScreen.style.display = "block";
    } else {
      alert("Licence invalide. Rejoignez notre Discord.");
      window.open("https://discord.gg/R2V2Acmb", "_blank");
    }
  } catch (e) {
    alert("Erreur serveur, réessayez.");
  }
});

legalLink.addEventListener("click", () => {
  modalLegal.style.display = "block";
});

closeModal.addEventListener("click", () => {
  modalLegal.style.display = "none";
});

modeBtn.addEventListener("click", () => {
  mode = mode === "normal" ? "vulgaire" : "normal";
  modeBtn.textContent = `Mode: ${mode.charAt(0).toUpperCase() + mode.slice(1)}`;
});

leaveBtn.addEventListener("click", () => {
  userLicense = "";
  chatScreen.style.display = "none";
  licenseScreen.style.display = "block";
  licenseInput.value = "";
  chatWindow.innerHTML = "";
});

sendBtn.addEventListener("click", async () => {
  const msg = chatInput.value.trim();
  if (!msg) return;
  appendMessage("Vous", msg);
  chatInput.value = "";
  try {
    const res = await fetch(`${apiURL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ license: userLicense, prompt: msg, mode })
    });
    if (res.ok) {
      const data = await res.json();
      appendMessage("Wum AI", data.response);
    } else {
      appendMessage("Erreur", "Erreur serveur ou licence invalide.");
    }
  } catch {
    appendMessage("Erreur", "Problème de connexion.");
  }
});

webSearchBtn.addEventListener("click", () => {
  const query = webSearchInput.value.trim();
  if (!query) return;
  const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
  window.open(url, "_blank");
});

function appendMessage(sender, message) {
  const div = document.createElement("div");
  div.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
