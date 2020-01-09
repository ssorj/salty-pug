# Salty Pug

## Scenario 1

1. The local store (store-24) uses //store-24/api/find-item to look
   for the item in its own inventory.

   [Interesting potential for a "local store" alias here]

2. The local store uses //store-32/api/find-item to look for the item
   at a nearby store.

3. The local store uses //store/api/find-item to look for the item in
   all the stores and get the one that's closest.

4. The item is found at store-41.  The local store uses
   //store-41/api/hold-item to place the item on hold so Peaches can
   pick it up later.

### Variants

- Same steps, but with one failed backbone connection.

- Same steps, but with connectivity severed between the east coast and
  west coast.

## Scenario 2

1. Look for the pegleg that Roscoe wants.  It's not in inventory
   anywhere.

   //store/api/find-item

   //factory/api/find-item

2. The local store uses //factory/api/make-item to get one
   manufactured.  The factory with the most spare capacity accepts the
   request and begins making it.  The factory returns a tracking ID to
   the local store, which it gives to Roscoe.  Roscoe can use the ID
   to check the state of his order on the website.

   The factory uses //website/api/update-item-status to publish the
   item's degree of completion.

### Variants

- In step 1, the item is inventory at a factory, and it needs to get
shipped to a store.  I think we'll want delivery trucks for this.

- In step 2, some website instances are on the west coast, and some on
  the east.  Because //website/api/update-item-status is multicast,
  the connected websites still function properly.

## Endpoints

    In general
      //<entity-type>/api/...              <- A class of things
      //<entity-type>-<entity-id>/api/...  <- A particular thing

    Store
      Handles //store/api/find-item
      Handles //store-<store-id>/api/find-item
      Handles //store-<store-id>/api/hold-item
      Calls //store/api/find-item
      Calls //store-<store-id>/api/find-item
      Calls //factory/api/make-item

    Factory
      Handles //factory/api/find-item
      Handles //factory/api/make-item
      Handles //factory-<factory-id>/api/find-item
      Handles //factory-<factory-id>/api/make-item
      Calls //website/api/update-item-status

    Website
      Handles //website/api/update-item-status
