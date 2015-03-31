import enulib
import os
import binascii
import time

# Create a unique payment identifier that can be used to query the status of the payment later
paymentId = binascii.hexlify(os.urandom(10))
print "Sending a payment of 12 NEKO to address 1DYucjPoEVzu7FMnwFVpKcvP9wo9ZYeF7u with payment id " + paymentId
result = enulib.create_payment("1DYucjPoEVzu7FMnwFVpKcvP9wo9ZYeF7u", 1200000000, "NEKO", paymentId, 1250)

if result['code'] == 0:
    print "Waiting 10 seconds before querying the payment (or you can poll with get_payment() until status = 'complete')"
    time.sleep(10)

    # Get full details about the payment from the enu API
    payment_status = enulib.get_payment(paymentId)
    print payment_status
else:
    print "Failed to create payment"
    print(result)