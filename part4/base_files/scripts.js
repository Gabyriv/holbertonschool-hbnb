document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }

  // Check authentication on page load
  checkAuthentication();
});

async function loginUser(email, password) {
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
  }
}

function getCookie(name) {
  // Function to get a cookie value by its name
  // Your code here
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function
  fetch('http://localhost:5000/api/v1/places/', {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(response => response.json())
    .then(data => displayPlaces(data));
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  places.forEach(place => {
    const placeDiv = document.createElement('div');
    placeDiv.className = 'place-card';
    placeDiv.dataset.price = place.price;

    placeDiv.innerHTML = `
      <div class="place-info">
        <h2 class="place-title">${place.title}</h2>
        <div class="place-details">
          <p class="place-price"><span>Price per night:</span> $${place.price}</p>
        </div>
        <button href="place.html?id=${place.id}" class="details-button">View Details</button>
      </div>
    `;

    placesList.appendChild(placeDiv);
  });

  // Store places data for filtering
  window.placesData = places;
  setupPriceFilter();
}

function setupPriceFilter() {
  const priceFilter = document.getElementById('price-filter');

  priceFilter.addEventListener('change', (event) => {
    const selectedPrice = event.target.value === 'all' ? Infinity : parseInt(event.target.value);
    const places = document.querySelectorAll('.place-card');

    places.forEach(place => {
      const price = parseInt(place.dataset.price);
      place.style.display = price <= selectedPrice ? 'block' : 'none';
    });
  });
}
