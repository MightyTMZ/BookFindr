const form = document.getElementById("chatForm");
const responseContainer = document.getElementById("responseContainer");
const chatResponse = document.getElementById("chatResponse");
const bookList = document.getElementById('book_rec_list');

// Function to copy text to clipboard using Clipboard API
function copyToClipboard() {
  chatResponse.select();
  navigator.clipboard.writeText(chatResponse.value)
    .then(() => {
      alert('Text successfully copied');
    })
    .catch(err => {
      console.error('Error copying text:', err);
    });
}

form.addEventListener("submit", function (event) {
  event.preventDefault();
  const personalInterests = document.getElementById("personalInterests").value;
  const pastReadingExperiences = document.getElementById("pastReadingExperiences").value;
  const ageGroup = document.getElementById("ageGroup").value;
  const specificNeeds = document.getElementById("specificNeeds").value;
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  // Show the response container and set placeholder text
  responseContainer.style.display = "block";
  chatResponse.value = "Generating Recommendations... This may take a little while";


  // Make the API call to the Django backend
  fetch("/book-recommender/form/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken // Include the CSRF token in the fetch request headers
    },
    body: JSON.stringify({
      personalInterests: personalInterests,
      pastReadingExperiences: pastReadingExperiences,
      ageGroup: ageGroup,
      specificNeeds: specificNeeds
    })

  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }
      return response.json();
    })
    .then(data => {
      // Display the response in the read-only textarea
      chatResponse.value = data.chatResponse;
      chatResponse.placeholder = "Response from ChatGPT:";
      bookList.innerHTML = "<button type=\"button\" class=\"btn btn-outline-dark\" id='copyTextButton'>Copy Text</button><br><br>" +
        "<a href=\"/book-recommender/search\" target='_blank'>Click here to search books across multiple bookstores</a>";

      const copyTextButton = document.getElementById("copyTextButton");
      copyTextButton.addEventListener("click", copyToClipboard); // Add event listener here
    })
    .catch(error => {
      console.error("Error occurred:", error);
      chatResponse.value = "An error occurred while processing the request.";
      chatResponse.placeholder = "Response from ChatGPT:";
    });



});