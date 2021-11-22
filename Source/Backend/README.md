# Backend

## Product

```http
GET /products/
```

```javascript
{
    productid: integer,
    name: varchar,
    images: [ varchar ],
    rate: float,
    url: varchar,
    brandid: integer,
    categoryid: integer
},
...
```

---

```http
GET /products/<productid>
```

```javascript
{
    productid: integer,
    name: varchar,
    images: [ varchar ],
    rate: float,
    url: varchar,
    brandid: integer,
    categoryid: integer
}
```

---

```http
GET /products/<productid>/price
```

```javascript
{
    priceid: integer,
    amount: float,
    startdate: timestamp,
    supplierid: integer
},
...
```

---

```http
GET /products/<productid>/subcategory
```

```javascript
{
    subcategoryid: integer,
    name: varchar,
    url: varchar,
    categoryid: integer
},
...
```

---

```http
GET /products/<productid>/category
```

```javascript
{
    categoryid: integer,
    name: varchar,
    url: varchar
}
```

---

```http
GET /products/<productid>/brand
```

```javascript
{
    brandid: integer,
    name: varchar,
    url: varchar
}
```

---

```http
GET /products/<productid>/supplier
```

```javascript
{
    supplierid: integer,
    name: varchar,
    rate: float,
    url: varchar
},
...
```

---

---

## Supplier

```http
GET /suppliers/
```

```javascript
{
    supplierid: integer,
    name: varchar,
    rate: float,
    url: varchar
},
...
```

---

```http
GET /suppliers/<supplierid>
```

```javascript
{
    supplierid: integer,
    name: varchar,
    rate: float,
    url: varchar
}
```

---

```http
GET /suppliers/<supplierid>/subcategory
```

```javascript
{
    subcategoryid: integer,
    name: varchar,
    url: varchar,
    categoryid: integer
},
...
```

---

```http
GET /suppliers/<supplierid>/category
```

```javascript
{
    categoryid: integer,
    name: varchar,
    url: varchar,
},
...
```

---

```http
GET /suppliers/<supplierid>/brand
```

```javascript
{
    brandid: integer,
    name: varchar,
    url: varchar
}
```

---

```http
GET /suppliers/<supplierid>/product
```

```javascript
{
    productid: integer,
    name: varchar
    images: [ varchar ],
    url: varchar,
    rate: float,
    brandid: integer,
    categoryid: integer
},
...
```

---

---

## Brand

```http
GET /brands/
```

```javascript
{
    supplierid: integer,
    name: varchar,
    rate: float,
    url: varchar
},
...
```

---

```http
GET /brands/<brandid>
```

```javascript
{
    brandid: integer,
    name: varchar,
    url: varchar
}
```

---

```http
GET /brands/<brandid>/subcategory
```

```javascript
{
    subcategoryid: integer,
    name: varchar,
    url: varchar,
    categoryid: integer
},
...
```

---

```http
GET /brands/<brandid>/category
```

```javascript
{
    categoryid: integer,
    name: varchar,
    url: varchar,
},
...
```

---

```http
GET /brands/<brandid>/supplier
```

```javascript
{
    supplierid: integer,
    name: varchar,
    url: varchar
}
```

---

```http
GET /brands/<brandid>/product
```

```javascript
{
    productid: integer,
    name: varchar,
    images: [ varchar ],
    url: varchar,
    rate: float,
    brandid: integer,
    categoryid: integer
},
...
```

## Category

```http
GET /categories/
```

```javascript
{
    categoryid: integer,
    name: varchar,
    url: varchar
},
...
```

---

```http
GET /categories/<categoryid>
```

```javascript
{
    categoryid: integer,
    name: varchar,
    url: varchar
}
```

---

```http
GET /categories/<categoryid>/subcategory
```

```javascript
{
    subcategoryid: integer,
    name: varchar,
    url: varchar,
    categoryid: integer
},
...
```

---

```http
GET /categories/<categoryid>/brand
```

```javascript
{
    brandid: integer,
    name: varchar,
    url: varchar,
},
...
```

---

```http
GET /categories/<categoryid>/supplier
```

```javascript
{
    supplierid: integer,
    name: varchar,
    url: varchar
},
...
```

---

```http
GET /categories/<categoryid>/product
```

```javascript
{
    productid: integer,
    name: varchar,
    images: [ varchar ],
    url: varchar,
    rate: float,
    brandid: integer,
    categoryid: integer
},
...
```

## Subcategory

```http
GET /subcategories/
```

```javascript
{
    subcategoryid: integer,
    name: varchar,
    url: varchar
},
...
```

---

```http
GET /subcategories/<subcategoryid>
```

```javascript
{
    subcategoryid: integer,
    name: varchar,
    url: varchar
}
```

---

```http
GET /subcategories/<subcategoryid>/category
```

```javascript
{
    categoryid: integer,
    name: varchar,
    url: varchar,
},
...
```

---

```http
GET /subcategories/<subcategoryid>/brand
```

```javascript
{
    brandid: integer,
    name: varchar,
    url: varchar,
},
...
```

---

```http
GET /subcategories/<subcategoryid>/supplier
```

```javascript
{
    supplierid: integer,
    name: varchar,
    url: varchar
},
...
```

---

```http
GET /subcategories/<subcategoryid>/product
```

```javascript
{
    productid: integer,
    name: varchar,
    images: [ varchar ],
    url: varchar,
    rate: float,
    brandid: integer,
    categoryid: integer
},
...
```
