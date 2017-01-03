#! /bin/sed -f
s/Client { client_name: \([0-9a-fA-F]*\)\.\., proxy_node_name: \([0-9a-fA-F]*\)\.\., peer_id: PeerId(\([0-9][0-9]*\)) }/Cl(\1…,\2…,\3)/g
s/ManagedNode(name: \([0-9a-fA-F]*\)\.\.)/MN(\1…)/g
s/NaeManager(name: \([0-9a-fA-F]*\)\.\.)/NaM(\1…)/g
s/NodeManager(name: \([0-9a-fA-F]*\)\.\.)/NoM(\1…)/g
s/ClientManager(name: \([0-9a-fA-F]*\)\.\.)/ClM(\1…)/g
s/routing message/rmsg/g
s/Routing message/Rmsg/g
s/RoutingMessage/RMsg/g
s/Prefix/Pfx/g
s/Response/Rsp/g
s/Success/Succ/g
s/Failure/Fail/g
s/rmsg RMsg/RMsg/g
s/MessageId(\([0-9a-fA-F]*\)\.\.)/MId(\1…)/g
s/PeerId(\([0-9][0-9]*\))/Peer(\1)/g
s/PublicId(name: \([0-9a-fA-F]*\)\.\.)/PubId(\1…)/g
s/src: \(\(Cl\|MN\|NaM\|NoM\|ClM\)([0-9a-fA-F…,]*)\), dst: \(\(Cl\|MN\|NaM\|NoM\|ClM\)([0-9a-fA-F…,]*)\),/\1→\3/g
s/:bootstrapping:/:bg:/g
s/:content:/:c:/g
s/:routing:/:r:/g
s/:routing_table:/:rt:/g
s/:states:/:s:/g
s/:node:/:n:/g
s/:ack_manager:/:am:/g
s/[routing::[a-z_]* \([a-z_]*\)\.rs:\([0-9]*\)]/[\1:\2]/g
s/peer_manager/pmng/g
s/AckManager/AMgr/g
s/UnacknowledgedMessage/UnackdMsg/g
s/SignedMessage/SignedMsg/g
s/signatures/sigs/
