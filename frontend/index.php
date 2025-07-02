<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Wum AI</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="license-screen">
    <h1>Wum AI</h1>
    <input id="license-input" placeholder="Entrez votre licence">
    <button id="license-btn">Valider</button>
    <p class="link" id="legal">Mention légale</p>
    <a href="https://discord.gg/R2V2Acmb" id="discord-btn" target="_blank">Discord</a>
  </div>

  <div id="chat-screen" style="display:none;">
    <header>
      <span>Wum</span>
      <div>
        <button id="mode-btn">Mode: Normal</button>
        <button id="leave-btn">Leave</button>
      </div>
    </header>
    <div id="chat-window"></div>
    <textarea id="chat-input" placeholder="Votre message..."></textarea>
    <button id="send-btn">Envoyer</button>
    <input id="web-search-input" placeholder="Recherche web...">
    <button id="web-search-btn">Recherche Web</button>
    <a href="https://discord.gg/R2V2Acmb" id="discord-quick" class="highlight">Discord</a>
  </div>

  <!-- Mention légale PHP (popup) -->
  <div id="modal-legal" class="modal">
    <div class="modal-content">
      <span id="close-modal">&times;</span>
      <?php include("legal.php"); ?>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>
