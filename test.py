import stripe

stripe.api_key = 'sk_test_51Hpc1EFmJfyWRdx1WQNwU5IJNnzLukkBbMUGJSUYikzinx2jCVZRomLFctZWrUzYNxZih4SyLWFCciodMeFiljLn00xbDcLYwj'

stripe.PaymentIntent.create(
    amount=1000,
    currency='usd',
    payment_method_types=['card'],
    recipient_email='derekh@codingtemple.com'
)