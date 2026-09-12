document.addEventListener('DOMContentLoaded', function () {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrftoken = csrfInput ? csrfInput.value : null;

    // --- Update Project Status (project_detail page) ---
    const updateBtn = document.getElementById('update-status-btn');
    if (updateBtn) {
        const scriptTag = document.querySelector('script[data-update-url]');
        const updateUrl = scriptTag.getAttribute('data-update-url');

        updateBtn.addEventListener('click', function () {
            const newStatus = document.getElementById('status-select').value;
            const messageBox = document.getElementById('status-message');
            const badge = document.getElementById('status-badge');

            fetch(updateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                },
                body: 'status=' + encodeURIComponent(newStatus),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    badge.textContent = data.status_display;
                    badge.className = 'badge badge-' + data.status;
                    messageBox.innerHTML = '<span class="text-success">Status updated successfully.</span>';
                } else {
                    messageBox.innerHTML = '<span class="text-danger">Error: ' + data.error + '</span>';
                }
                setTimeout(() => { messageBox.innerHTML = ''; }, 3000);
            })
            .catch(error => {
                messageBox.innerHTML = '<span class="text-danger">Request failed.</span>';
            });
        });
    }

    // --- Live Client Filtering (client_list page) ---
    const sectorFilter = document.getElementById('sector-filter');
    if (sectorFilter) {
        const scriptTag = document.querySelector('script[data-filter-url]');
        const filterUrl = scriptTag.getAttribute('data-filter-url');
        const resultsDiv = document.getElementById('client-results');
        const loadingIndicator = document.getElementById('loading-indicator');

        sectorFilter.addEventListener('change', function () {
            const sector = sectorFilter.value;
            loadingIndicator.style.display = 'inline';

            fetch(filterUrl + '?sector=' + encodeURIComponent(sector))
                .then(response => response.text())
                .then(html => {
                    resultsDiv.innerHTML = html;
                    loadingIndicator.style.display = 'none';
                })
                .catch(error => {
                    loadingIndicator.style.display = 'none';
                    resultsDiv.innerHTML = '<p class="text-danger">Failed to load clients.</p>';
                });
        });
    }

    // --- Live Project Search (project_list page), preserving status filter ---
    const searchInput = document.getElementById('project-search');
    if (searchInput) {
        const scriptTag = document.querySelector('script[data-search-url]');
        const searchUrl = scriptTag.getAttribute('data-search-url');
        const status = scriptTag.getAttribute('data-status') || '';
        const rowsContainer = document.getElementById('project-rows');
        let debounceTimer;

        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const q = searchInput.value;
            debounceTimer = setTimeout(function () {
                let url = searchUrl + '?q=' + encodeURIComponent(q);
                if (status) {
                    url += '&status=' + encodeURIComponent(status);
                }
                fetch(url)
                    .then(response => response.text())
                    .then(html => {
                        rowsContainer.innerHTML = html;
                    })
                    .catch(error => {
                        rowsContainer.innerHTML = '<tr><td colspan="7" class="text-center text-danger py-4">Search failed.</td></tr>';
                    });
            }, 300);
        });
    }

    // --- Global Search (dashboard page) with Ctrl/Cmd+K shortcut ---
    const globalSearchInput = document.getElementById('global-search-input');
    if (globalSearchInput) {
        const scriptTag = document.querySelector('script[data-global-search-url]');
        const globalSearchUrl = scriptTag.getAttribute('data-global-search-url');
        const resultsBox = document.getElementById('global-search-results');
        let debounceTimer;

        globalSearchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const q = globalSearchInput.value;
            if (!q) {
                resultsBox.innerHTML = '';
                resultsBox.classList.remove('active');
                return;
            }
            debounceTimer = setTimeout(function () {
                fetch(globalSearchUrl + '?q=' + encodeURIComponent(q))
                    .then(response => response.text())
                    .then(html => {
                        resultsBox.innerHTML = html;
                        resultsBox.classList.add('active');
                    })
                    .catch(error => {
                        resultsBox.innerHTML = '<div class="search-empty">Search failed.</div>';
                        resultsBox.classList.add('active');
                    });
            }, 250);
        });

        document.addEventListener('click', function (e) {
            if (!e.target.closest('.global-search-wrapper')) {
                resultsBox.classList.remove('active');
            }
        });

        document.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                globalSearchInput.focus();
            }
        });
    }
});