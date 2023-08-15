document.addEventListener("DOMContentLoaded", function() {
        document.getElementById("search-form").addEventListener("submit", function(event) {
            event.preventDefault();  // Prevent the form from submitting normally

            const form_data = {
                "search-book": document.getElementById("book-item").value,
                "csrfmiddlewaretoken": document.querySelector("[name=csrfmiddlewaretoken]").value
            };

            // Show loading message
            const searchResultsDiv = document.getElementById("search-results");
            searchResultsDiv.innerHTML = "";
            searchResultsDiv.style.height = 'auto'; // gets rid of hard coded style
            searchResultsDiv.innerHTML = "<p>Loading... This may take a little while</p>";



            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/book-recommender/search/", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("X-CSRFToken", document.querySelector('input[name="csrfmiddlewaretoken"]').value);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText);

                    // Clear previous content
                    searchResultsDiv.innerHTML = "";

                    // Create a function to render search results
                    function renderSearchResults(results) {
                        results.forEach(result => {
                            const productItemDiv = document.createElement("div");
                            productItemDiv.className = "productItem";

                            const productImageDiv = document.createElement("div");
                            productImageDiv.className = "productImage";
                            const productImage = document.createElement("img");
                            productImage.src = result.product_image;
                            productImage.alt = "Book cover";
                            productImageDiv.appendChild(productImage);
                            productItemDiv.appendChild(productImageDiv);

                            const productInfoDiv = document.createElement("div");
                            productInfoDiv.className = "productInfo";

                            const productTitle = document.createElement("h1");
                            productTitle.className = "productTitle";
                            productTitle.textContent = result.title;
                            productInfoDiv.appendChild(productTitle);

                            const propertyLabels = {
                                main_price: "Hardcover or Paperback:",
                                kindle_price: "Kindle:",
                                audible_price: "Audible:",
                                availability: "Availability:"
                            };

                            for (const property in result) {
                                if (property !== "product_image" && property !== "title" && property !== "link") {
                                    const h3Element = document.createElement("h3");
                                    h3Element.className = property.includes("img") ? "priceLabelWithImage" : "priceLabel";
                                    if (propertyLabels[property]) {
                                        h3Element.textContent = `${propertyLabels[property]} ${result[property]}`;
                                        if (property.includes("img")) {
                                            const imgElement = document.createElement("img");
                                            imgElement.src = result[property];
                                            imgElement.alt = `${property} Logo`;
                                            h3Element.appendChild(imgElement);
                                        }
                                        productInfoDiv.appendChild(h3Element);
                                    }
                                }
                            }

                            const linkH3 = document.createElement("h3");
                            linkH3.innerHTML = `
                                Note the information above could be wrong or misleading.
                                If you want full details visit <a target="_blank" href="${result.link}">here</a>.
                            `;
                            productInfoDiv.appendChild(linkH3);

                            productItemDiv.appendChild(productInfoDiv);
                            searchResultsDiv.appendChild(productItemDiv);
                        });
                    }

                    function renderSearchResultsTPL(results) {
                        results.forEach(result => {
                            const productItemDiv = document.createElement("div");
                            productItemDiv.className = "productItem";

                            const productImageDiv = document.createElement("div");
                            productImageDiv.className = "productImage";
                            const productImage = document.createElement("img");
                            productImage.src = result.book_image;
                            productImage.alt = "Book cover";
                            productImageDiv.appendChild(productImage);
                            productItemDiv.appendChild(productImageDiv);

                            const productInfoDiv = document.createElement("div");
                            productInfoDiv.className = "productInfo";

                            const productTitle = document.createElement("h1");
                            productTitle.className = "productTitle";
                            productTitle.textContent = result.title;
                            productInfoDiv.appendChild(productTitle);

                            // Render holds_info, year, type, print_length properties
                            const propertiesToRender = ["holds_info", "year", "type", "print_length"];
                            propertiesToRender.forEach(property => {
                                const h3Element = document.createElement("h3");
                                h3Element.className = "priceLabel";
                                h3Element.textContent = result[property];
                                productInfoDiv.appendChild(h3Element);
                            });

                            const linkH3 = document.createElement("h3");
                            linkH3.innerHTML = `
                                Note the information above could be wrong, misleading or not up-to-date.
                                If you want to place hold, view full details and availability, please visit <a target="_blank" href="${result.link}">here</a>.
                            `;
                            productInfoDiv.appendChild(linkH3);

                            productItemDiv.appendChild(productInfoDiv);
                            searchResultsDiv.appendChild(productItemDiv);
                        });
                    }

                    function renderSearchResultsIndigo(bookJson) {
                        const productItemDiv = document.createElement("div");
                        productItemDiv.className = "productItem";

                        const productImageDiv = document.createElement("div");
                        // productImageDiv.className = "productImage";
                        const productImage = document.createElement("img");
                        productImage.src = bookJson.book_cover;
                        productImage.alt = "Book cover";
                        productImage.style.width = "75%"; // Adjust the width as needed
                        productImageDiv.appendChild(productImage);
                        productItemDiv.appendChild(productImageDiv);

                        const productInfoDiv = document.createElement("div");
                        productInfoDiv.className = "productInfo";

                        const productTitle = document.createElement("h1");
                        productTitle.className = "productTitle";
                        productTitle.textContent = bookJson.title;
                        productInfoDiv.appendChild(productTitle);

                        const propertiesToRender = [
                            { label: "Author:", property: "author" },
                            { label: "Price:", property: "price" },
                        ];

                        propertiesToRender.forEach(info => {
                            const value = bookJson[info.property];
                            if (value !== undefined && value !== null) {
                                const h3Element = document.createElement("h3");
                                h3Element.className = "priceLabel";
                                h3Element.textContent = `${info.label} ${value}`;
                                productInfoDiv.appendChild(h3Element);
                            }
                        });

                        const linkH3 = document.createElement("h3");
                        linkH3.innerHTML = `
                            Note: The information above could be wrong, misleading, or not up-to-date.
                            If you want to access more details such as delivery, pick up, prices of other formats, visit <a target="_blank" href="${bookJson.access_link}">here</a>.
                        `;
                        productInfoDiv.appendChild(linkH3);

                        productItemDiv.appendChild(productInfoDiv);
                        searchResultsDiv.appendChild(productItemDiv);
                    }


                    const amazonLogo = document.createElement("img");
                    amazonLogo.src = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg";
                    amazonLogo.alt = "Amazon Logo";
                    amazonLogo.style.marginBottom = "35px";
                    amazonLogo.style.marginTop = "20px";
                    amazonLogo.style.width = "40%";
                    searchResultsDiv.appendChild(amazonLogo);

                    if (data.topSearchResults.length === 0) {
                        const noResultsDiv = document.createElement("div");
                        noResultsDiv.className = "noResults";
                        noResultsDiv.textContent = "No results found.";
                        searchResultsDiv.appendChild(noResultsDiv);
                    } else {
                        renderSearchResults(data.topSearchResults);
                    }

                    if (data.topSearchResultsTPL.length !== 0) {
                        // Add TPL logo before TPL results
                        const tplLogo = document.createElement("img");
                        tplLogo.src = "https://upload.wikimedia.org/wikipedia/commons/4/47/Toronto_Public_Library_Logo.png";
                        tplLogo.alt = "TPL Logo";
                        tplLogo.style.marginTop = "20px";
                        tplLogo.style.marginBottom = "35px";
                        tplLogo.style.width = "30%";
                        searchResultsDiv.appendChild(tplLogo);

                        renderSearchResultsTPL(data.topSearchResultsTPL);
                    }
                    if (data.topSearchResultsIndigo.length !== 0) {
                    // Add Indigo logo before Indigo results
                    const indigoLogo = document.createElement("img");
                    indigoLogo.src = "https://upload.wikimedia.org/wikipedia/commons/9/96/Indigo_logo.png";
                    indigoLogo.alt = "Indigo and Chapters logo";
                    indigoLogo.style.marginTop = "20px";
                    indigoLogo.style.marginBottom = "35px";
                    indigoLogo.style.width = "30%";
                    searchResultsDiv.appendChild(indigoLogo);

                    data.topSearchResultsIndigo.forEach(indigoResult => {
                        renderSearchResultsIndigo(indigoResult);
                    });
                }


                } else if (xhr.readyState === 4) {
                    console.error("Error:", xhr.status);
                }
            };
            xhr.send(JSON.stringify(form_data));
        });
    });