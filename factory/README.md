# Salty Pug factory

## Finding items in factory inventory

    GET /api/find-item?kind=<kind>&color=<color>&size=<size>

Addresses:

    factory-<factory-id>
    factory-all (multicast)

Response body:

      {
          "error": null,
          "items": [
              { /* Item fields */ },
              { /* Item fields */ },
              { /* Item fields */ }
          ]
      }

## Making new items

    POST /api/make-item

Addresses:

    factory-<factory-id>
    factory-any (anycast)

Request body:

    {
        "store_id": "<store-id>",
        "item": {
            "kind": "<kind>",
            "color": "<color>",
            "size": "<size>"
        }
    }

Response body:

    {
        "error": null,
        "factory_id": "<factory-id>",
        "item_id": "<uuid>"
    }

Responses are delayed (and thus acks are slowed) if a lot of things
are currently being made.

When the process of making the item is complete, the factory calls
`//store-<store-id>/api/stock-item` to place it in the store's
inventory.

## Checking the status of an item

    GET /api/check-item-status?id=<item-id>

Addresses:

    factory-<factory-id>

Response body:

    {
        "error": null,
        "status": "<description>"
    }

## Shipping an item to a store

    POST /api/ship-item

Addresses:

    factory-<factory-id>

Request body:

    {
        "item_id": "<item-id>",
        "store_id": "<store-id>"
    }

Response body:

    {
        "error": null
    }
