from psu_base.classes.Log import Log
from psu_cashnet.models.transaction import Transaction

log = Log()


def cashnet(request):
    cn_unprocessed = Transaction.objects.filter(status_code='R').filter(cashnet_result_code=0).count()
    return {
        "cn_unprocessed": cn_unprocessed,
    }
