// Create and mount the Stripe card payment element
let stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
let clientSecret = $("#id_client_secret").text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();

// Leave style as the Stripe default so it looks familiar to users
let style = {
  base: {
    fontSmoothing: "antialiased",
  },
};

// Mount the card
let card = elements.create("card", { style: style });
card.mount("#card-element");
// Handle card validation errors
card.addEventListener("change", function (event) {
  let cardErrorDiv = document.getElementById("card-errors");
  if (event.error) {
    $(cardErrorDiv).html(errorMessageHtml(event.error.message));
  } else {
    cardErrorDiv.textContent = "";
  }
});

// Handle form submission
let paymentForm = document.getElementById("payment-form");
paymentForm.addEventListener("submit", function (event) {
  // Disable inputs
  event.preventDefault();
  card.update({ disabled: true });
  $("#submit-button").attr("disabled", true);
  $("#payment-form").fadeToggle(200);
  $("#loading-overlay").fadeToggle(200);

  // Attept card confirmation
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
      },
    })
    .then(function (result) {
      if (result.error) {
        // Display error message
        let cardErrorsDiv = document.getElementById("card-errors");
        $(cardErrorsDiv).html(errorMessageHtml(result.error.message));

        // Re-enable inputs so user can fix error
        card.update({ disabled: false });
        $("#submit-button").attr("disabled", false);
        $("#payment-form").fadeToggle(200);
        $("#loading-overlay").fadeToggle(200);
      } else {
        if (result.paymentIntent.status === "succeeded") {
          paymentForm.submit();
        }
      }
    });
});

// Return html to display an error message
function errorMessageHtml(message) {
  return `
    <span class="icon mr-1" role="alert">
    <i class="fas fa-circle-exclamation"></i>
    </span>
    <span>${message}</span>`;
}
