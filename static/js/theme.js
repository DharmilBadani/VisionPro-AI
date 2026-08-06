(function () {
  const root = document.documentElement;

  function applyDarkTheme() {
    root.dataset.theme = 'dark';
    root.setAttribute('data-bs-theme', 'dark');
    root.style.colorScheme = 'dark';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyDarkTheme);
  } else {
    applyDarkTheme();
  }
})();







