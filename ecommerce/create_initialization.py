from paycomuz.methods_subscribe_api import Paycom

paycom = Paycom()
p_url = paycom.create_initialization(amount=5.00, order_id='197', return_url='https://example.com/success/')
print(p_url)

