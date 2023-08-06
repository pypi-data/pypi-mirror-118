# Portunus

> Create and manage multi-tenant environments through a user-friendly command-line interface.

Portunus allows a user to dynamically create networks that are connected to [Faucet](https://github.com/faucetsdn/faucet), an SDN controller.  These networks can be configured with a variety of options such as NAT, DHCP, VLANs, subnets, gateways, stack links, mirroring ports, and the ability to wire in physical interfaces into the virtual network. Each network can then have Docker containers, virtual machines, and even physical devices attached to it.

Portunus uses [dovesnap](https://github.com/IQTLabs/dovesnap) behind the scenes to create these networks as well as create and attach containers to those networks. Since dovesnap is a Docker Network Plugin that uses OVS as its driver, there isn't a place for virtual machines in that ecosystem. One of the benefits of using Portunus on top of dovesnap is it knows that the docker network that the containers are attached to is really just an OVS bridge that dovesnap manages. Fortunately, there is also a libvirt driver for OVS, so Portunus handles creating and wiring in VMs to that existing network, allowing containers and VMs to live in the same specified, controlled, and monitored network.  Since it is just an OVS bridge, we can also wire in physical interfaces to the bridge, and dovesnap is smart enought to detect additions or removals of ports on these bridges and updates the network, and subsequently Faucet accordingly.

Dovesnap also enables each container to be given labels on startup that currently expose two features provided by Faucet: centralized mirroring and ACLs. Portunus also exposes these options to the user, and rounds out the compatibility by wiring in these options for VMs as well.

# Dependencies

```
docker
docker-compose
faucet
git
pip3
python3
```


# Quick Start

```
pip3 install portunus
portunus
```

In the menu, if it's the first time, choose `Install Dependencies` in addition to `Start Containers`.

# Example Environment

Portunus can be wholly configured and run on a single machine, no extra hardware or physical switches needed. However, it can also work in a distributed environment where the controller and NFV functions are in a central location and the compute resources can act almost like a cluster where nodes can be added or removed from the controller as the environment complexity needs to change. See the [example environment diagram](https://github.com/IQTLabs/portunus/blob/main/examples/environment/example_environment.svg).

# Related Components

 - [Dovesnap](https://github.com/iqtlabs/dovesnap)
 - [FaucetConfRPC](https://github.com/IQTLabs/faucetconfrpc)
 - [Open vSwitch](https://github.com/openvswitch/ovs)

# Additional Info

 - Blog posts:
   - [Take the Pain out of Orchestrating & Instrumenting Testbed Environments with Portunus](https://www.iqt.org/take-the-pain-out-of-orchestrating-instrumenting-testbed-environments-with-portunus/)
   - [Per-packet Scalable Switch Policy Controls with Dovesnap](https://www.iqt.org/per-packet-scalable-switch-policy-controls-with-dovesnap/)
   - [Bending Network Reality: Merging Virtual and Physical Networks with Dovesnap](https://www.iqt.org/bending-network-reality-merging-virtual-and-physical-networks-with-dovesnap/)
   - [Connecting Containers to Faucet](https://www.vandervecken.com/faucet/index.php/2020/05/23/connecting-containers-to-faucet/)
 - [Technology stack](https://github.com/IQTLabs/portunus/blob/main/examples/environment/portunus_tech_stack.svg)
