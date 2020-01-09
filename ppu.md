# Pirate Pugs Unlimited

Pirate Pugs Unlimited (PPU) makes high-quality adventureware for pugs
who embrace a nautical and criminal lifestyle.

## General ideas

 - No AMQP, only HTTP.  But it uses HTTP in ways that show the
   underlying power of messaging.

 - All data is local to the entities at the edge - stores and factories
   and delivery trucks.  There is no central data store.  This is to
   highlight the potential advantages for reliability and our ability
   to directly communicate to the edges.

## Model

 - Stores - This is where pugs go to buy our adventureware
 - Factories - This is where we make the adventureware
 - Delivery trucks - This is how we get the adventureware from our
   factories to our stores

Stores, factories, and delivery trucks each have an inventory database
and a location.

Each instance of each entity has its own private cluster.

We need some public clusters for backbone availability.  You could have one
cheaper Amazon one and a more expensive Google one, and this can show traffic flow
based on cost settings.

## Scenario 1

Peaches (a fancy pug with little respect for the law of the sea) walks
in to her local store seeking a cutlass.  It is unavailable at this
store.  The staff want to help, so they first query a nearby store
that's close to Peaches' home.  It doesn't have it, so they query all
the other stores and find the closest store that has the item.
Peaches decides, yes, she wants it, so the staff put the item on hold.

### Communications

 - Simple unicast HTTP request to query a known local alternative stores
 - Multicast HTTP request to query inventory at all the stores

   POST /all-stores/
   XXX-Reply-To-Me: /store/32

 - Standard point-to-point HTTP request to hold the item

### Iterations

1. No failures.  All the stores report the requested inventory.

2. One backbone connection fails, but because the network has
   redundant connections, all the stores are still able to report
   their inventory.

3. Then our cloud provider for the backbone goes down, fully disconnecting half of the
   stores.  Because the other half remain connected and the data is
   stored at each store, not a central database, they can still report
   their inventory.
   XXX - Gear this toward two cloud providers

## Scenario 2

Roscoe (he's neuvo-punk, has some authority issues, loves boats) walks
in to his local store, seeking a clear plastic tunic, size medium.
The staff help him check all the stores, and none are available, so he
needs to order one from the factory.  He sends his order to a factory,
and he receives a tracking ID.  He wants to pick it up at the store
when it's available, so he also requests that it be sent to his local
store.

When the factory finishes making the tunic, they notify him that it's
done and making its way to the store.  The tracking ID also enables
him to see where the delivery truck with his item is.

### Communications

 - Anycast HTTP request to send the work order
   - Dynamic load balancing based on factory backlog
 - "Fire and forget" multicast HTTP for sending position data from the delivery
   trucks

### Iterations

[The same reliability iterations could apply here]

------------------------------------------------------------------------------------------------------------------

Demo concept loosely based on EdgeWorx talks,
that hits all of our killer-demo points.
###########################################################

Scenario
-------------------------------------

You have a manufacturing enterprise.
It consists of management offices,
factories, and warehouses.

In the cloud you have a three-mesh of routers to
redundantly connect the sales and management offices
to the factories and warehouses.

At each factory and warehouse you have one edge router,
which serves scores or hundreds of edge clients -- manufacturing
and materials handling devices.

The many edge clients are running on small hardware
similar to Raspberry Pi.



Killer-Demo Points
-------------------------------------

1. Dynamic Load Balancing
   Management traffic down to the factories is dynamically
   load balanced based on how fast the various factories
   are consuming work orders.


2. Ease and Flexibility of Setup
   Show how the system can be set up easily with Skupper.


3. Command and Control
   This is the management traffic down to factories.


4. Edge to Edge
   Factories talk to Warehouses to get stuff that they need,
   and also to each other.

   Also there in traffic that stays within a single factory
   or warehouse. The edge devices talk to each other while
   doing their jobs.


5. Anycast
   The edge routers anycast work-orders to manufacturing
   devices.


6. Multicast
   Edge routers sometimes multicast messages that need to go
   to all edge devices. I.e. shutdown commands.


7. Adapt to network change.
   If one of the 3-mesh interior routers goes down, the network
   adapts. If one of the connections from an interior to an edge
   fails, a different interior router starts serving that edge
   router.


8. Rollout Upgrade/Downgrade
   Show how this can work on both interior and edge routers.
   Upgrade without shutdown.


9. New services appearing.
   Show new edge devices appearing in the factories, and
   joining the network.

   Show new services appearing in the cloud that the factories
   and warehouses start talking to.

   New management and sales services appearing and subscribing
   to topics of messages that are sent up from factories to
   management.
