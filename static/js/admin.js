const statusElement = document.getElementById('adminStatus');
const form = document.getElementById('settingsForm');
const panels = document.querySelectorAll('.lazy-panel');
let loadedConfig = null;

function setStatus(message, isError = false) {
  statusElement.textContent = message;
  statusElement.style.color = isError ? '#9c3f3f' : '';
}

function populateForm(config) {
  form.querySelectorAll('[name]').forEach(field => {
    const value = config[field.name];
    if(value === undefined) return;
    field.type === 'checkbox' ? field.checked = Boolean(value) : field.value = value;
  });
}

async function loadConfig() {
  if(loadedConfig) return;
  setStatus('Loading current configuration...');
  const response = await fetch(window.ZENECE_ROUTES.siteConfig);
  if(!response.ok) throw new Error('Could not load configuration.');
  loadedConfig = await response.json();
  populateForm(loadedConfig);
  setStatus('Configuration loaded.');
}

const panelObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if(!entry.isIntersecting) return;
    loadConfig().catch(error => setStatus(error.message, true));
    observer.unobserve(entry.target);
  });
}, {rootMargin:'240px'});
panels.forEach(panel => panelObserver.observe(panel));

form.addEventListener('submit', async event => {
  event.preventDefault();
  const token = document.getElementById('adminToken').value;
  const payload = {};

  form.querySelectorAll('[name]').forEach(field => {
    payload[field.name] = {
      value: field.type === 'checkbox' ? field.checked : field.value,
      value_type: field.dataset.type
    };
  });

  setStatus('Saving changes...');
  const response = await fetch(window.ZENECE_ROUTES.adminSettings, {
    method:'POST',
    headers:{'Content-Type':'application/json','X-Admin-Token':token},
    body:JSON.stringify(payload)
  });
  const result = await response.json();
  if(!response.ok) {
    setStatus(result.error || 'Could not save changes.', true);
    return;
  }
  loadedConfig = result.config;
  setStatus(`${result.updated.length} settings saved.`);
});

document.getElementById('navForm').addEventListener('submit', async event => {
  event.preventDefault();
  const links = Array.from(document.querySelectorAll('.nav-row')).map(row => ({
    id: Number(row.dataset.id),
    title: row.querySelector('[name="title"]').value,
    url: row.querySelector('[name="url"]').value,
    is_visible: row.querySelector('[name="is_visible"]').checked
  }));
  const response = await fetch('/admin/nav', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Admin-Token': document.getElementById('adminToken').value
    },
    body: JSON.stringify({links})
  });
  const result = await response.json();
  setStatus(response.ok ? 'Navigation saved.' : (result.error || 'Could not save navigation.'), !response.ok);
});
