document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');
  const loginButton = document.getElementById('login-button');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      // Clear any previous error messages
      errorMessage.style.display = 'none';

      // Show loading state
      loginButton.disabled = true;
      const originalButtonText = loginButton.textContent;
      loginButton.innerHTML = '<span class="loading-spinner"></span>Logging in...';

      try {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        await loginUser(email, password);
      } catch (error) {
        // Display error message
        errorMessage.textContent = error.message || 'An error occurred during login. Please try again.';
        errorMessage.style.display = 'block';
      } finally {
        // Reset button state
        loginButton.disabled = false;
        loginButton.innerHTML = originalButtonText;
      }
    });
  }

  // Check authentication on page load
  checkAuthentication();
});

async function loginUser(email, password) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Invalid credentials');
    }

    // Store JWT token in cookie
    document.cookie = `token=${data.access_token}; path=/; max-age=86400`; // 86400 seconds = 1 day

    // Redirect to main page
    window.location.href = 'index.html';
  } catch (error) {
    throw error;
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.querySelector('.nav-login');

  if (token) {
    // User is logged in
    if (loginLink) {
      loginLink.textContent = 'Logout';
      loginLink.href = '#';
      loginLink.onclick = (e) => {
        e.preventDefault();
        logout();
      };
    }
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
    return true;
  } else {
    // User is not logged in
    if (loginLink) {
      loginLink.textContent = 'Login';
      loginLink.href = 'login.html';
    }
    return false;
  }
}

function logout() {
  document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  window.location.href = 'login.html';
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
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
      <div class="place-info-index">
        <h2 class="place-title">${place.title}</h2>
        <div class="place-details">
          <p class="place-price"><span>Price per night:</span> $${place.price}</p>
        </div>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
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
