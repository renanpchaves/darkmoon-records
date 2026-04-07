const API = 'http://localhost:8000';

function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = String(str);
  return d.innerHTML;
}

function showFeedback(el, type, msg) {
  el.textContent = msg;
  el.className = `feedback ${type} visible`;
}
