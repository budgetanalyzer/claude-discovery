// Client-side search and filter functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const filterHigh = document.getElementById('filterHighQuality');
    const filterMedium = document.getElementById('filterMediumQuality');
    const filterLow = document.getElementById('filterLowQuality');
    const discoveriesContainer = document.getElementById('discoveries');

    // Render discovery cards
    function renderDiscoveries() {
        discoveriesContainer.innerHTML = '';

        discoveries.forEach(discovery => {
            const card = createDiscoveryCard(discovery);
            discoveriesContainer.appendChild(card);
        });

        applyFilters();
    }

    // Create a discovery card element
    function createDiscoveryCard(discovery) {
        const card = document.createElement('div');
        card.className = 'discovery-card';
        card.dataset.name = discovery.repository.name.toLowerCase();
        card.dataset.owner = discovery.repository.owner.toLowerCase();
        card.dataset.language = (discovery.repository.language || '').toLowerCase();
        card.dataset.patterns = discovery.discovery.patterns_found.join(' ').toLowerCase();
        card.dataset.score = discovery.quality.score;

        const qualityClass =
            discovery.quality.score >= 7 ? 'quality-high' :
            discovery.quality.score >= 5 ? 'quality-medium' : 'quality-low';

        const qualityLabel =
            discovery.quality.score >= 7 ? 'High Quality' :
            discovery.quality.score >= 5 ? 'Medium' : 'Lower Quality';

        const stars = discovery.repository.stars.toLocaleString();
        const language = discovery.repository.language || 'Unknown';

        const patternsHtml = discovery.discovery.patterns_found
            .map(p => `<span class="pattern-tag">${escapeHtml(p)}</span>`)
            .join('');

        const contactsHtml = discovery.contacts.slice(0, 2)
            .map(c => {
                if (c.type === 'github') {
                    return `<a href="https://github.com/${c.value}">@${c.value}</a>`;
                } else if (c.type === 'email') {
                    return escapeHtml(c.value);
                }
                return '';
            })
            .filter(c => c)
            .join(', ');

        card.innerHTML = `
            <div class="card-header">
                <div>
                    <h3 class="card-title">
                        <a href="${discovery.repository.url}" target="_blank">
                            ${escapeHtml(discovery.repository.owner)}/${escapeHtml(discovery.repository.name)}
                        </a>
                    </h3>
                </div>
                <span class="quality-badge ${qualityClass}">${qualityLabel} ${discovery.quality.score}/10</span>
            </div>

            <div class="card-meta">
                <span>⭐ ${stars}</span>
                <span>💻 ${escapeHtml(language)}</span>
            </div>

            <div class="card-description">
                ${escapeHtml(discovery.quality.reasoning || 'No description available')}
            </div>

            ${patternsHtml ? `<div class="card-patterns">${patternsHtml}</div>` : ''}

            <div class="card-footer">
                <div class="contacts">
                    ${contactsHtml ? `Contact: ${contactsHtml}` : ''}
                </div>
                <a href="${discovery.discovery.file_url}" target="_blank" class="discovery-link">
                    View ${discovery.discovery.markdown_file} →
                </a>
            </div>
        `;

        return card;
    }

    // Apply search and filters
    function applyFilters() {
        const searchTerm = searchInput.value.toLowerCase();
        const cards = discoveriesContainer.querySelectorAll('.discovery-card');

        cards.forEach(card => {
            const score = parseInt(card.dataset.score);
            const matchesSearch =
                searchTerm === '' ||
                card.dataset.name.includes(searchTerm) ||
                card.dataset.owner.includes(searchTerm) ||
                card.dataset.language.includes(searchTerm) ||
                card.dataset.patterns.includes(searchTerm);

            const matchesQuality =
                (filterHigh.checked && score >= 7) ||
                (filterMedium.checked && score >= 5 && score < 7) ||
                (filterLow.checked && score < 5);

            if (matchesSearch && matchesQuality) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });

        updateStats();
    }

    // Update visible stats
    function updateStats() {
        const visibleCards = discoveriesContainer.querySelectorAll('.discovery-card:not(.hidden)');
        document.getElementById('totalCount').textContent = visibleCards.length;
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Event listeners
    searchInput.addEventListener('input', applyFilters);
    filterHigh.addEventListener('change', applyFilters);
    filterMedium.addEventListener('change', applyFilters);
    filterLow.addEventListener('change', applyFilters);

    // Initial render
    renderDiscoveries();
});
