from paycomuz.methods_subscribe_api import Paycom

from clickuz import ClickUz

c_url = ClickUz.generate_url(order_id='172',amount='150000',return_url='http://example.com')
print(c_url)

paycom = Paycom()
p_url = paycom.create_initialization(amount=5.00, order_id='197', return_url='https://example.com/success/')
print(p_url)

