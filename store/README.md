# Salty Pug store

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
