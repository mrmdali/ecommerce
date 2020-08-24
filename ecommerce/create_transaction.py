from paycomuz.methods_subscribe_api import Paycom
paycom = Paycom()

# Create Card
amount = 5000.00
card = paycom.create_cards(card_number='8600 4954 7331 6478', expire='03/99', amount=amount, save=False)
print(card)
token = card['token']

verify = paycom.cards_verify(code='code', token=token)
print(verify)

# Create Transaction
result = paycom.create_transaction(token=token, order_id=1, amount=amount)
print(result)