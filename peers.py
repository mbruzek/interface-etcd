from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class EtcdPeer(RelationBase):
    '''This class handles peer relation communication by setting states that
    the reactive code can respond to. '''

    scope = scopes.UNIT

    @hook('{peers:etcd}-relation-joined')
    def peer_joined(self):
        '''A new peer has joined, set the state on the unit so we can track
        when they are departed. '''
        conv = self.conversation()
        conv.set_state('{relation_name}.joined')

    @hook('{peers:etcd}-relation-departed')
    def peers_going_away(self):
        '''Trigger a state on the unit that it is leaving. We can use this
        state in conjunction with the joined state to determine which unit to
        unregister from the etcd cluster. '''
        conv = self.conversation()
        conv.remove_state('{relation_name}.joined')
        conv.set_state('{relation_name}.departing')

    def dismiss(self):
        '''Remove the departing state from all other units in the conversation,
        and we can resume normal operation.
        '''
        for conv in self.conversations():
            conv.remove_state('{relation_name}.departing')

    def get_peers(self):
        '''Return a list of peer names participating in the conversation scope
        '''
        peers = []
        # Iterate over all the conversations of this type.
        for conversation in self.conversations():
            peers.append(conversation.scope)
        return peers
