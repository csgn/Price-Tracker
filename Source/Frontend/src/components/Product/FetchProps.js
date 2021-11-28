import axios from 'axios';

const djangoAPI = axios.create({
  baseURL: 'http://localhost:8000/products/',
  timeout: 1000,
});

export async function fetchProductBrand(productid, callback) {
  await djangoAPI
    .get(`${productid}/brand/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProductSubcategory(productid, callback) {
  await djangoAPI
    .get(`${productid}/subcategory/`)
    .then(async (res) => {
      callback(res.data);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProductCategory(productid, callback) {
  await djangoAPI
    .get(`${productid}/category/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProductSupplier(productid, callback) {
  await djangoAPI.get(`${productid}/supplier/`).then(async (res) => {
    callback(res.data);
  });
}

export async function fetchProductPrice(productid, callback) {
  await djangoAPI
    .get(`${productid}/price/`)
    .then(async (res) => {
      let data = res.data;
      data.map((el) => {
        el.startdate = new Date(el.startdate)
          .toISOString()
          .split('T')[0]
          .toString();
      });

      callback(data);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProduct(productid, callback) {
  await djangoAPI
    .get(`${productid}/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProducts(callback) {
  await djangoAPI
    .get(`/`)
    .then(async (res) => {
      callback(res.data);
    })
    .catch((err) => {
      console.error(err);
    });
}
