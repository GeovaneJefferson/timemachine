/* ---------- VIEW SWITCHING (NEW, NON-DESTRUCTIVE) ---------- */
const views = {
  dashboard: document.getElementById('dashboard-view'),
  locations: document.getElementById('locations-view'),
  folders: document.getElementById('folders-view')
};

function showView(name) {
  Object.values(views).forEach(v => v.classList.add('hidden'));
  views[name]?.classList.remove('hidden');
}

/* Default */
showView('dashboard');

/* ---------- CONTEXT MENU LOGIC (FROM dashboard.html — UNCHANGED) ---------- */
const contextMenu = document.getElementById('context-menu');
const restoreBtn = document.getElementById('ctx-restore');

function showContextMenu(event, type) {
  event.preventDefault();
  let x = event.clientX;
  let y = event.clientY;
  contextMenu.style.left = `${x}px`;
  contextMenu.style.top = `${y}px`;

  if (type === 'folder') {
    restoreBtn.querySelector('span').textContent = 'Restore Folder';
  } else {
    restoreBtn.querySelector('span').textContent = 'Restore';
  }
  contextMenu.classList.remove('hidden');
}

function hideContextMenu() {
  contextMenu?.classList.add('hidden');
}

window.addEventListener('scroll', hideContextMenu, true);

/* ---------- NAVIGATION HOOKS (ADDED, NON-DESTRUCTIVE) ---------- */
document.addEventListener('click', e => {

  /* Sidebar: open device */
  if (e.target.closest('[data-open-device]')) {
    showView('locations');
  }

  /* Folder click */
  if (e.target.closest('[data-open-folder]')) {
    showView('folders');
  }

  /* Back buttons */
  if (e.target.closest('[data-back-dashboard]')) {
    showView('dashboard');
  }
  if (e.target.closest('[data-back-locations]')) {
    showView('locations');
  }
});
