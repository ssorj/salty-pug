# Factory

## Item data

An "item" in JSON format:

    {
        "id": "<uuid>",     // Not always present
        "kind": "<kind>",   // "cutlass", "pegleg", or "parrot"
        "color": "<color>", // "red", "green", or "blue"
        "size": "<size>"    // "small", "medium", or "large"
    }

## Finding items in factory inventory

    GET /api/find-item?kind=<kind>&color=<color>&size=<size>

Addresses:

    factory-<factory-id>
    factory-all (multicast)

Response body:

      {
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
        "factory_id": "<factory-id>",
        "item_id": "<uuid>"
    }

Responses are delayed (and thus acks are slowed) if a lot of things
are currently being made.

## Checking the status of an item

    GET /api/check-item-status?id=<item-id>

Addresses:

    factory-<factory-id>

Response body:

    {
        "item_status": "<description>"
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

    XXX
