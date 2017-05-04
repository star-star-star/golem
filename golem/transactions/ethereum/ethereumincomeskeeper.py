from golem.transactions.incomeskeeper import IncomesKeeper
from ethereum.utils import sha3, decode_hex


def _same_node(addr_info, node_id):
    if len(node_id) > 32:
        node_id = decode_hex(node_id)
    return sha3(node_id)[12:] == addr_info


class EthereumIncomesKeeper(IncomesKeeper):
    def received(self, sender_node_id, task_id, subtask_id, transaction_id, value):
        # FIXME:
        # W ether weryfikować, że blok/płatnośc istnieje
        # oraz, że płatność jest skierowana do nas (ethereumtransactionsystem.get_payment_address
        return super(EthereumIncomesKeeper, self).received(sender_node_id, task_id, subtask_id, transaction_id, value)
