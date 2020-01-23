# Store

## Item data

An "item" in JSON format:

    {
        "id": "<item-id>",  // A UUID. Not always present.
        "kind": "<kind>",   // "cutlass", "pegleg", or "parrot"
        "color": "<color>", // "red", "green", or "blue"
        "size": "<size>"    // "small", "medium", or "large"
    }

## Finding items in store inventory

    GET /api/find-item?kind=<kind>&color=<color>&size=<size>

Addresses:

    store-<store-id>
    store-all (multicast)

Response body:

      {
          "error": null,
          "items": [
              { /* Item fields */ },
              { /* Item fields */ },
              { /* Item fields */ }
          ]
      }

## Stocking items

    POST /api/stock-item

Addresses:

    store-<store-id>

Request body:

    {
        "item": {
            "kind": "<kind>",
            "color": "<color>",
            "size": "<size>"
        }
    }

Response body:

    {
        "error": null,
    }
