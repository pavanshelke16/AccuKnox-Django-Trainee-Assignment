'''
Question 1: Are Django signals executed synchronously or asynchronously by default?

Answer: By default, Django signals are executed synchronously. 
This means that when a signal is triggered, the function connected to the signal runs immediately, 
blocking further code execution until the signal completes.
'''

# Example:

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time

@receiver(post_save, sender=User)
def user_saved_signal(sender, instance, **kwargs):
    print("Signal started")
    time.sleep(2)  # Simulate a delay to show synchronous behavior
    print("Signal finished")

# Create a new user
user = User.objects.create(username="testuser")
print("User created")

'''
Explanation:

-When a user is saved, the signal is triggered.
-The signal introduces a 2-second delay with time.sleep(2),
demonstrating that the signal runs synchronously because the program waits for the signal to finish before proceeding to print "User created."
'''



'''
Question 2: Do Django signals run in the same thread as the caller?

Answer: Yes, Django signals run in the same thread as the caller by default. 
If the caller is in the main thread, the signal will also execute on the main thread.
'''

# Example:

import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_saved_signal(sender, instance, **kwargs):
    print(f"Signal is running in thread: {threading.current_thread().name}")

print(f"Main thread: {threading.current_thread().name}")
user = User.objects.create(username="testuser")

'''
Explanation:

-The code prints the thread name both in the main program and inside the signal.
-Since the output for both will be the same, it proves that Django signals run in the same thread as the caller.
'''




'''
Question 3: Do Django signals run in the same database transaction as the caller by default?

Answer: Yes, Django signals run in the same database transaction as the caller by default. 
If the caller’s transaction is rolled back, any actions performed by the signal will also be rolled back.
'''

# Example:

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import IntegrityError

@receiver(post_save, sender=User)
def user_saved_signal(sender, instance, **kwargs):
    print("Signal executed")

try:
    with transaction.atomic():
        user = User.objects.create(username="testuser")
        raise IntegrityError("Simulating a rollback")
except IntegrityError:
    print("Transaction rolled back")

print("Total users:", User.objects.count())


'''
Explanation:

-The user creation happens inside a transaction.
-When an error is raised to roll back the transaction, both the user creation and the signal’s actions are undone.
-The final count of users will be zero, proving that the signal runs within the same database transaction as the caller.
'''