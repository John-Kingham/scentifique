let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
let client_secret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(stripe_public_key);
let elements = stripe.elements();
// Leave style as the Stripe default so it looks familiar to users
let style = {
    base: {
        fontSmoothing: 'antialiased',
    },
};
let card = elements.create('card', {style: style});
card.mount('#card-element');