# Salty Pug

## Services

 - [Store](store/) - A place where items are sold
 - [Factory](factory/) - A place where items are made
 - [Console](console/) - A console for controlling the app

<!-- - [Truck](factory/) - A vehicle for transporting items -->

## Store endpoints

      //store-<store-id>/api/find-items
      //store-<store-id>/api/hold-item
      //store-<store-id>/api/stock-item
      //store-all/api/find-items

## Factory endpoints

      //factory-<factory-id>/api/find-items
      //factory-<factory-id>/api/make-item
      //factory-<factory-id>/api/ship-item
      //factory-all/api/find-items
      //factory-any/api/make-item

## Item data

A product "item" in JSON format:

    {
        "id": "<item-id>",  // A UUID. Not always present.
        "kind": "<kind>",   // "cutlass", "pegleg", or "parrot"
        "color": "<color>", // "red", "green", or "blue"
        "size": "<size>"    // "small", "medium", or "large"
    }
