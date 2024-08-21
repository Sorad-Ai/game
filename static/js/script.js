const nav = document.querySelector(".nav"),
  searchIcon = document.querySelector("#searchIcon"),
  searchInput = document.querySelector(".search-input"), // assuming this is the class of the search input field
  navOpenBtn = document.querySelector(".navOpenBtn"),
  navCloseBtn = document.querySelector(".navCloseBtn");

searchIcon.addEventListener("click", () => {
  nav.classList.toggle("openSearch");
  nav.classList.remove("openNav");
  if (nav.classList.contains("openSearch")) {
    searchInput.focus(); // add focus to the search input field
    return searchIcon.classList.replace("uil-search", "uil-times");
  }
  searchIcon.classList.replace("uil-times", "uil-search");
});

navOpenBtn.addEventListener("click", () => {
  nav.classList.add("openNav");
  nav.classList.remove("openSearch");
  searchIcon.classList.replace("uil-times", "uil-search");
});
navCloseBtn.addEventListener("click", () => {
  nav.classList.remove("openNav");
});


// Search
document.querySelector('input[name="q"]').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
      e.preventDefault(); // Prevent the default form submission if needed
      this.form.submit(); // Submit the form
  }
});

function sug_sub(){
  document.getElementById("form").submit()
}

// Suggesation
async function fetchSuggestions(value) {
  const suggestionsContainer = document.getElementById("suggestions");
  suggestionsContainer.innerHTML = "";

  if (value) {
      const response = await fetch(`/get-suggestions/?q=${value}`);
      const suggestions = await response.json();

      suggestions.forEach(suggestion => {
          const div = document.createElement("div");
          div.classList.add("suggestion-item");
          div.textContent = suggestion;
          div.onclick = () => {
              document.getElementById("search-bar").value = suggestion;
              suggestionsContainer.innerHTML = "";
          };
          suggestionsContainer.appendChild(div);
      });
  }
}