document.addEventListener('DOMContentLoaded', function() {
  // Live Search Functionality
  const searchInput = document.getElementById('searchInput');
  const liveSearchResults = document.getElementById('liveSearchResults');

  if (searchInput && liveSearchResults) {
    searchInput.addEventListener('input', async function() {
      const query = this.value.trim();
      
      if (query.length < 2) {
        liveSearchResults.style.display = 'none';
        return;
      }
      
      try {
        const response = await fetch('/api/search?q=${encodeURIComponent(query)}');
        const movies = await response.json();
        
        if (movies.length > 0) {
          liveSearchResults.innerHTML = '';
          movies.forEach(movie => {
            const item = document.createElement('a');
            item.href = '#';
            item.className = 'list-group-item list-group-item-action';
            
            item.innerHTML = `
              <div class="d-flex align-items-center">
                <img src="${movie.poster || 'https://via.placeholder.com/50x75'}" 
                     alt="${movie.title}" 
                     style="width: 50px; height: 75px; object-fit: cover; margin-right: 10px;">
                <div>
                  <h6 class="mb-0">${movie.title}</h6>
                  <small class="text-muted">${movie.year || 'N/A'}</small>
                </div>
              </div>
            `;
            
            item.addEventListener('click', (e) => {
              e.preventDefault();
              window.location.href = '/search?q=${encodeURIComponent(movie.title)}';
            });
            
            liveSearchResults.appendChild(item);
          });
          liveSearchResults.style.display = 'block';
        } else {
          liveSearchResults.innerHTML = '<div class="list-group-item">No results found</div>';
          liveSearchResults.style.display = 'block';
        }
      } catch (error) {
        console.error('Search failed:', error);
      }
    });

    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !liveSearchResults.contains(e.target)) {
        liveSearchResults.style.display = 'none';
      }
    });
  }

  // Add hover effects to movie cards
  const movieCards = document.querySelectorAll('.movie-card');
  movieCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'scale(1.03)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'scale(1)';
    });
  });
});
function showLoader() {
  document.getElementById('loader').classList.remove('d-none');
}