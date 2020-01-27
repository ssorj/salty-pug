# Salty Pug store

## Finding items in store inventory

    GET /api/find-items?kind=<kind>&color=<color>&size=<size>

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

## Stocking an item

    POST /api/stock-item

Addresses:

    store-<store-id>

Request body:

    {
        "item": {
            // All fields are required
            "id" "<item-id>",
            "kind": "<kind>",
            "color": "<color>",
            "size": "<size>"
        }
    }

Response body:

    {
        "error": null,
    }
