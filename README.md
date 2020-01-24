# Salty Pug

## Endpoints

### General

      //<entity-type>-any/api/             <- A dynamically selected thing (anycast balanced treatment)
      //<entity-type>-all/api/             <- All the things (multicast)
      //<entity-type>-<entity-id>/api/     <- A particular thing
        - One for each store
        - Note that this single service would still have multiple backing processes

### Store endpoints

      Handles //store-all/api/find-item
      Handles //store-any/api/find-item
      Handles //store-<store-id>/api/find-item
      Handles //store-<store-id>/api/hold-item
      Handles //store-<store-id>/api/stock-item
      Calls //store-all/api/find-item
      Calls //store-<store-id>/api/find-item
      Calls //factory-all/api/find-item
      Calls //factory-any/api/make-item

### Factory endpoints

      Handles //factory-all/api/find-item
      Handles //factory-any/api/make-item
      Handles //factory-<factory-id>/api/find-item
      Handles //factory-<factory-id>/api/make-item
      Calls //store-<store-id>/api/stock-item

## Item data

An "item" in JSON format:

    {
        "id": "<item-id>",  // A UUID. Not always present.
        "kind": "<kind>",   // "cutlass", "pegleg", or "parrot"
        "color": "<color>", // "red", "green", or "blue"
        "size": "<size>"    // "small", "medium", or "large"
    }
