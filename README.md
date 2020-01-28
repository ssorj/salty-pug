# Salty Pug

## Services

 - [Store](store/) - A place where items are sold
 - [Factory](factory/) - A place where items are made
 - [Truck](factory/) - A vehicle for transporting items
 - [Console](console/) - A console for controlling the app

### Store endpoints

      //store-all/api/find-items
      //store-any/api/find-items
      //store-<store-id>/api/find-items
      //store-<store-id>/api/hold-item
      //store-<store-id>/api/stock-item

### Factory endpoints

      //factory-all/api/find-items
      //factory-any/api/make-item
      //factory-<factory-id>/api/find-items
      //factory-<factory-id>/api/make-item

## Item data

A product "item" in JSON format:

    {
        "id": "<item-id>",  // A UUID. Not always present.
        "kind": "<kind>",   // "cutlass", "pegleg", or "parrot"
        "color": "<color>", // "red", "green", or "blue"
        "size": "<size>"    // "small", "medium", or "large"
    }
