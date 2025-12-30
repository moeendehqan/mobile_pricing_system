from zarinpal import ZarinPal
from accounting.models import transactions
from django.contrib.auth.models import User
from django.utils import timezone



class Config:
    def __init__(self, merchant_id, sandbox, access_token=None):
        self.merchant_id = merchant_id
        self.sandbox = sandbox
        self.access_token = access_token


class ZarinpalService:
    def __init__(self):
        self.merchant_id = "2b894f9c-9b1a-4c32-8a23-2ce5fb66f51a"
        self.access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZDcwM2U2YWU1MDYxYjhiMjA2NGRkZmVjNDdkY2FhM2FhNTcwNGIxMzQ4YWE3NGJlM2ZhNjkxMDM0ODYxYTVmNmEzZjAxZDI4YmJlYjQxZjIiLCJpYXQiOjE3NjcxMTIyODMuMTM5Nzg1LCJuYmYiOjE3NjcxMTIyODMuMTM5Nzg3LCJleHAiOjE5MjQ4Nzg2ODMuMTA0MTU2LCJzdWIiOiIzMTQ1MjQzIiwic2NvcGVzIjpbXX0.aoClB6BjoRyV_o0i7lQhug3gkKvj-6ur9VjqNnl9m2No1ljKJ48cRCbyhvFFkdtbmVYuFpzkoStjhr99kB7aQ5R8IEhVII7moSrF8qhnv8am5derJz5fgzYOio2Vp-e4jrS51fJ4ts5Gs-HN8Ewq5eY7wRPVXQk5IFkEI6EhFpDt9qlJ3RLSW41R7eRH77ulIOsM3nLIKjMfSyrddIeVJvehDILlFD2dL15_C3pJQNU5OgGMtIQXbfMWAtXrdOi-DwarX8PR0m0DqZiuqlbshx2nhzCKuDhEJvL17swOoxSnQPsplA4cax3EJKXUMxLATV_e5Crx5XUqseD79Rxij2qMCRTRYdcmrjYJQI6lQztQU_vCIGen2_HVFuHC47H-OoA8udfdwLBFNRdTsG3k-rjH-KNkAP2e-WKx-aN_UExD13NZgxZ5d9-jmi8ak1fpQ2gFX1p9c_u6UlCBLLLR_9qfURhFd9nIEsedl_bxN8mKtuqB5Io27-0biBhbzpVdUv48BqaZw8375ezveKznyRzR6xiqzTAngOWsRHwvU_zhoXXmKeecwyukgd7QDCLWqjRWOmHaUvMGcvUYpNfRNUA2pNZZrEYPebQKX2Jz8IOd44GSe0HTvLF0-oUGC_kanXx9e3iQIir8UOYYjF0oQnRldwfLxb_qbJ-4AsrGKnY"
        self.sandbox = True
        self.callback_url = 'https://api.shikala.com/transaction/verify/'
        self.config = Config(
            sandbox=self.sandbox,
            merchant_id=self.merchant_id,
            access_token=self.access_token,
        )
        self.zarinpal = ZarinPal(self.config)
    def create(self, amount, user: User):
        description = f"پرداخت برای {user.first_name} {user.last_name}"
        response = self.zarinpal.payments.create({
            "amount": amount,
            "description": description,
            "callback_url": self.callback_url,
            "mobile": user.phone_number,
        })
        if "data" in response and "authority" in response["data"]:
            authority = response["data"]["authority"]
            payment_url = self.zarinpal.payments.generate_payment_url(authority)
            transaction = transactions.objects.create(
                user=user,
                bede=0,
                best=amount,
                transaction_type='online',
                uniqidentifier=authority,
            )
            return payment_url
        else:
            return None
    def verify(self, authority):
        transaction = transactions.objects.get(uniqidentifier=authority)
        if transaction.is_confirmed:
            return True
        amount = transaction.best
        response = self.zarinpal.verifications.verify({
            "authority": authority,
            "amount": amount,
        })
        if "data" in response and "code" in response["data"] and response["data"]["code"] == 100:
            transaction.is_confirmed = True
            transaction.confirm_at = timezone.now()
            transaction.save()
            return True
        if "data" in response and "code" in response["data"] and response["data"]["code"] == 101:
            transaction.is_confirmed = True
            transaction.confirm_at = timezone.now()
            transaction.save()
            return True
        else:
            return False



    